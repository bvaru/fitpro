import re

path = 'templates/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''<section id="final-cta" class="sec"
    style="background:linear-gradient(180deg, rgba(255,252,253,.2) 0%, rgba(255,255,255,0) 100%), radial-gradient(circle at 16% 24%, rgba(225,29,72,.08) 0%, transparent 22%), radial-gradient(circle at 84% 76%, rgba(30,75,142,.08) 0%, transparent 24%); color: var(--ink);">
    <div class="container position-relative text-center">'''

replacement = '''<section id="final-cta" class="sec"
    style="position: relative; overflow: hidden; background:linear-gradient(180deg, rgba(255,252,253,.2) 0%, rgba(255,255,255,0) 100%), radial-gradient(circle at 16% 24%, rgba(225,29,72,.08) 0%, transparent 22%), radial-gradient(circle at 84% 76%, rgba(30,75,142,.08) 0%, transparent 24%); color: var(--ink);">
    <img src="/static/images/cta_wellness_art.png" class="premium-art cta-art" alt="Wellness CTA Art" />
    <div class="container position-relative text-center">'''

content = content.replace(target, replacement)

# ensure we replace it even if whitespace differences
if "cta_wellness_art.png" not in content:
    content = re.sub(
        r'<section id="final-cta"[^>]+>\s*<div class="container position-relative text-center">',
        r'<section id="final-cta" class="sec" style="position: relative; overflow: hidden; background:linear-gradient(180deg, rgba(255,252,253,.2) 0%, rgba(255,255,255,0) 100%), radial-gradient(circle at 16% 24%, rgba(225,29,72,.08) 0%, transparent 22%), radial-gradient(circle at 84% 76%, rgba(30,75,142,.08) 0%, transparent 24%); color: var(--ink);">\n    <img src="/static/images/cta_wellness_art.png" class="premium-art cta-art" alt="Wellness CTA Art" />\n    <div class="container position-relative text-center">',
        content
    )

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
