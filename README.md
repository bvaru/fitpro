# FitPro — Fitness Program Web Application

A production-ready fitness program website with Razorpay payments, admin dashboard, and PostgreSQL/SQLite support.

## 🗂 Project Structure

```
fitpro/
├── app.py              # Main Flask application (all routes & models)
├── requirements.txt    # Python dependencies
├── Procfile            # Gunicorn start command for Render
├── runtime.txt         # Python version for Render
├── .env.example        # Environment variable template
├── .gitignore
└── templates/
    ├── index.html      # Landing page (hero, plans, testimonials, contact)
    ├── admin_login.html# Admin login page
    └── dashboard.html  # Admin dashboard (users + payments tables)
```

## 🚀 Local Setup

### 1. Clone and enter directory
```bash
git clone <your-repo>
cd fitpro
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
```bash
cp .env.example .env
# Edit .env with your values
```

### 5. Run locally
```bash
python app.py
```
Visit: http://localhost:5000

---

## 🌐 Deploy to Render

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

### Step 2: Create Render Web Service
1. Go to https://render.com → New → Web Service
2. Connect your GitHub repo
3. Set these:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Python Version:** 3.11

### Step 3: Add Environment Variables in Render Dashboard
| Variable | Value |
|---|---|
| `SECRET_KEY` | (generate a random string) |
| `DATABASE_URL` | (auto-filled if using Render PostgreSQL) |
| `RAZORPAY_KEY` | `rzp_live_XXXXXXX` |
| `RAZORPAY_SECRET` | your secret |
| `ADMIN_USERNAME` | admin |
| `ADMIN_PASSWORD` | your-secure-password |

### Step 4: Add Render PostgreSQL
1. Render Dashboard → New → PostgreSQL
2. Copy the **Internal Database URL**
3. Add it as `DATABASE_URL` in your Web Service environment variables

---

## 💳 Razorpay Setup

1. Create account at https://razorpay.com
2. Go to Settings → API Keys → Generate Test Key
3. Add `RAZORPAY_KEY` and `RAZORPAY_SECRET` to environment variables
4. For live payments, generate Live Key and replace

---

## 🔐 Admin Panel

| Route | Description |
|---|---|
| `/admin` | Login page |
| `/dashboard` | Users & payments overview |
| `/download` | Export Excel file |
| `/admin/logout` | Logout |

Default credentials (change via env vars):
- Username: `admin`
- Password: `fitpro@2024`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/register` | Register user, returns `user_id` |
| `POST` | `/api/create-order` | Create Razorpay order |
| `POST` | `/api/verify-payment` | Verify signature, save payment |

---

## 🔧 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | Flask session secret |
| `DATABASE_URL` | Optional | PostgreSQL URL (SQLite fallback) |
| `RAZORPAY_KEY` | ✅ | Razorpay API key |
| `RAZORPAY_SECRET` | ✅ | Razorpay secret key |
| `ADMIN_USERNAME` | Optional | Admin login (default: admin) |
| `ADMIN_PASSWORD` | Optional | Admin password (default: fitpro@2024) |

---

## 📱 User Flow

1. User lands on homepage → scrolls through plans
2. Clicks "Join Now" on a plan
3. Modal opens → enters Name, Email (optional), Phone
4. Backend registers user → creates Razorpay order
5. Razorpay checkout opens
6. User pays → backend verifies signature
7. Payment saved as "paid" → success screen shown
8. WhatsApp link opens with pre-filled message to coach

---

## 🛡️ Security

- Razorpay HMAC-SHA256 signature verification before saving payments
- Session-based admin authentication
- All dashboard routes protected with `@login_required`
- Phone validation (10-digit Indian mobile numbers only)
