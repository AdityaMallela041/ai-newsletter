# newsletter/templates.py

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def render_newsletter(data):
    """
    Render newsletter with all data including trending tools and feedback
    """
    
    # Extract single articles (not lists)
    development = data.get("development")
    training = data.get("training")
    research = data.get("research")
    startup = data.get("startup")
    tools = data.get("tools", [])
    
    print(f"🛠️ DEBUG: Tools passed to template: {len(tools)} tools")
    if tools:
        for i, t in enumerate(tools):
            print(f"   {i+1}. {t['name']}")
    
    # Count total
    articles = [development, training, research, startup]
    total_articles = sum(1 for a in articles if a)
    video_count = sum(1 for a in articles if a and a.get("video_id"))
    
    # Time-based greeting
    current_hour = datetime.now().hour
    if current_hour < 12:
        time_of_day = "morning"
    elif current_hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"
    
    # Get feedback URL from environment
    FEEDBACK_API_URL = os.getenv("FEEDBACK_API_URL", "http://localhost:8000/feedback")
    
    # Newsletter ID (you can generate this dynamically)
    newsletter_id = data.get("newsletter_id", 1)
    
    # Recipient email (this should come from your email list)
    recipient_email = data.get("recipient_email", "user@example.com")
    
    # Load template
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("newsletter.html")
    
    return template.render(
        # Header
        newsletter_title="CSE(AI&ML) Weekly Newsletter",
        current_date=datetime.now().strftime("%B %d, %Y"),
        time_of_day=time_of_day,
        recipient_name=data.get("recipient_name", ""),
        
        # Summary
        total_articles=total_articles,
        video_count=video_count,
        
        # Single articles per category
        development=development,
        training=training,
        research=research,
        startup=startup,
        tools=tools,
        
        # Feedback metadata
        feedback_url=FEEDBACK_API_URL,
        newsletter_id=newsletter_id,
        recipient_email=recipient_email,
        
        # Footer links
        unsubscribe_url=data.get("unsubscribe_url", "#"),
        preferences_url=data.get("preferences_url", "#"),
        archive_url=data.get("archive_url", "#"),
        year=datetime.now().year
    )
