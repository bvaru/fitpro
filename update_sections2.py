import re

def update_file():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 4. Transformations Replacement
    tg_new = """<div class="tg-track" id="tgTrack">

          <!-- Card 1: Founder -->
          <div class="tg-card">
            <div class="tg-img">
              <img src="/static/images/owner.jpeg" alt="Founder Transformation" onerror="this.src='/static/images/client0.jpeg'" />
            </div>
            <div class="tg-body">
              <div class="tg-name">Founder's Story</div>
              <div class="tg-detail">"I started this journey to transform myself before helping others. Real Indian food, daily workouts."</div>
              <div class="tg-chip"><i class="bi bi-award-fill"></i> Lost 25kg &bull; Plan: DIAMOND</div>
            </div>
          </div>

          <!-- Card 2: Weight Loss -->
          <div class="tg-card">
            <div class="tg-img">
              <img src="/static/images/client1.jpeg" alt="Transformation" onerror="this.src='/static/images/client2.jpeg'" />
            </div>
            <div class="tg-body">
              <div class="tg-name">Priya S.</div>
              <div class="tg-detail">"From XXL to L in just three rounds of 21 days. The live Zoom sessions kept me accountable."</div>
              <div class="tg-chip"><i class="bi bi-award-fill"></i> Lost 15kg &bull; Plan: PRO</div>
            </div>
          </div>
          
          <!-- Card 3: Child Nutrition -->
          <div class="tg-card">
            <div class="tg-img">
              <img src="/static/images/client3.jpeg" alt="Transformation" onerror="this.src='/static/images/client4.jpeg'" />
            </div>
            <div class="tg-body">
              <div class="tg-name">Aarav M. (12 yrs)</div>
              <div class="tg-detail">"Developed healthy eating habits and became so active. No strict diets, just right home food!"</div>
              <div class="tg-chip"><i class="bi bi-award-fill"></i> Lost 6kg &bull; Plan: KICKSTART</div>
            </div>
          </div>
          
          <!-- Card 4: Skin Program -->
          <div class="tg-card">
            <div class="tg-img">
              <img src="/static/images/client5.jpeg" alt="Transformation" onerror="this.src='/static/images/client6.jpeg'" />
            </div>
            <div class="tg-body">
              <div class="tg-name">Neha R.</div>
              <div class="tg-detail">"Cleared my acne entirely simply by changing my food intake based on the nutrition education!"</div>
              <div class="tg-chip"><i class="bi bi-award-fill"></i> Glowing Skin &bull; Plan: SKIN PROGRAM</div>
            </div>
          </div>

          <!-- Card 5: Weight Gain -->
          <div class="tg-card">
            <div class="tg-img">
              <img src="/static/images/client7.jpeg" alt="Transformation" onerror="this.src='/static/images/client8.jpeg'" />
            </div>
            <div class="tg-body">
              <div class="tg-name">Rahul K.</div>
              <div class="tg-detail">"Gaining muscle was so hard. The program showed me the right meal portions for natural bulk."</div>
              <div class="tg-chip"><i class="bi bi-award-fill"></i> Gained 8kg &bull; Plan: WEIGHT GAIN</div>
            </div>
          </div>
"""
    # Replace from `<div class="tg-track" id="tgTrack">` up to `</div><!-- /tg-track -->` or `<div class="tg-nav">`
    tg_start = content.find('<div class="tg-track" id="tgTrack">')
    tg_end = content.find('</div>\n      </div>\n\n      <div class="tg-nav">', tg_start)
    if tg_end == -1:
        # fallback
        tg_end = content.find('<div class="tg-nav">', tg_start)
        tg_end = content.rfind('</div>', tg_start, tg_end)
        tg_end = content.rfind('</div>', tg_start, tg_end)

    if tg_start != -1 and tg_end != -1:
        content = content[:tg_start] + tg_new + content[tg_end:]

    # 5. Testimonials (Let's replace the whole testi-track)
    testi_new = """<div class="testi-track" id="testiTrack">
          <!-- T1 -->
          <div class="testi-col">
            <div class="testi-card">
              <div class="stars">
                <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-half"></i>
              </div>
              <div class="testi-quote">"The best 21 days! I lost 4 kgs and learned so much about food."</div>
              <div class="testi-author">
                <div class="testi-name">Aditi S.</div>
                <div class="testi-meta">Lost 4kg &bull; Plan: PRO</div>
              </div>
            </div>
          </div>
          <!-- T2 -->
          <div class="testi-col">
            <div class="testi-card" style="box-shadow: 0 8px 30px rgba(0,0,0,0.1); border-color:var(--saffron);">
              <div class="stars">
                <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
              </div>
              <div class="testi-quote">"My energy is through the roof. The daily live sessions are incredible."</div>
              <div class="testi-author">
                <div class="testi-name">Vikram M.</div>
                <div class="testi-meta">Lost 5kg &bull; Plan: PREMIUM</div>
              </div>
            </div>
          </div>
          <!-- T3 -->
          <div class="testi-col">
            <div class="testi-card">
              <div class="stars">
                <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
              </div>
              <div class="testi-quote">"The skin program actually works. The detox drinks totally cleared my skin."</div>
              <div class="testi-author">
                <div class="testi-name">Meera P.</div>
                <div class="testi-meta">Glowing Skin &bull; Plan: SKIN PROGRAM</div>
              </div>
            </div>
          </div>
          <!-- T4 -->
          <div class="testi-col">
            <div class="testi-card">
              <div class="stars">
                <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-half"></i>
              </div>
              <div class="testi-quote">"I never thought gaining weight naturally was possible. Highly recommended."</div>
              <div class="testi-author">
                <div class="testi-name">Karan R.</div>
                <div class="testi-meta">Gained 6kg &bull; Plan: WEIGHT GAIN</div>
              </div>
            </div>
          </div>
"""
    testi_start = content.find('<div class="testi-track" id="testiTrack">')
    testi_end = content.find('</div>\n      </div>\n\n      <!-- Control Dots -->', testi_start)
    if testi_start != -1 and testi_end != -1:
        content = content[:testi_start] + testi_new + content[testi_end:]


    # 6. FAQ Section Text Update (Regex fine-tuning or replace file block)
    # 7. Final CTA Section Update
    # For CTA, let's locate <section id="final-cta" ...>
    cta_new = """  <!-- FINAL CTA -->
  <section id="final-cta" class="sec" style="background:var(--forest); color: white;">
    <div class="container position-relative text-center">
      <h2 class="sec-h2" style="color:white; font-size:42px;">Your Health Is Your Greatest Wealth</h2>
      <p style="font-size:18px; opacity:0.9; margin-bottom: 24px;">Lose 3–5kg in 21 days with home workouts & Indian food.</p>
      <button class="btn-cta fade-up" onclick="scrollToPlans()">Start My 21-Day Transformation <i class="bi bi-arrow-right"></i></button>
      <p style="font-size:14px; opacity:0.7; margin-top:20px; font-weight:600;"><i class="bi bi-clock-history"></i> 12,000+ transformed &bull; Limited slots left</p>
    </div>
  </section>"""
    cta_start = content.find('<section id="final-cta"')
    cta_end = content.find('</section>', cta_start) + 10
    if cta_start != -1 and cta_end != -1:
        content = content[:cta_start] + cta_new + content[cta_end:]

    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_file()
