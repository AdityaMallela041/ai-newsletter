# newsletter/templates.py
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def render_newsletter(data):
    """
    Render the newsletter template.
    Accepts:
      - data as a dict with keys: featured, stories, events
      - OR data as a list of articles (legacy)
    Returns rendered HTML (string).
    """
    # Normalize input
    featured = None
    stories = []
    events = []

    if isinstance(data, dict):
        featured = data.get("featured")
        stories = data.get("stories") or []
        events = data.get("events") or []
    elif isinstance(data, list):
        # legacy: treat first item as featured, rest as stories
        if len(data) > 0:
            featured = data[0]
            stories = data[1:]
    else:
        # nothing valid passed
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
        item.setdefault("summary", "")
        item.setdefault("image", "https://via.placeholder.com/300x180.png?text=AI+News")
        return item

    featured = assure_fields(featured)
    stories = [assure_fields(s) for s in stories]
    events = [assure_fields(e) for e in events]

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("newsletter.html")

    return template.render(
        featured=featured,
        stories=stories,
        events=events,
        date=datetime.now().strftime("%B %d, %Y"),
        year=datetime.now().year
    )
