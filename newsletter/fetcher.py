# newsletter/fetcher.py

import os
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def fetch_articles():
    """
    Fetch ONE article per category with unique images
    """
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}

    def search(query, max_results=3):
        """Enhanced search with image support"""
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_images": True,
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

    # Fetch categorized content
    developments_results, dev_images = search("latest AI machine learning breakthroughs news 2025", max_results=3)
    training_results, train_images = search("youtube.com AI machine learning tutorial course training 2024 2025", max_results=3)
    research_results, research_images = search("AI research papers machine learning arxiv publications 2025", max_results=3)
    startups_results, startups_images = search("new AI startups machine learning companies founded 2025", max_results=3)

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

    def extract_video_id(url_val):
        """Extract YouTube video ID if present"""
        if not url_val or "youtube.com" not in url_val and "youtu.be" not in url_val:
            return None
        try:
            if "youtu.be" in url_val:
                return url_val.split("/")[-1].split("?")[0]
            parsed = urlparse(url_val)
            if "youtube.com" in parsed.netloc:
                return parse_qs(parsed.query).get("v", [None])[0]
        except:
            return None
        return None

    def get_high_quality_image(res, image_pool, article_type, index=0):
        """Get UNIQUE image per article"""
        # Try article's own image
        if res.get("image"):
            return res["image"]
        
        # Try image pool with index
        if image_pool and len(image_pool) > index:
            return image_pool[index]
        
        # Try YouTube thumbnail
        video_id = extract_video_id(res.get("url", ""))
        if video_id:
            return f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
        
        # UNIQUE Unsplash image per category
        keywords = {
            "development": "artificial+intelligence+technology",
            "training": "online+learning+education",
            "research": "science+laboratory+research",
            "startup": "startup+business+innovation"
        }
        
        # Use hash of article title for uniqueness
        import time
        seed = hash(res.get("title", "")) + int(time.time() * 1000)
        keyword = keywords.get(article_type, "technology")
        return f"https://source.unsplash.com/800x450/?{keyword}&sig={abs(seed)}"

    def format_article(res, article_type, image_pool=[], index=0):
        """Format article with comprehensive metadata"""
        if not res:
            return None
        
        url_val = res.get("url", "#")
        content_val = res.get("content") or res.get("snippet") or res.get("title") or ""
        
        # Skip insufficient content
        if len(content_val.split()) < 10:
            return None
        
        # Get UNIQUE image
        image = get_high_quality_image(res, image_pool, article_type, index)
        
        # Check if it's a YouTube video
        video_id = extract_video_id(url_val)
        
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
            "video_id": video_id,
            "source": extract_source_name(url_val),
            "published_date": published_date,
            "score": res.get("score", 0.0),
            "category": article_type
        }

    def get_best_article(results, images, category):
        """Pick best article - prioritize videos"""
        if not results:
            return None
        
        # Priority 1: Find YouTube video
        for idx, res in enumerate(results):
            if extract_video_id(res.get("url", "")):
                return format_article(res, category, images, idx)
        
        # Priority 2: Highest score article
        best = max(results, key=lambda x: x.get("score", 0))
        idx = results.index(best)
        return format_article(best, category, images, idx)

    # Get single best article from each category
    development = get_best_article(developments_results, dev_images, "development")
    training = get_best_article(training_results, train_images, "training")
    research = get_best_article(research_results, research_images, "research")
    startup = get_best_article(startups_results, startups_images, "startup")

    # Fetch trending tools (simple list)
    trending_tools = fetch_trending_tools()

    # Count totals
    articles = [development, training, research, startup]
    total = sum(1 for a in articles if a)
    videos = sum(1 for a in articles if a and a.get("video_id"))

    print(f"\n📊 Fetch Summary:")
    print(f"   Latest Developments: {'✅ Video' if development and development.get('video_id') else '✅ Article'}")
    print(f"   AI Training: {'✅ Video' if training and training.get('video_id') else '✅ Article'}")
    print(f"   AI Research: {'✅ Video' if research and research.get('video_id') else '✅ Article'}")
    print(f"   AI Startups: {'✅ Video' if startup and startup.get('video_id') else '✅ Article'}")
    print(f"   Trending Tools: {len(trending_tools)} tools")
    print(f"   Total: {total} articles ({videos} videos)")

    return {
        "development": development,
        "training": training,
        "research": research,
        "startup": startup,
        "trending_tools": trending_tools,
        "total_articles": total,
        "video_count": videos,
    }


def fetch_trending_tools():
    """Fetch trending AI tools as simple list"""
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "api_key": os.getenv("TAVILY_API_KEY"),
        "query": "trending AI tools platforms software 2025",
        "search_depth": "basic",
        "max_results": 4,
        "include_images": False,
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        results = result.get("results", [])
        
        tools_list = []
        for res in results[:4]:
            content = res.get("content") or res.get("snippet") or ""
            tools_list.append({
                "name": res.get("title", "AI Tool"),
                "description": content[:150] + "..." if len(content) > 150 else content,
                "link": res.get("url", "#")
            })
        
        return tools_list
        
    except Exception as e:
        print(f"❌ Error fetching tools: {e}")
        return []
