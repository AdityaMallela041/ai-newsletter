# fix_newsletter_template.py
import re

with open('newsletter/templates/newsletter.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all instances of summary_html with summary
content = content.replace('{{ development.summary_html | safe }}', '{{ development.summary }}')
content = content.replace('{{ training.summary_html | safe }}', '{{ training.summary }}')
content = content.replace('{{ research.summary_html | safe }}', '{{ research.summary }}')
content = content.replace('{{ startup.summary_html | safe }}', '{{ startup.summary }}')

with open('newsletter/templates/newsletter.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed newsletter.html - Changed summary_html → summary")
