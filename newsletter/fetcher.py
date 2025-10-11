# newsletter/fetcher.py
import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def fetch_articles():
    """
    Fetch latest AI/ML news with enhanced image extraction from multiple sources
    """
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}

    def search(query, max_results=5):
        """Enhanced search with better image handling"""
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_images": True,  # Request images from Tavily
            "include_answer": False,
            "include_raw_content": False,
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            return result.get("results", []), result.get("images", [])
        except Exception as e:
            print(f"❌ Error fetching from Tavily: {e}")
            return [], []

    # Fetch with images
    featured_results, featured_images = search("major AI breakthrough 2025", max_results=1)
    story_results, story_images = search("latest AI machine learning news", max_results=8)
    quick_hit_results, quick_images = search("AI news updates", max_results=6)
    tool_results, tool_images = search("new AI tools platforms 2025", max_results=5)
    event_results, event_images = search("upcoming AI conferences workshops 2025", max_results=4)

    def extract_source_name(url_val):
        """Extract clean source name from URL"""
        if not url_val:
            return "AI NEWS"
        try:
            domain = urlparse(url_val).netloc
            source = domain.replace("www.", "").split(".")[0]
            return source.upper()
        except:
            return "AI NEWS"

    def get_image_for_article(res, image_pool, index=0):
        """
        Get image for article from multiple sources:
        1. Article's own image field
        2. Image pool from Tavily
        3. OpenGraph image via URL scraping
        4. High-quality placeholder
        """
        # Try article's own image first
        if res.get("image"):
            return res["image"]
        
        # Try image pool
        if image_pool and len(image_pool) > index:
            return image_pool[index]
        
        # Try getting image from the article URL using a simple trick
        article_url = res.get("url", "")
        if article_url:
            # Use a free OpenGraph API service
            try:
                og_api = f"https://opengraph.io/api/1.1/site/{requests.utils.quote(article_url)}?app_id=free"
                og_resp = requests.get(og_api, timeout=5)
                if og_resp.status_code == 200:
                    og_data = og_resp.json()
                    og_image = og_data.get("hybridGraph", {}).get("image")
                    if og_image:
                        return og_image
            except:
                pass
        
        # Fallback: Use Unsplash for real AI/tech images instead of placeholder
        title_keywords = res.get("title", "artificial intelligence")
        keywords = "artificial+intelligence+technology"
        return f"https://source.unsplash.com/1200x630/?{keywords}"

    def format_article(res, article_type="story", image_pool=[], index=0):
        """Format article with comprehensive metadata and real images"""
        if not res:
            return None
            
        url_val = res.get("url", "#")
        content_val = res.get("content") or res.get("snippet") or res.get("title") or ""
        
        # Skip articles with insufficient content
        if article_type == "event" and len(content_val.split()) < 10:
            return None
        
        # Get best available image
        image = get_image_for_article(res, image_pool, index)
        
        # Extract published date
        published_date = res.get("published_date")
        if not published_date:
            published_date = datetime.now().strftime("%b %d, %Y")
        else:
            try:
                if isinstance(published_date, str):
                    date_obj = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                    published_date = date_obj.strftime("%b %d, %Y")
            except:
                published_date = datetime.now().strftime("%b %d, %Y")
        
        return {
            "title": res.get("title") or "Untitled",
            "url": url_val,
            "link": url_val,
            "content": content_val,
            "image": image,
            "source": extract_source_name(url_val),
            "published_date": published_date,
            "score": res.get("score", 0.0),
        }

    # Format all content with images
    featured = None
    if featured_results:
        featured = format_article(featured_results[0], "featured", featured_images, 0)
    
    stories = []
    for i, r in enumerate(story_results[:6]):
        article = format_article(r, "story", story_images, i)
        if article:
            stories.append(article)
    
    quick_hits = []
    for i, r in enumerate(quick_hit_results[:5]):
        article = format_article(r, "quick_hit", quick_images, i)
        if article:
            quick_hits.append({
                "title": article.get("title", ""),
                "link": article.get("link", "#"),
                "summary": article.get("content", "")[:150] + "..."
            })
    
    trending_tools = []
    for i, r in enumerate(tool_results[:4]):
        article = format_article(r, "tool", tool_images, i)
        if article:
            trending_tools.append({
                "icon": "🔧",
                "name": article["title"][:60],
                "description": article["content"][:120] + "...",
                "link": article["link"]
            })
    
    events = []
    for i, r in enumerate(event_results):
        article = format_article(r, "event", event_images, i)
        if article:
            events.append(article)

    print(f"\n📊 Fetch Summary:")
    print(f"   Featured: {1 if featured else 0}")
    print(f"   Stories: {len(stories)}")
    print(f"   Quick Hits: {len(quick_hits)}")
    print(f"   Trending Tools: {len(trending_tools)}")
    print(f"   Events: {len(events)}")
    
    # Debug: Show image sources
    print(f"\n🖼️ Image Summary:")
    print(f"   Featured image: {featured['image'][:60] if featured else 'None'}...")
    if stories:
        print(f"   Story 1 image: {stories[0]['image'][:60]}...")

    return {
        "featured": featured,
        "stories": stories,
        "quick_hits": quick_hits,
        "trending_tools": trending_tools,
        "events": events,
    }
