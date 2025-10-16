# newsletter/pipeline.py

import os
import shutil
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from newsletter.fetcher import fetch_articles
from newsletter.summarizer import summarize_with_groq
from newsletter.emailer import send_email
from newsletter.database import save_newsletter


def convert_image_to_base64(image_path):
    """Convert local image to base64 for email embedding"""
    import base64
    try:
        with open(image_path, 'rb') as img_file:
            encoded = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded}"
    except Exception as e:
        print(f"⚠️  Error converting image: {e}")
        return None


def embed_local_images(html_content):
    """Convert local image paths to base64 for email compatibility"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    assets_path = os.path.join(project_root, 'newsletter', 'assets', 'vbit_logo.jpg')
    
    if os.path.exists(assets_path):
        base64_img = convert_image_to_base64(assets_path)
        if base64_img:
            html_content = html_content.replace('../assets/vbit_logo.jpg', base64_img)
            html_content = html_content.replace('assets/vbit_logo.jpg', base64_img)
    
    return html_content


def read_css_file():
    """Read CSS file content"""
    css_path = os.path.join(os.path.dirname(__file__), 'templates', 'newsletter.css')
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️  Warning: CSS file not found at {css_path}")
        return ""


def generate_newsletter():
    """Main pipeline to generate newsletter"""
    
    print("\n" + "="*60)
    print("🤖 VBIT AI NEWSLETTER GENERATOR - v6.0")
    print("="*60 + "\n")
    
    # Step 1: Fetch content
    print("📥 Step 1: Fetching latest AI & ML content...")
    articles = fetch_articles()
    print(f"✅ Fetched content from categories\n")
    
    # Step 2: Summarize each article
    print("📝 Step 2: Generating summaries with AI...")
    skip_keys = ['total_articles', 'video_count']
    
    for category, article in articles.items():
        if category in skip_keys or not isinstance(article, dict):
            continue
        if isinstance(article, list):
            continue
        if article and 'content' in article:
            print(f"   → Summarizing {category}...")
            summary = summarize_with_groq(article['content'], category)
            if summary:
                article['summary'] = summary
            else:
                article['summary'] = article['content'][:200] + "..."
    
    print(f"✅ Summaries generated\n")
    
    # Step 3: Generate HTML
    print("🎨 Step 3: Generating VBIT-branded newsletter...")
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('newsletter.html')
    
    template_data = {
        'newsletter_title': 'AI & ML Weekly Newsletter',
        'current_date': datetime.now().strftime('%B %d, %Y'),
        'time_of_day': get_time_of_day(),
        'recipient_name': 'Student',
        'development': articles.get('development'),
        'training': articles.get('training'),
        'research': articles.get('research'),
        'trending_tools': articles.get('tools', []),
        'startup': articles.get('startup'),
        'feedback_url': 'https://vbit-feedback.example.com',
        'newsletter_id': datetime.now().strftime('%Y%m%d'),
        'unsubscribe_url': '#',
        'preferences_url': '#',
        'archive_url': '#',
        'year': datetime.now().year
    }
    
    html_content = template.render(**template_data)
    
    # Step 4: Embed logo as base64
    print("🖼️  Step 4: Embedding logo as base64...")
    html_with_logo = embed_local_images(html_content)
    
    # Step 5: Inline CSS for email
    print("🔧 Step 5: Inlining CSS for email compatibility...")
    css_content = read_css_file()
    
    # Add CSS to <head>
    if '<head>' in html_with_logo:
        final_html = html_with_logo.replace(
            '</head>',
            f'<style>\n{css_content}\n</style>\n</head>'
        )
    else:
        final_html = html_with_logo
    
    # Remove external CSS link
    import re
    final_html = re.sub(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', '', final_html)
    
    # Step 6: Save to output folder
    print("💾 Step 6: Saving newsletter...")
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'newsletter_{timestamp}.html')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ Newsletter saved: {output_file}\n")
    
    # Step 7: Copy CSS file to output (for development viewing)
    css_src = os.path.join(template_dir, 'newsletter.css')
    css_dst = os.path.join(output_dir, 'newsletter.css')
    if os.path.exists(css_src):
        shutil.copy2(css_src, css_dst)
        print(f"✅ CSS copied to output folder\n")
    
    # Step 8: Copy assets
    assets_src = os.path.join(os.path.dirname(__file__), 'assets')
    assets_dst = os.path.join(output_dir, 'assets')
    
    if os.path.exists(assets_src):
        os.makedirs(assets_dst, exist_ok=True)
        for file in os.listdir(assets_src):
            src_file = os.path.join(assets_src, file)
            dst_file = os.path.join(assets_dst, file)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst_file)
        print(f"✅ Assets copied to output folder\n")
    
    # Step 9: Save to database
    print("💾 Step 7: Saving to database...")
    try:
        newsletter_id = save_newsletter(
            title=template_data['newsletter_title'],
            content_html=final_html,
            created_by_email='system@vbit.edu',
            total_articles=articles.get('total_articles', 0)
        )
        print(f"✅ Saved to database (ID: {newsletter_id})\n")
    except Exception as e:
        print(f"⚠️  Database save skipped: {e}\n")
    
    # Step 10: Send email (optional)
    if os.getenv('SEND_EMAIL', 'false').lower() == 'true':
        print("📧 Step 8: Sending newsletter via email...")
        try:
            send_email(final_html, template_data['newsletter_title'])
            print("✅ Newsletter sent!\n")
        except Exception as e:
            print(f"⚠️  Email sending failed: {e}\n")
    else:
        print("ℹ️  Email sending disabled (set SEND_EMAIL=true in .env to enable)\n")
    
    print("="*60)
    print("🎉 NEWSLETTER GENERATION COMPLETE!")
    print(f"📂 Output: {output_file}")
    print("="*60 + "\n")
    
    return output_file


def get_time_of_day():
    """Get time of day greeting"""
    hour = datetime.now().hour
    if hour < 12:
        return 'morning'
    elif hour < 17:
        return 'afternoon'
    else:
        return 'evening'


if __name__ == '__main__':
    generate_newsletter()
