# newsletter/pipeline.py

import os
import shutil
import re
import base64
import urllib.parse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from premailer import Premailer
from dotenv import load_dotenv

from newsletter.fetcher import fetch_articles
from newsletter.summarizer import summarize_with_groq
from newsletter.emailer import send_email
from newsletter.database import save_newsletter, log_newsletter_sent, init_db

load_dotenv()


def convert_image_to_base64(image_path):
    """Convert local image to base64 for email embedding"""
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


def convert_youtube_iframes_to_thumbnails(html_content):
    """Replace YouTube iframe embeds with FULL-WIDTH clickable thumbnails"""
    iframe_pattern = r'<iframe[^>]*src=["\']https://www\.youtube\.com/embed/([^"\']+)["\'][^>]*>.*?</iframe>'
    
    def replace_with_thumbnail(match):
        video_id = match.group(1).split('?')[0]
        
        return f'''
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 20px 0;">
    <tr>
        <td style="padding: 0;">
            <a href="https://www.youtube.com/watch?v={video_id}" target="_blank" style="display: block; text-decoration: none;">
                <div style="position: relative; width: 100%; padding-bottom: 56.25%; background-color: #000; border-radius: 8px; overflow: hidden;">
                    <img src="https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg" 
                         alt="YouTube Video" 
                         style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; display: block; border: 0;">
                    
                    <table cellpadding="0" cellspacing="0" border="0" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80px; height: 56px; z-index: 10;">
                        <tr>
                            <td style="background-color: rgba(255, 0, 0, 0.9); border-radius: 14px; text-align: center; vertical-align: middle;">
                                <svg width="80" height="56" viewBox="0 0 80 56" style="display: block;">
                                    <polygon points="30,18 50,28 30,38" fill="#ffffff" style="fill: #ffffff;"/>
                                </svg>
                            </td>
                        </tr>
                    </table>
                </div>
                
                <div style="text-align: center; margin-top: 15px; padding: 0 10px;">
                    <span style="color: #3b82f6; font-size: 15px; font-weight: 700; font-family: Arial, Helvetica, sans-serif;">
                        ▶ Click to Watch on YouTube
                    </span>
                </div>
            </a>
        </td>
    </tr>
</table>
        '''
    
    html_content = re.sub(iframe_pattern, replace_with_thumbnail, html_content, flags=re.DOTALL)
    return html_content


def inline_css_for_email(html_content):
    """Use Premailer to inline CSS for email compatibility"""
    try:
        premailer = Premailer(
            html_content,
            strip_important=False,
            keep_style_tags=True,
            remove_classes=False,
            capitalize_float_margin=True
        )
        return premailer.transform()
    except Exception as e:
        print(f"⚠️  Error inlining CSS: {e}")
        return html_content


def generate_feedback_url(newsletter_id: int, recipient_email: str) -> str:
    """Generate personalized feedback URL for each recipient"""
    base_url = os.getenv('FEEDBACK_API_URL', 'http://localhost:8000')
    params = {
        'newsletter_id': newsletter_id,
        'email': recipient_email
    }
    return f"{base_url}/feedback?{urllib.parse.urlencode(params)}"


def get_time_of_day():
    """Get time of day greeting"""
    hour = datetime.now().hour
    if hour < 12:
        return 'morning'
    elif hour < 17:
        return 'afternoon'
    else:
        return 'evening'


