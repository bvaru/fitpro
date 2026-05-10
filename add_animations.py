import re

path = 'templates/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add animation and floating
content = content.replace('.premium-art {', '''.premium-art {
      animation: wellnessSketchFloat 15s ease-in-out infinite;
      transition: opacity 1s ease, transform 1s ease;''')

content = content.replace('class="premium-art ', 'class="premium-art fade-up ')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
