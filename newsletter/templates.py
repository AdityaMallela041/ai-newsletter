# newsletter/templates.py
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def render_newsletter(data):
    """
    Render newsletter with all data including trending tools
    """
    
    # Extract single articles (not lists)
    development = data.get("development")
    training = data.get("training")
    research = data.get("research")
    startup = data.get("startup")
    trending_tools = data.get("trending_tools", [])  # ADD THIS LINE
    
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
    
    # Load template
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("newsletter.html")
    
    return template.render(
        # Header
        newsletter_title="CSE(AI&ML) Weekly Newsletter",
        current_date=datetime.now().strftime("%A, %B %d, %Y"),
        time_of_day=time_of_day,
        recipient_name=data.get("recipient_name", "Student"),
        
        # Summary
        total_articles=total_articles,
        video_count=video_count,
        
        # Single articles per category
        development=development,
        training=training,
        research=research,
        startup=startup,
        trending_tools=trending_tools,  # ADD THIS LINE
        
        # Metadata
        feedback_url=data.get("feedback_url", "#"),
        newsletter_id=data.get("newsletter_id", 0),
        unsubscribe_url=data.get("unsubscribe_url", "#"),
        preferences_url=data.get("preferences_url", "#"),
        archive_url=data.get("archive_url", "#"),
        year=datetime.now().year
    )
