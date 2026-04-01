import re
import os

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

def override_file():
    filepath = 'templates/index.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Hero
    content = re.sub(
        r'<h1 class="hero-h1 fade-up">Lose <BR><em>3-5kg in 21Days </em><br>Without gym or Without missing your favorite food</h1>',
        r'<h1 class="hero-h1 fade-up">Lose <br><em>3-5kg in 21 Days </em><br>with Home Workouts &amp; Indian Diet</h1>',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'<p class="hero-sub fade-up fd1">A 21-day natural weight loss program using home food and home workouts,\s*guided by effective practical and secret methods to help you achieve your ideal body shape.</p>',
        r'<p class="hero-sub fade-up fd1">A 21-day natural weight loss program using home food and home workouts, guided by effective practical and secret methods to help you achieve your ideal body shape.</p>',
        content
    )
    
    # Hero Carousel video
    video_html = """                  <!-- Video Slide -->
                  <div class="carousel-slide active">
                    <video src="/static/images/Video.mp4" autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover; object-position:center top; display:block;"></video>
                  </div>

                  <!-- Slide 1 — ✏️ src="/static/images/hero1.jpeg" -->
                  <div class="carousel-slide">"""
    
    content = content.replace(
        """                  <!-- Slide 1 — ✏️ src="/static/images/hero1.jpeg" -->
                  <div class="carousel-slide active">""",
        video_html
    )

    # 2. Add to How It Works
    hw_addition = """
          <div class="hw-col zoom-in fd1">
            <div class="feat-card" style="display:flex; flex-direction:column;">
              <img src="/static/images/education.jpeg" alt="Nutrition Education" style="width:100%; height:160px; object-fit:cover; border-radius:12px; margin-bottom:24px;" onerror="this.src='https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=900&q=80&fit=crop'" />
              <div class="feat-h">Nutrition Education</div>
              <div class="feat-p">Learn the science of eating right to sustain your results for life.</div>
            </div>
          </div>
          <div class="hw-col zoom-in fd2">
            <div class="feat-card" style="display:flex; flex-direction:column;">
              <img src="/static/images/proven_results.png" alt="Health Talk" style="width:100%; height:160px; object-fit:contain; margin-bottom:24px; mix-blend-mode:multiply;" onerror="this.src='https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=900&q=80&fit=crop'" />
              <div class="feat-h">Health Talk</div>
              <div class="feat-p">Every day live class at 8 pm – 8:30 pm. The right food education to transform your body.</div>
            </div>
          </div>
        </div>
      </div>"""
    
    hw_target = re.search(r'<div class="feat-p">100% natural weight management\. No powdered products or artificial supplements\.</div>.*?</div>.*?</div>.*?</div>.*?</div>', content, re.DOTALL)
    if hw_target:
        new_hw = hw_target.group(0).replace("        </div>\n      </div>", hw_addition).replace("        </div>\r\n      </div>", hw_addition)
        content = content.replace(hw_target.group(0), new_hw)

    # 3. Replace Pricing Area
    with open('tmp_pricing.html', 'r', encoding='utf-8') as f2:
        pricing_html = f2.read()
        
    start_str = '<div class="row g-4 justify-content-center">'
    end_str = '<!-- TRANSFORMATIONS -->'
    
    sec_idx = content.find('<section id="plans"')
    if sec_idx != -1:
        s_idx = content.find(start_str, sec_idx)
        e_idx = content.find(end_str, sec_idx)
        
        # We need to backtrack from end_str to find the closing </section>
        close_sec = content.rfind('</section>', s_idx, e_idx)
        
        if s_idx != -1 and close_sec != -1:
            # Reconstruct the section end correctly:
            # We replace everything from `s_idx` to `close_sec` with our pricing HTML + `    </div>\n  ` 
            content = content[:s_idx] + pricing_html + "\n    </div>\n  " + content[close_sec:]

    check_and_save(content, filepath)

if __name__ == "__main__":
    override_file()
