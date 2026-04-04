import os
import hmac
import hashlib
import json
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, jsonify,
    session, redirect, url_for, send_file
)
from flask_sqlalchemy import SQLAlchemy
import razorpay

# ── App & Config ─────────────────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

# Database: prefer PostgreSQL (DATABASE_URL), fall back to SQLite
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///fitpro.db")
# Render uses postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

RAZORPAY_KEY    = os.environ.get("RAZORPAY_KEY", "rzp_test_XXXXXXXXXXXXXXXX")
RAZORPAY_SECRET = os.environ.get("RAZORPAY_SECRET", "your_razorpay_secret")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "fitpro@2024")

# ✏️  Set your WhatsApp number in the OWNER_WHATSAPP environment variable
# Format: country code + number, no + or spaces. E.g. 919876543210
OWNER_WHATSAPP = os.environ.get("OWNER_WHATSAPP", "919999999999")

rzp_client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

# ── Models ────────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = "users"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(200), nullable=True)
    phone      = db.Column(db.String(20), nullable=False, unique=True)
    plan       = db.Column(db.String(80), nullable=True)
    instagram  = db.Column(db.String(120), nullable=True)
    # "registered" = lead who filled the form; "paid" = completed payment
    status     = db.Column(db.String(20), nullable=False, default="registered")
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payments   = db.relationship("Payment", backref="user", lazy=True)


