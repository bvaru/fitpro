import re

def check_and_save(content, filename):
    if len(content) < 50000:
        print("ERROR: Result length too small, something was truncated!")
        return False
    if "</html>" not in content.lower():
        print("ERROR: Corrupted document, missing </html>.")
        return False
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: File updated safely.")
    return True

def override_file2():
    filepath = 'templates/index.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 4. Transformations Replacement
    tg_new = """<div class="tg-track" id="tgTrack">

          <!-- Card 1: Founder -->
          <div class="tg-card">
            <div class="tg-img">
              <img src="/static/images/owner.jpeg" alt="Founder Transformation" onerror="this.src='/static/images/client0.jpeg'" style="object-fit:cover;" />
            </div>
            <div class="tg-body">
              <div class="tg-name">Founder's Story</div>
              <div class="tg-detail">"Started my own transformation journey. Created this simple effective Indian home plan."</div>
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
              <div class="tg-detail">"Lost 15kg in just three rounds of 21 days using the guided home workouts and Indian meals."</div>
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
              <div class="tg-detail">"Developed healthy eating habits and became active again. No strict diet, just right food!"</div>
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
              <div class="tg-detail">"Cleared my acne entirely simply by changing my food intake based on nutrition education alone."</div>
              <div class="tg-chip"><i class="bi bi-award-fill"></i> Clear Skin &bull; Plan: SKIN PROGRAM</div>
            </div>
          </div>

          <!-- Card 5: Weight Gain -->
          <div class="tg-card">
            <div class="tg-img">
              <img src="/static/images/client7.jpeg" alt="Transformation" onerror="this.src='/static/images/client8.jpeg'" />
            </div>
            <div class="tg-body">
              <div class="tg-name">Rahul K.</div>
              <div class="tg-detail">"Gaining healthy weight was hard until the coach showed me the right meal portions."</div>
              <div class="tg-chip"><i class="bi bi-award-fill"></i> Gained 8kg &bull; Plan: WEIGHT GAIN</div>
            </div>
          </div>
"""
    
    tg_match = re.search(r'<div class="tg-track" id="tgTrack">.*?</div>\s*</div>\s*<!-- ── Card 1 ── -->', content, re.DOTALL)
    # the existing cards are inside tg-track. Let's just use regex to replace `<div class="tg-track" id="tgTrack">` up to its matching `</div>` before `<div class="tg-nav">`
    # or just replace using str logic
    
    tg_start = content.find('<div class="tg-track" id="tgTrack">')
    if tg_start != -1:
        # assume the tg-track ends before the tg-counter or just before the generic close </div> </div>
        # actually, the track ends with `<!-- /tg-track -->` if commented, but it wasn't.
        # it ends right before `</div>\n      </div>\n\n      <div class="tg-nav">` actually wait, tg-nav is BEFORE tg-scroll.
        # let's look at the file: `<div class="tg-scroll" id="tgScroll">\n        <div class="tg-track" id="tgTrack">` ... ends ... `        </div>\n      </div>`
        # then testimonials starts.
        # Just search for `</section>` of transformations.
        sec_trans = content.find('</section>', tg_start)
        # the track end is right before `</div>\n      </div>\n    </div>\n  </section>`
        track_end = content.rfind('</div>', tg_start, sec_trans - 10) # last div inside section
        track_end = content.rfind('</div>', tg_start, track_end - 1) # second to last div
        if track_end != -1:
            content = content[:tg_start] + tg_new + content[track_end:]
    
    # 5. Testimonials
    testi_new = """<div class="testi-track" id="testiTrack">
          <!-- T1 -->
          <div class="testi-col">
            <div class="testi-card">
              <div class="stars">
                <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-half"></i>
              </div>
              <div class="testi-quote">"The best 21 days! I lost 4 kgs and learned so much about food. Highly recommend PRO."</div>
              <div class="testi-author">
                <div class="testi-av av-g">A</div>
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
                <div class="testi-av av-r">V</div>
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
                <div class="testi-av av-a">M</div>
                <div class="testi-name">Meera P.</div>
                <div class="testi-meta">Clear Skin &bull; Plan: SKIN PROGRAM</div>
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
                <div class="testi-av av-g">K</div>
                <div class="testi-name">Karan R.</div>
                <div class="testi-meta">Gained 6kg &bull; Plan: WEIGHT GAIN</div>
              </div>
            </div>
          </div>
"""
    test_start = content.find('<div class="testi-track"')
    if test_start != -1:
        test_sec_end = content.find('</section>', test_start)
        test_track_end = content.rfind('</div>', test_start, test_sec_end - 5)
        test_track_end = content.rfind('</div>', test_start, test_track_end - 1)
        if test_track_end != -1:
            content = content[:test_start] + testi_new + content[test_track_end:]
            
    # 6 & 7. FAQ CTA Update and CTA Section
    # Let's find FAQ accordion end
    faq_end_idx = content.find('</div><!-- /accordion -->')
    if faq_end_idx != -1:
        faq_cta = """\n      <div class="text-center mt-5"><button class="btn-hero" onclick="scrollToPlans()">Start Transformation Journey</button></div>\n      """
        content = content[:faq_end_idx] + '</div><!-- /accordion -->' + faq_cta + content[faq_end_idx+25:]
        
    cta_new = """  <!-- FINAL CTA -->
  <section id="final-cta" class="sec" style="background:var(--forest); color: white;">
    <div class="container position-relative text-center">
      <h2 class="sec-h2" style="color:white; font-size:42px;">Your Health Is Your Greatest Wealth</h2>
      <p style="font-size:18px; opacity:0.9; margin-bottom: 24px;">Lose 3–5kg in 21 days with home workouts & Indian food.</p>
      <button class="btn-cta fade-up" onclick="scrollToPlans()">Start My 21-Day Transformation <i class="bi bi-arrow-right"></i></button>
      <p style="font-size:14px; opacity:0.7; margin-top:20px; font-weight:600;"><i class="bi bi-clock-history"></i> 12,000+ transformed &bull; Limited slots left</p>
    </div>
  </section>"""
  
    cta_start = content.find('<section id="contact"')
    if cta_start != -1:
        content = content[:cta_start] + cta_new + "\n\n  " + content[cta_start:]

    check_and_save(content, filepath)

if __name__ == "__main__":
    override_file2()
