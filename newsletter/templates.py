# newsletter/templates.py
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def render_newsletter(data):
    """
    Render newsletter template with backward compatibility.
    Accepts:
      - data as a dict with keys: featured, stories, events, quick_hits, etc.
      - OR data as a list of articles (legacy support)
    Returns rendered HTML (string).
    """
    # Normalize input
    featured = None
    stories = []
    events = []
    quick_hits = []
    trending_tools = []
    highlights = []
    sponsored_content = None
    
    if isinstance(data, dict):
        featured = data.get("featured")
        stories = data.get("stories") or []
        events = data.get("events") or []
        quick_hits = data.get("quick_hits") or []
        trending_tools = data.get("trending_tools") or []
        highlights = data.get("highlights") or []
        sponsored_content = data.get("sponsored_content")
    elif isinstance(data, list):
        # Legacy: treat first item as featured, rest as stories
        if len(data) > 0:
            featured = data[0]
            stories = data[1:]
    else:
        stories = []

    # If no featured but we have stories, promote first story
    if not featured and stories:
        featured = stories.pop(0)

    # Ensure fields exist
    def assure_fields(item):
        if item is None:
            return None
        item.setdefault("title", "Untitled")
        item.setdefault("url", "#")
        item.setdefault("link", item.get("url", "#"))
        item.setdefault("summary", "")
        item.setdefault("image", "https://via.placeholder.com/1200x630/667eea/ffffff?text=AI+News")
        item.setdefault("source", "AI NEWS")
        item.setdefault("published_date", datetime.now().strftime("%b %d, %Y"))
        return item

    featured = assure_fields(featured)
    stories = [assure_fields(s) for s in stories]
    events = [assure_fields(e) for e in events]
    
    # Convert stories to featured_articles format (top 3)
    featured_articles = [featured] + stories if featured else stories
    featured_articles = featured_articles[:3]
    
    # If we have more stories, convert to quick_hits
    if len(stories) > 2 and not quick_hits:
        quick_hits = [
            {
                "title": s.get("title", ""),
                "link": s.get("link", s.get("url", "#")),
                "summary": s.get("summary", "")[:150] + "..."
            }
            for s in stories[2:6]
        ]
    
    # Convert events to highlights if they exist
    if events and not highlights:
        highlights = [
            {
                "icon": "📅",
                "title": e.get("title", ""),
                "link": e.get("link", e.get("url", "#"))
            }
            for e in events
        ]
    
    # Determine time of day
    current_hour = datetime.now().hour
    if current_hour < 12:
        time_of_day = "morning"
    elif current_hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("newsletter.html")

    return template.render(
        # Legacy support
        featured=featured,
        stories=stories,
        events=events,
        date=datetime.now().strftime("%B %d, %Y"),
        year=datetime.now().year,
        
        # New template variables
        newsletter_title="CSE(AI&ML) Weekly Newsletter",
        current_date=datetime.now().strftime("%A, %B %d, %Y"),
        time_of_day=time_of_day,
        recipient_name=data.get("recipient_name", "Student") if isinstance(data, dict) else "Student",
        featured_articles=featured_articles,
        quick_hits=quick_hits,
        trending_tools=trending_tools,
        highlights=highlights,
        sponsored_content=sponsored_content,
        feedback_url=data.get("feedback_url", "#") if isinstance(data, dict) else "#",
        total_views=data.get("total_views", 0) if isinstance(data, dict) else 0,
        avg_rating=data.get("avg_rating", 0.0) if isinstance(data, dict) else 0.0,
        unsubscribe_url=data.get("unsubscribe_url", "#") if isinstance(data, dict) else "#",
        preferences_url=data.get("preferences_url", "#") if isinstance(data, dict) else "#",
        archive_url=data.get("archive_url", "#") if isinstance(data, dict) else "#",
        team_signature=data.get("team_signature", "CSE(AI&ML) Team") if isinstance(data, dict) else "CSE(AI&ML) Team"
    )
