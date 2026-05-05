import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the nav arrows and update the wrapper
old_header = """        <div>
          <div class="sec-overline">Testimonials</div>
          <h2 class="sec-h2" style="margin-bottom:0;">WHAT OUR <em>HEROES SAY</em></h2>
        </div>
        <div class="tg-nav" style="margin-top:0;">
          <button class="tg-arrow" onclick="testiScroll(-1)" aria-label="Previous"><i
              class="bi bi-chevron-left"></i></button>
          <button class="tg-arrow" onclick="testiScroll(1)" aria-label="Next"><i
              class="bi bi-chevron-right"></i></button>
        </div>
      </div>

      <div class="testi-scroll" id="testi-scroll">
        <div class="testi-track" id="testiTrack">"""

new_header = """        <div>
          <div class="sec-overline">Testimonials</div>
          <h2 class="sec-h2" style="margin-bottom:0;">WHAT OUR <em>HEROES SAY</em></h2>
        </div>
      </div>

      <div class="row align-items-stretch">"""

content = content.replace(old_header, new_header)

# 2. Replace column wrapper
content = content.replace('<div class="testi-col">', '<div class="col-md-6 col-lg-4 mb-4 d-flex flex-column">')

# 3. Replace card
content = content.replace('<div class="testi-card">', '<div class="testi-card d-flex flex-column h-100">')
content = content.replace('<div class="testi-card" style="box-shadow: 0 8px 30px rgba(0,0,0,0.1); border-color:var(--saffron);">', '<div class="testi-card d-flex flex-column h-100" style="box-shadow: 0 8px 30px rgba(0,0,0,0.1); border-color:var(--saffron);">')

# 4. Replace quote
content = content.replace('<div class="testi-quote">', '<div class="testi-quote flex-grow-1">')

# 5. Replace author
content = content.replace('<div class="testi-author">', '<div class="testi-author mt-auto flex-shrink-0">')

# 6. Replace ending wrapper
content = content.replace('        </div><!-- /testiTrack -->\n      </div>', '      </div><!-- /row -->')

# 7. Remove the script part
script_to_remove = """<script>
    document.addEventListener("DOMContentLoaded", () => {
      // Testimonials Arrows Fix
      const testiSection = document.getElementById("testimonials");
      if (testiSection && !document.getElementById("testi-nav-bottom")) {
        const topNav = testiSection.querySelector(".d-flex .tg-nav");
        if (topNav) topNav.style.display = "none";
        
        const navDiv = document.createElement("div");
        navDiv.id = "testi-nav-bottom";
        navDiv.className = "tg-nav fade-up visible";
        navDiv.style.marginTop = "30px";
        navDiv.innerHTML = `
          <button class="tg-arrow" onclick="testiScroll(-1)" aria-label="Previous"><i class="bi bi-chevron-left"></i></button>
          <button class="tg-arrow" onclick="testiScroll(1)" aria-label="Next"><i class="bi bi-chevron-right"></i></button>
        `;
        testiSection.querySelector(".container").appendChild(navDiv);
      }
    });
  </script>"""

if script_to_remove in content:
    content = content.replace(script_to_remove, '')
else:
    print("Script part not found exactly as string. Using regex or doing nothing.")
    
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done replacing.")