def main():
    """Main pipeline to generate newsletter"""
    
    print("\n" + "="*60)
    print("🤖 VBIT AI NEWSLETTER GENERATOR - v8.0")
    print("="*60 + "\n")
    
    # Initialize database
    init_db()
    
    # Step 1: Fetch content
    print("📥 Step 1: Fetching latest AI & ML content...")
    articles = fetch_articles()
    print(f"✅ Fetched content from categories\n")
    
    # Step 2: Summarize articles
    print("📝 Step 2: Generating summaries with AI...")
    skip_keys = ['total_articles', 'video_count', 'tools']
    
    for category, article in articles.items():
        if category in skip_keys or not isinstance(article, dict) or isinstance(article, list):
            continue
        
        if article and 'content' in article:
            print(f"   → Summarizing {category}...")
            summary = summarize_with_groq(article['content'], category)
            article['summary'] = summary if summary else article['content'][:200] + "..."
    
    print(f"✅ Summaries generated\n")
    
    # Step 3: Generate HTML template
    print("🎨 Step 3: Generating VBIT-branded newsletter...")
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('newsletter.html')
    
    current_date = datetime.now().strftime('%B %d, %Y')
    
    # Base template data (without feedback_url yet)
    base_template_data = {
        'newsletter_title': 'AI & ML Weekly Newsletter',
        'current_date': current_date,
        'time_of_day': get_time_of_day(),
        'recipient_name': 'Student',
        'development': articles.get('development'),
        'training': articles.get('training'),
        'research': articles.get('research'),
        'tools': articles.get('tools', []),
        'startup': articles.get('startup'),
        'newsletter_id': datetime.now().strftime('%Y%m%d'),
        'unsubscribe_url': '#',
        'preferences_url': '#',
        'archive_url': '#',
        'year': datetime.now().year,
        'feedback_url': ''  # Placeholder for now
    }
    
    # Render base HTML (for database storage)
    base_html_content = template.render(**base_template_data)
    print(f"✅ Newsletter HTML generated\n")
    
    # Step 4: Embed logo
    print("🖼️  Step 4: Embedding logo as base64...")
    html_with_logo = embed_local_images(base_html_content)
    print(f"✅ Logo embedded\n")
    
    # Step 5: Convert YouTube videos
    print("📺 Step 5: Converting YouTube videos to full-width thumbnails...")
    html_with_thumbnails = convert_youtube_iframes_to_thumbnails(html_with_logo)
    print(f"✅ YouTube videos converted\n")
    
    # Step 6: Inline CSS
    print("🔧 Step 6: Inlining CSS for email compatibility...")
    base_final_html = inline_css_for_email(html_with_thumbnails)
    print(f"✅ CSS inlined\n")
    
    # Step 7: Save to output folder
    print("💾 Step 7: Saving newsletter...")
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'newsletter_{timestamp}.html')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(base_final_html)
    
    print(f"✅ Newsletter saved: {output_file}\n")
    
    # Copy CSS and assets
    css_src = os.path.join(template_dir, 'newsletter.css')
    css_dst = os.path.join(output_dir, 'newsletter.css')
    if os.path.exists(css_src):
        shutil.copy2(css_src, css_dst)
    
    assets_src = os.path.join(os.path.dirname(__file__), 'assets')
    assets_dst = os.path.join(output_dir, 'assets')
    if os.path.exists(assets_src):
        os.makedirs(assets_dst, exist_ok=True)
        for file in os.listdir(assets_src):
            src_file = os.path.join(assets_src, file)
            dst_file = os.path.join(assets_dst, file)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst_file)
    
    # Step 8: Save to database
    print("💾 Step 8: Saving to database...")
    newsletter_id = save_newsletter(
        title=base_template_data['newsletter_title'] + f" - {current_date}",
        content_html=base_final_html,
        created_by_email=os.getenv('ADMIN_EMAIL', 'system@vbit.edu')
    )
    
    if not newsletter_id:
        print("⚠️  Failed to save to database. Continuing anyway...\n")
        newsletter_id = int(datetime.now().strftime('%Y%m%d'))  # Fallback ID
    
    # Step 9: Send personalized emails with feedback URLs
    print("📧 Step 9: Sending personalized newsletters...")
    
    recipient_emails = os.getenv('RECIPIENT_EMAIL', '').split(',')
    recipient_emails = [email.strip() for email in recipient_emails if email.strip()]
    
    if recipient_emails:
        print(f"   Sending to {len(recipient_emails)} recipients...\n")
        
        for recipient_email in recipient_emails:
            # Generate personalized feedback URL
            feedback_url = generate_feedback_url(newsletter_id, recipient_email)
            
            # Update template data with personalized feedback URL
            personalized_data = base_template_data.copy()
            personalized_data['feedback_url'] = feedback_url
            
            # Render personalized HTML
            personalized_html = template.render(**personalized_data)
            
            # Apply all transformations
            personalized_html = embed_local_images(personalized_html)
            personalized_html = convert_youtube_iframes_to_thumbnails(personalized_html)
            personalized_html = inline_css_for_email(personalized_html)
            
            # Send email
            send_email(personalized_html, f"🤖 AI & ML Weekly - {current_date}")
        
        # Log newsletter as sent
        log_newsletter_sent(newsletter_id, recipient_emails)
        print("✅ Newsletter sent to all recipients!\n")
    else:
        print("⚠️  No recipients configured in .env\n")
    
    print("="*60)
    print("🎉 NEWSLETTER GENERATION COMPLETE!")
    print(f"📂 Output: {output_file}")
    print(f"🗄️  Database ID: {newsletter_id}")
    print("="*60 + "\n")
    
    return output_file


if __name__ == '__main__':
    main()