class Payment(db.Model):
    __tablename__ = "payments"
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount         = db.Column(db.Integer, nullable=False)   # paise
    status         = db.Column(db.String(30), default="created")
    payment_id     = db.Column(db.String(120), nullable=True)
    order_id       = db.Column(db.String(120), nullable=True)
    plan_name      = db.Column(db.String(80), nullable=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()
    # Migrate: add `status` column to existing databases that predate this field
    try:
        db.session.execute(db.text(
            "ALTER TABLE users ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'registered'"
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()  # Column already exists — safe to ignore
    # Migrate: add `instagram` column
    try:
        db.session.execute(db.text(
            "ALTER TABLE users ADD COLUMN instagram VARCHAR(120)"
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()  # Column already exists — safe to ignore
    # Migrate: add `is_deleted` column
    try:
        db.session.execute(db.text(
            "ALTER TABLE users ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE"
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()  # Column already exists — safe to ignore


@app.context_processor
def inject_now():
    return {"now": datetime.utcnow()}

# ── Auth helpers ──────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

# ── Public routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", razorpay_key=RAZORPAY_KEY)


@app.route("/api/register", methods=["POST"])
def register():
    data      = request.get_json()
    name      = (data.get("name") or "").strip()
    email     = (data.get("email") or "").strip()
    phone     = (data.get("phone") or "").strip()
    plan      = (data.get("plan") or "").strip()
    instagram = (data.get("instagram") or "").strip().lstrip("@")

    if not name or not phone:
        return jsonify({"error": "Name and phone are required."}), 400

    # Normalise: strip +91, spaces, dashes → 10 digits
    digits = phone.replace("+91", "").replace(" ", "").replace("-", "")
    if not digits.isdigit() or len(digits) != 10:
        return jsonify({"error": "Enter a valid 10-digit Indian mobile number."}), 400

    # Prevent duplicates: if this phone already exists, update name/email/plan
    # and return the same user_id (no new row created)
    user = User.query.filter_by(phone=digits).first()
    if user:
        user.name      = name
        user.email     = email or user.email
        user.plan      = plan  or user.plan
        user.instagram = instagram or user.instagram
        db.session.commit()
        return jsonify({
            "user_id": user.id,
            "status":  user.status,
            "message": "Welcome back! Proceeding with your existing account.",
        })

    # New user — status defaults to "registered" (lead)
    user = User(
        name      = name,
        email     = email or None,
        phone     = digits,
        plan      = plan or None,
        instagram = instagram or None,
        status    = "registered",
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "user_id": user.id,
        "status":  user.status,
        "message": "Registered successfully.",
    })


@app.route("/api/create-order", methods=["POST"])
def create_order():
    data    = request.get_json() or {}
    user_id = data.get("user_id")
    amount  = data.get("amount")   # in paise
    plan    = data.get("plan", "")

    if not user_id or not amount:
        return jsonify({"error": "user_id and amount are required."}), 400

    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid payment amount."}), 400

    if amount <= 0:
        return jsonify({"error": "Enter a valid payment amount."}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    try:
        order = rzp_client.order.create({
            "amount":   amount,
            "currency": "INR",
            "receipt":  f"receipt_uid_{user_id}_{int(datetime.utcnow().timestamp())}",
            "notes":    {"plan": plan, "user_id": str(user_id)},
        })
    except Exception as e:
        return jsonify({"error": f"Razorpay error: {str(e)}"}), 500

    payment = Payment(
        user_id  = user_id,
        amount   = amount,
        status   = "created",
        order_id = order["id"],
        plan_name= plan,
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "order_id":   order["id"],
        "amount":     order["amount"],
        "currency":   order["currency"],
        "key":        RAZORPAY_KEY,
        "user_name":  user.name,
        "user_email": user.email or "",
        "user_phone": user.phone,
    })


@app.route("/api/verify-payment", methods=["POST"])
def verify_payment():
    import urllib.parse
    data               = request.get_json() or {}
    razorpay_order_id  = data.get("razorpay_order_id")
    razorpay_payment_id= data.get("razorpay_payment_id")
    razorpay_signature = data.get("razorpay_signature")
    user_id            = data.get("user_id")

    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        return jsonify({"error": "Missing payment details."}), 400

    # ── Verify HMAC signature ─────────────────────────────────────────────────
    body     = f"{razorpay_order_id}|{razorpay_payment_id}"
    expected = hmac.new(
        RAZORPAY_SECRET.encode("utf-8"),
        body.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    pmt = Payment.query.filter_by(order_id=razorpay_order_id).order_by(Payment.created_at.desc()).first()
    if not pmt:
        return jsonify({"error": "Payment order not found."}), 404

    if user_id and str(pmt.user_id) != str(user_id):
        return jsonify({"error": "Payment user mismatch."}), 400

    if not hmac.compare_digest(expected, razorpay_signature):
        pmt.status = "failed"
        db.session.commit()
        return jsonify({"error": "Payment verification failed."}), 400

    # ── Update payment record ─────────────────────────────────────────────────
    if pmt.status != "paid":
        pmt.status     = "paid"
        pmt.payment_id = razorpay_payment_id

    # ── Mark user as paid ─────────────────────────────────────────────────────
    user = db.session.get(User, pmt.user_id)
    if user:
        user.status = "paid"
        if pmt and pmt.plan_name:
            user.plan = pmt.plan_name

    db.session.commit()

    # ── Build WhatsApp deep-link with rich pre-filled message ─────────────────
    plan_name  = pmt.plan_name if pmt else "a plan"
    amount_inr = f"₹{pmt.amount // 100:,}" if pmt else ""
    user_name  = user.name if user else "A user"
    user_phone = user.phone if user else ""

    msg = (
        f"Hello! 🙏 I just completed my payment for the *21 Days Weight Loss Program*.\n\n"
        f"*Name:* {user_name}\n"
        f"*Plan:* {plan_name}\n"
        f"*Amount Paid:* {amount_inr}\n"
        f"*Payment ID:* {razorpay_payment_id}\n\n"
        f"I'm excited to start my transformation journey. "
        f"Please let me know the next steps! 💪"
    )
    whatsapp_url = f"https://wa.me/{OWNER_WHATSAPP}?text=" + urllib.parse.quote(msg)

    return jsonify({
        "success":      True,
        "message":      "Payment verified successfully!",
        "payment_id":   razorpay_payment_id,
        "user_name":    user_name,
        "user_phone":   user_phone,
        "plan_name":    plan_name,
        "amount_inr":   amount_inr,
        "whatsapp":     whatsapp_url,
    })

# ── Admin routes ──────────────────────────────────────────────────────────────

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard"))
        error = "Invalid credentials."
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/dashboard")
@login_required
def dashboard():
    users    = User.query.filter_by(is_deleted=False).order_by(User.created_at.desc()).all()
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    total_revenue = sum(p.amount for p in payments if p.status == "paid") // 100
    paid_count    = sum(1 for p in payments if p.status == "paid")
    paid_users    = sum(1 for u in users if u.status == "paid")
    lead_users    = sum(1 for u in users if u.status == "registered")
    return render_template(
        "dashboard.html",
        users=users,
        payments=payments,
        total_revenue=total_revenue,
        paid_count=paid_count,
        paid_users=paid_users,
        lead_users=lead_users,
    )

@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_deleted = True
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/download")
@login_required
def download_excel():
    import pandas as pd
    import io

    all_users = User.query.order_by(User.created_at.desc()).all()
    payments = Payment.query.order_by(Payment.created_at.desc()).all()

    users_data = [{
        "ID":         u.id,
        "Name":       u.name + (" (Deleted)" if getattr(u, 'is_deleted', False) else ""),
        "Email":      u.email or "",
        "Phone":      u.phone,
        "Instagram":  ("@" + u.instagram) if u.instagram else "",
        "Plan":       u.plan or "",
        "Status":     u.status.upper(),
        "Registered": u.created_at.strftime("%Y-%m-%d %H:%M"),
    } for u in all_users]

    payments_data = [{
        "ID":         p.id,
        "User ID":    p.user_id,
        "User Name":  p.user.name if p.user else "",
        "Plan":       p.plan_name or "",
        "Amount (₹)": p.amount / 100,
        "Status":     p.status,
        "Payment ID": p.payment_id or "",
        "Order ID":   p.order_id or "",
        "Date":       p.created_at.strftime("%Y-%m-%d %H:%M"),
    } for p in payments]

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame(users_data).to_excel(writer, sheet_name="Users", index=False)
        pd.DataFrame(payments_data).to_excel(writer, sheet_name="Payments", index=False)
    output.seek(0)

    filename = f"fitpro_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
