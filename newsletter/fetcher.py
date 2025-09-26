import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def fetch_articles():
    """Fetch latest AI/ML news and split into featured, stories, and events."""
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}

    def search(query, max_results=5):
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
        }
        try:
            resp = requests.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except Exception as e:
            print("❌ Error fetching from Tavily:", e)
            return []

    # Featured story
    featured_results = search("major breakthrough in AI and machine learning 2025", max_results=1)

    # Regular stories
    story_results = search("latest AI and machine learning news", max_results=4)

    # Events
    event_results = search("upcoming AI machine learning conferences workshops 2025", max_results=4)

    def format_article(res, is_event=False):
        url_val = res.get("url")
        domain = urlparse(url_val).netloc if url_val else ""

        # Tavily sometimes uses 'image_url', not 'thumbnail'
        image_url = res.get("image_url") or res.get("thumbnail")
        if not image_url:
            # fallback → try favicon, else placeholder
            image_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128" if domain else \
                        "https://via.placeholder.com/600x300.png?text=AI+News"

        content_val = res.get("content") or res.get("snippet") or res.get("title") or ""

        # For events, skip if no meaningful description
        if is_event and len(content_val.split()) < 10:
            return None

        return {
            "title": res.get("title") or "Untitled",
            "url": url_val,
            "content": content_val,
            "image": image_url,
        }


    featured = format_article(featured_results[0]) if featured_results else None
    stories = [format_article(r) for r in story_results if format_article(r)]
    events = [format_article(r, is_event=True) for r in event_results if format_article(r, is_event=True)]

    return {
        "featured": featured,
        "stories": stories,
        "events": events,
    }
