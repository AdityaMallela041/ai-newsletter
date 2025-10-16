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
        print(f"⚠️ Error converting image: {e}")
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
    """ENHANCED: Replace YouTube iframe embeds with FULL-WIDTH clickable thumbnails"""
    
    # Pattern 1: Standard iframe embeds
    iframe_pattern = r'<iframe[^>]*src=["\']https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})[^"\']*["\'][^>]*>.*?</iframe>'
    
    def replace_with_thumbnail(match):
        video_id = match.group(1)
        return f'''
        <a href="https://www.youtube.com/watch?v={video_id}" 
           style="display: block; text-align: center; text-decoration: none; margin: 20px 0;">
            <img src="https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg" 
                 alt="YouTube Video" 
                 style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="margin-top: 12px; color: #667eea; font-weight: 600; font-size: 16px;">
                ▶ Click to Watch on YouTube
            </p>
        </a>
        '''
    
    html_content = re.sub(iframe_pattern, replace_with_thumbnail, html_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Pattern 2: Handle embed URLs that might be in different formats
    embed_link_pattern = r'<a[^>]*href=["\']https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})[^"\']*["\'][^>]*>.*?</a>'
    html_content = re.sub(embed_link_pattern, replace_with_thumbnail, html_content, flags=re.IGNORECASE | re.DOTALL)
    
    return html_content


def generate_newsletter():
    """
    Generate newsletter HTML from fetched articles
    """
    print("🚀 Starting Newsletter Generation Pipeline...")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    # Fetch articles
    print("\n📰 Fetching curated AI/ML content...")
    articles = fetch_articles()
    
    if not articles or articles.get("total_articles", 0) == 0:
        print("❌ No articles fetched. Aborting newsletter generation.")
        return None, None
    
    # Summarize articles
    print("\n🤖 Generating AI summaries...")
    for category in ["development", "training", "research", "startup"]:
        article = articles.get(category)
        if article and isinstance(article, dict):
            content = article.get("content", "")
            if content:
                print(f"   📝 Summarizing {category}...")
                summary = summarize_with_groq(content, category=category)
                if summary:
                    article["summary"] = summary
                else:
                    article["summary"] = f"<p>{content[:180]}...</p>"
    
    # Render HTML template
    print("\n📄 Rendering newsletter template...")
    project_root = os.path.dirname(os.path.dirname(__file__))
    template_dir = os.path.join(project_root, 'newsletter', 'templates')
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('newsletter.html')
    
    # Prepare template data
    now = datetime.now()
    hour = now.hour
    
    if hour < 12:
        time_of_day = "Morning"
    elif hour < 17:
        time_of_day = "Afternoon"
    else:
        time_of_day = "Evening"
    
    # Save newsletter to database FIRST to get newsletter_id
    print("\n💾 Saving to database...")
    newsletter_id = save_newsletter(
        title='Weekly AI & ML Insights',
        content_html="<p>Generating...</p>",  # Temporary content
        created_by_email="system@vbit.edu"
    )
    
    if newsletter_id:
        print(f"   ✅ Newsletter ID: {newsletter_id}")
    else:
        print("   ⚠️ Could not save to database, using ID 1")
        newsletter_id = 1
    
    # Generate feedback URLs with newsletter_id and recipient_email
    base_feedback_url = os.getenv('FEEDBACK_API_URL', 'http://localhost:8000/feedback')
    recipient_email = os.getenv('RECIPIENT_EMAIL', 'test@example.com').split(',')[0].strip()
    
    # Create complete feedback URL with parameters
    feedback_url = f"{base_feedback_url}?newsletter_id={newsletter_id}&email={urllib.parse.quote(recipient_email)}"
    
    template_data = {
        'newsletter_title': 'Weekly AI & ML Insights',
        'current_date': now.strftime('%B %d, %Y'),
        'time_of_day': time_of_day,
        'year': now.year,
        'newsletter_id': newsletter_id,
        'recipient_email': recipient_email,
        'development': articles.get('development'),
        'training': articles.get('training'),
        'research': articles.get('research'),
        'startup': articles.get('startup'),
        'tools': articles.get('tools', []),
        'feedback_url': feedback_url,  # Complete feedback URL with parameters
        'unsubscribe_url': os.getenv('UNSUBSCRIBE_URL', '#'),
        'preferences_url': os.getenv('PREFERENCES_URL', '#'),
        'archive_url': os.getenv('ARCHIVE_URL', '#'),
    }
    
    html_content = template.render(**template_data)
    
    # Convert YouTube iframes to thumbnails
    print("   🎥 Converting YouTube embeds...")
    html_content = convert_youtube_iframes_to_thumbnails(html_content)
    
    # Embed local images
    print("   🖼️ Embedding local images...")
    html_content = embed_local_images(html_content)
    
    # Inline CSS for email compatibility
    print("   🎨 Inlining CSS...")
    try:
        premailer = Premailer(html_content, strip_important=False)
        html_content = premailer.transform()
    except Exception as e:
        print(f"   ⚠️ CSS inlining warning: {e}")
    
    # Save to output directory
    output_dir = os.path.join(project_root, 'newsletter', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f'newsletter_{timestamp}.html')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"   ✅ Newsletter saved: {output_path}")
    
    # Update newsletter in database with actual HTML content
    try:
        from newsletter.database import SessionLocal, Newsletter
        session = SessionLocal()
        newsletter = session.query(Newsletter).filter_by(newsletter_id=newsletter_id).first()
        if newsletter:
            newsletter.content_html = html_content
            session.commit()
            print(f"   ✅ Database updated with final HTML")
        session.close()
    except Exception as e:
        print(f"   ⚠️ Could not update database: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Newsletter generation complete!")
    print(f"📧 Feedback URL: {feedback_url}&rating=5")  # Example with 5 stars
    
    return html_content, newsletter_id


def send_newsletter():
    """
    Generate and send newsletter via email
    """
    result = generate_newsletter()
    
    if not result or result[0] is None:
        print("❌ Failed to generate newsletter")
        return False
    
    html_content, newsletter_id = result
    
    # Check if sending is enabled
    send_email_flag = os.getenv("SEND_EMAIL", "false").lower() == "true"
    
    if not send_email_flag:
        print("\n⚠️ Email sending is disabled (SEND_EMAIL=false)")
        print("   To enable, set SEND_EMAIL=true in .env")
        return True
    
    print("\n📧 Sending newsletter...")
    
    subject = f"🤖 AI Newsletter - {datetime.now().strftime('%B %d, %Y')}"
    success = send_email(html_content, subject)
    
    if success and newsletter_id:
        recipient_emails = [email.strip() for email in os.getenv("RECIPIENT_EMAIL", "").split(",") if email.strip()]
        try:
            log_newsletter_sent(
                newsletter_id=newsletter_id,
                recipient_emails=recipient_emails,
                status="sent"
            )
            print("✅ Newsletter sent successfully!")
        except Exception as e:
            print(f"⚠️ Email sent but logging failed: {e}")
    else:
        print("❌ Failed to send newsletter")
    
    return success


if __name__ == "__main__":
    send_newsletter()
