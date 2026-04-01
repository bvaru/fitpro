import re

def update_file():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Update How It Works
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
      </div>
"""
    # Replace the end </div></div> for hw-stream
    target_hw = """              <div class="feat-p">100% natural weight management. No powdered products or artificial supplements.</div>
            </div>
          </div>
        </div>
      </div>"""
    content = content.replace(target_hw, target_hw.replace("        </div>\n      </div>", hw_addition))
    
    # 2. Re-write the pricing section
    with open('tmp_pricing.html', 'r', encoding='utf-8') as f2:
        pricing_html = f2.read()
        
    # find exactly <div class="row g-4 justify-content-center"> inside pricing section and replace until its closing tag.
    # We will use regex to find the Plans row
    
    # A bit hard to use regex for nested HTML, so we'll use string slicing instead.
    start_str = "      <div class=\"row g-4 justify-content-center\">"
    # Find start after `<section id="plans" class="sec">`
    sec_idx = content.find('<section id="plans"')
    start_idx = content.find(start_str, sec_idx)
    end_str = "<!-- TRANSFORMATIONS -->"
    end_idx = content.find(end_str, sec_idx)
    
    # The pricing block is roughly from start_idx up to end_idx, except some closing divs.
    # From start_idx to end_idx: there is the row, its closing </div>, the container closing </div>, and </section>.
    # Let's replace the whole interior of the container just to be safe.
    
    container_start = content.find('<div class="row g-4 justify-content-center">', sec_idx)
    container_end = content.find('    </div>\n  </section>', sec_idx)
    
    if container_start > 0 and container_end > container_start:
        content = content[:container_start] + pricing_html + content[container_end:]
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Updates completed.")

if __name__ == "__main__":
    update_file()
