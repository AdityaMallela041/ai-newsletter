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
    Fetch categorized AI/ML content:
    - Latest Developments
    - AI Training
    - AI Research  
    - AI Tools
    - AI Startups
    """
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}

    def search(query, max_results=5):
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
    developments_results, dev_images = search("latest AI machine learning breakthroughs news 2025", max_results=4)
    training_results, train_images = search("AI training techniques machine learning courses workshops 2025", max_results=3)
    research_results, research_images = search("AI research papers machine learning arxiv publications 2025", max_results=3)
    tools_results, tools_images = search("new AI tools platforms software releases 2025", max_results=4)
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

    def get_high_quality_image(res, image_pool, index=0):
        """Get best quality image with proper aspect ratio"""
        # Try article's own image
        if res.get("image"):
            return res["image"]
        
        # Try image pool
        if image_pool and len(image_pool) > index:
            return image_pool[index]
        
        # Try to get YouTube thumbnail
        video_id = extract_video_id(res.get("url", ""))
        if video_id:
            return f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
        
        # Fallback to Unsplash with proper dimensions
        keywords = "artificial+intelligence+technology"
        return f"https://source.unsplash.com/800x450/?{keywords}"

    def format_article(res, article_type, image_pool=[], index=0):
        """Format article with comprehensive metadata"""
        if not res:
            return None
            
        url_val = res.get("url", "#")
        content_val = res.get("content") or res.get("snippet") or res.get("title") or ""
        
        # Skip insufficient content
        if len(content_val.split()) < 10:
            return None
        
        # Get high-quality image with proper sizing
        image = get_high_quality_image(res, image_pool, index)
        
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
            "video_id": video_id,  # For YouTube embeds
            "source": extract_source_name(url_val),
            "published_date": published_date,
            "score": res.get("score", 0.0),
            "category": article_type
        }

    # Format all categories
    developments = [format_article(r, "development", dev_images, i) 
                    for i, r in enumerate(developments_results) 
                    if format_article(r, "development", dev_images, i)][:4]
    
    training = [format_article(r, "training", train_images, i) 
                for i, r in enumerate(training_results) 
                if format_article(r, "training", train_images, i)][:3]
    
    research = [format_article(r, "research", research_images, i) 
                for i, r in enumerate(research_results) 
                if format_article(r, "research", research_images, i)][:3]
    
    tools = [format_article(r, "tool", tools_images, i) 
             for i, r in enumerate(tools_results) 
             if format_article(r, "tool", tools_images, i)][:4]
    
    startups = [format_article(r, "startup", startups_images, i) 
                for i, r in enumerate(startups_results) 
                if format_article(r, "startup", startups_images, i)][:3]

    print(f"\n📊 Fetch Summary:")
    print(f"   Latest Developments: {len(developments)}")
    print(f"   AI Training: {len(training)}")
    print(f"   AI Research: {len(research)}")
    print(f"   AI Tools: {len(tools)}")
    print(f"   AI Startups: {len(startups)}")

    return {
        "developments": developments,
        "training": training,
        "research": research,
        "tools": tools,
        "startups": startups,
    }
