# newsletter/templates.py
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def render_newsletter(data):
    """Render newsletter with categorized content"""
    
    # Extract categories
    developments = data.get("developments") or []
    training = data.get("training") or []
    research = data.get("research") or []
    tools = data.get("tools") or []
    startups = data.get("startups") or []
    
    # Determine time of day
    current_hour = datetime.now().hour
    if current_hour < 12:
        time_of_day = "morning"
    elif current_hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"
    
    # Calculate total articles for summary
    total_articles = len(developments) + len(training) + len(research) + len(tools) + len(startups)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("newsletter.html")

    return template.render(
        newsletter_title="CSE(AI&ML) Weekly Newsletter",
        current_date=datetime.now().strftime("%A, %B %d, %Y"),
        time_of_day=time_of_day,
        recipient_name=data.get("recipient_name", "Student"),
        
        # Categorized content
        developments=developments,
        training=training,
        research=research,
        tools=tools,
        startups=startups,
        total_articles=total_articles,
        
        # Metadata
        feedback_url=data.get("feedback_url", "#"),
        newsletter_id=data.get("newsletter_id", 0),
        unsubscribe_url=data.get("unsubscribe_url", "#"),
        preferences_url=data.get("preferences_url", "#"),
        archive_url=data.get("archive_url", "#"),
        team_signature="CSE(AI&ML) Newsletter Team"
    )
