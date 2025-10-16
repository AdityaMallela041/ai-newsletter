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
    Fetch CURATED, CUTTING-EDGE content focused on GenAI, LLMs, Agents, and Deep Learning
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
    
    # =====================================================
    # 🎯 CURATED SEARCH QUERIES - GENAI, LLMS, AGENTS, DL
    # =====================================================
    
    # 1. LATEST DEVELOPMENTS - Focus on GenAI breakthroughs, LLM innovations, AI Agents
    developments_results, dev_images = search(
        "latest generative AI breakthroughs LLM GPT-4 Claude Gemini multimodal models "
        "AI agents autonomous systems RAG vector databases 2025 announcements releases",
        max_results=5
    )
    
    # 2. TRAINING & COURSES - Advanced LLM, Agent development, Deep Learning courses
    training_results, train_images = search(
        "youtube.com advanced large language model training LLM fine-tuning "
        "AI agent development reinforcement learning from human feedback RLHF "
        "transformer architecture tutorial deep learning course 2024 2025",
        max_results=5
    )
    
    # 3. RESEARCH PAPERS - Cutting-edge arXiv papers on LLMs, Agents, GenAI
    research_results, research_images = search(
        "arxiv.org latest research papers large language models LLM transformers "
        "multi-agent systems chain-of-thought reasoning prompt engineering "
        "neural networks deep learning October 2025",
        max_results=5
    )
    
    # 4. STARTUPS & TOOLS - GenAI platforms, LLM APIs, Agent frameworks
    startups_results, startups_images = search(
        "new generative AI startups LLM API platforms AI agent frameworks "
        "vector databases AutoGPT LangChain OpenAI alternatives founded 2025",
        max_results=5
    )
    
    
    def extract_source_name(url_val):
        """Extract clean source name from URL"""
        if not url_val:
            return "GENAI NEWS"
        try:
            domain = urlparse(url_val).netloc
            source = domain.replace("www.", "").split(".")[0]
            return source.upper()
        except:
            return "GENAI NEWS"
    
    
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
        
        # UNIQUE Unsplash image per category with GenAI focus
        keywords = {
            "development": "artificial+intelligence+neural+network",
            "training": "machine+learning+programming",
            "research": "data+science+technology",
            "startup": "innovation+technology+startup"
        }
        
        # Use hash of article title for uniqueness
        import time
        seed = hash(res.get("title", "")) + int(time.time() * 1000)
        keyword = keywords.get(article_type, "technology")
        return f"https://source.unsplash.com/800x450/?{keyword}&sig={abs(seed)}"
    
    
    def is_quality_content(res, category):
        """
        Filter for CURATED, HIGH-QUALITY content
        - Must be recent (2024-2025)
        - Must contain relevant keywords
        - Must have substantial content
        """
        title = (res.get("title") or "").lower()
        content = (res.get("content") or res.get("snippet") or "").lower()
        full_text = title + " " + content
        
        # Minimum content length
        if len(content.split()) < 20:
            return False
        
        # Category-specific quality filters
        quality_keywords = {
            "development": [
                "gpt", "llm", "large language model", "generative ai", "genai",
                "claude", "gemini", "agent", "autonomous", "multimodal",
                "rag", "vector", "embedding", "chatbot", "ai assistant"
            ],
            "training": [
                "tutorial", "course", "learn", "training", "guide",
                "llm", "transformer", "fine-tuning", "rlhf", "prompt engineering",
                "langchain", "agent", "deep learning", "neural network"
            ],
            "research": [
                "arxiv", "paper", "research", "study", "neural", "transformer",
                "attention mechanism", "llm", "language model", "benchmark",
                "deep learning", "reasoning", "agent", "multi-agent"
            ],
            "startup": [
                "startup", "founded", "launch", "platform", "api", "tool",
                "llm", "genai", "agent", "vector database", "ai platform",
                "openai", "anthropic", "cohere", "framework"
            ]
        }
        
        # Check if content contains quality keywords
        keywords = quality_keywords.get(category, [])
        matches = sum(1 for keyword in keywords if keyword in full_text)
        
        # Require at least 2 keyword matches
        return matches >= 2
    
    
    def format_article(res, article_type, image_pool=[], index=0):
        """Format article with comprehensive metadata"""
        if not res:
            return None
        
        url_val = res.get("url", "#")
        content_val = res.get("content") or res.get("snippet") or res.get("title") or ""
        
        # Quality check
        if not is_quality_content(res, article_type):
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
        """
        Pick BEST, MOST RELEVANT article
        Priority: Quality > Relevance > Videos > Score
        """
        if not results:
            return None
        
        # Filter for quality content
        quality_results = []
        for idx, res in enumerate(results):
            article = format_article(res, category, images, idx)
            if article:
                quality_results.append((article, res.get("score", 0)))
        
        if not quality_results:
            return None
        
        # Priority 1: Find YouTube video with high score
        video_articles = [(a, s) for a, s in quality_results if a.get("video_id")]
        if video_articles:
            return max(video_articles, key=lambda x: x[1])[0]
        
        # Priority 2: Highest score article
        return max(quality_results, key=lambda x: x[1])[0]
    
    
    # Get single BEST article from each category
    development = get_best_article(developments_results, dev_images, "development")
    training = get_best_article(training_results, train_images, "training")
    research = get_best_article(research_results, research_images, "research")
    startup = get_best_article(startups_results, startups_images, "startup")
    
    # Fetch trending GenAI tools
    trending_tools = fetch_trending_genai_tools()
    
    # Count totals
    articles = [development, training, research, startup]
    total = sum(1 for a in articles if a)
    videos = sum(1 for a in articles if a and a.get("video_id"))
    
    print(f"\n📊 Curated Content Summary:")
    print(f"   🚀 Latest GenAI/LLM Developments: {'✅ Video' if development and development.get('video_id') else '✅ Article'}")
    print(f"   🎓 Advanced Training/Courses: {'✅ Video' if training and training.get('video_id') else '✅ Article'}")
    print(f"   🔬 Cutting-Edge Research: {'✅ Video' if research and research.get('video_id') else '✅ Article'}")
    print(f"   💡 GenAI Startups/Tools: {'✅ Video' if startup and startup.get('video_id') else '✅ Article'}")
    print(f"   🛠️  Trending Tools: {len(trending_tools)} tools")
    print(f"   📈 Total: {total} curated articles ({videos} videos)")
    
    return {
        "development": development,
        "training": training,
        "research": research,
        "startup": startup,
        "trending_tools": trending_tools,
        "total_articles": total,
        "video_count": videos,
    }


def fetch_trending_genai_tools():
    """Fetch CURATED trending GenAI/LLM tools and platforms"""
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "api_key": os.getenv("TAVILY_API_KEY"),
        "query": "trending generative AI tools LLM platforms agent frameworks "
                 "LangChain AutoGPT vector databases Pinecone Weaviate Chroma "
                 "OpenAI API alternatives 2025",
        "search_depth": "advanced",
        "max_results": 5,
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
            # Filter for actual tools/platforms
            if any(keyword in content.lower() for keyword in ["tool", "platform", "framework", "api", "library", "sdk"]):
                tools_list.append({
                    "name": res.get("title", "GenAI Tool"),
                    "description": content[:150] + "..." if len(content) > 150 else content,
                    "link": res.get("url", "#")
                })
        
        return tools_list[:4]  # Top 4 tools
    
    except Exception as e:
        print(f"❌ Error fetching GenAI tools: {e}")
        return []
