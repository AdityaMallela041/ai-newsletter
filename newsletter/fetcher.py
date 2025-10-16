# newsletter/fetcher.py

import os
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from dotenv import load_dotenv
import re

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
    
    # 1. LATEST DEVELOPMENTS
    developments_results, dev_images = search(
        "latest generative AI breakthroughs LLM GPT-4 Claude Gemini multimodal models "
        "AI agents autonomous systems RAG vector databases 2025 announcements releases",
        max_results=5
    )
    
    # 2. TRAINING & COURSES
    training_results, train_images = search(
        "youtube.com advanced large language model training LLM fine-tuning "
        "AI agent development reinforcement learning from human feedback RLHF "
        "transformer architecture tutorial deep learning course 2024 2025",
        max_results=5
    )
    
    # 3. RESEARCH PAPERS
    research_results, research_images = search(
        "arxiv.org latest research papers large language models LLM transformers "
        "multi-agent systems chain-of-thought reasoning prompt engineering "
        "neural networks deep learning October 2025",
        max_results=5
    )
    
    # 4. STARTUPS & TOOLS
    startups_results, startups_images = search(
        "new generative AI startups LLM API platforms AI agent frameworks "
        "vector databases AutoGPT LangChain OpenAI Anthropic Cohere founded 2025",
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
        """ENHANCED: Extract YouTube video ID from ALL URL formats"""
        if not url_val:
            return None
        
        # Comprehensive YouTube URL patterns
        patterns = [
            # Standard: https://www.youtube.com/watch?v=VIDEO_ID
            r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
            
            # Short: https://youtu.be/VIDEO_ID
            r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
            
            # Embed: https://www.youtube.com/embed/VIDEO_ID
            r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            
            # Shorts: https://www.youtube.com/shorts/VIDEO_ID
            r'(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
            
            # Mobile: https://m.youtube.com/watch?v=VIDEO_ID
            r'(?:m\.youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
            
            # Live: https://www.youtube.com/live/VIDEO_ID
            r'(?:youtube\.com\/live\/)([a-zA-Z0-9_-]{11})',
            
            # Video with timestamp: ?v=VIDEO_ID&t=123s
            r'[?&]v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url_val)
            if match:
                video_id = match.group(1)
                print(f"   🎥 Extracted YouTube ID: {video_id}")
                return video_id
        
        # Check if URL contains youtube/youtu keywords but no match
        if 'youtube' in url_val.lower() or 'youtu.be' in url_val.lower():
            print(f"   ⚠️ YouTube URL detected but couldn't extract ID: {url_val}")
        
        return None
    
    def get_high_quality_image(res, image_pool, article_type, index=0):
        """Get UNIQUE image per article"""
        if res.get("image"):
            return res["image"]
        
        if image_pool and len(image_pool) > index:
            return image_pool[index]
        
        video_id = extract_video_id(res.get("url", ""))
        if video_id:
            return f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
        
        keywords = {
            "development": "artificial+intelligence+neural+network",
            "training": "machine+learning+programming",
            "research": "data+science+technology",
            "startup": "innovation+technology+startup"
        }
        
        import time
        seed = hash(res.get("title", "")) + int(time.time() * 1000)
        keyword = keywords.get(article_type, "technology")
        return f"https://source.unsplash.com/800x450/?{keyword}&sig={abs(seed)}"
    
    def is_quality_content(res, category):
        """ENHANCED: Filter for HIGH-QUALITY, TECHNICAL content"""
        title = (res.get("title") or "").lower()
        content = (res.get("content") or res.get("snippet") or "").lower()
        full_text = title + " " + content
        
        # INCREASED: Minimum 50 words for technical depth
        word_count = len(content.split())
        if word_count < 50:
            print(f"   ❌ Rejected: Too short ({word_count} words)")
            return False
        
        # Category-specific quality keywords (expanded lists)
        quality_keywords = {
            "development": [
                "gpt", "llm", "large language model", "generative ai", "genai",
                "claude", "gemini", "agent", "autonomous", "multimodal",
                "rag", "vector", "embedding", "chatbot", "ai assistant",
                "transformer", "attention", "fine-tuning", "prompt engineering",
                "api", "model", "training", "inference", "deployment"
            ],
            "training": [
                "tutorial", "course", "learn", "training", "guide",
                "llm", "transformer", "fine-tuning", "rlhf", "prompt engineering",
                "langchain", "agent", "deep learning", "neural network",
                "pytorch", "tensorflow", "hugging face", "practical", "hands-on",
                "build", "implement", "code", "project"
            ],
            "research": [
                "arxiv", "paper", "research", "study", "neural", "transformer",
                "attention mechanism", "llm", "language model", "benchmark",
                "deep learning", "reasoning", "agent", "multi-agent",
                "novel", "algorithm", "architecture", "experiment", "result",
                "performance", "accuracy", "dataset"
            ],
            "startup": [
                "startup", "founded", "launch", "platform", "api", "tool",
                "llm", "genai", "agent", "vector database", "ai platform",
                "openai", "anthropic", "cohere", "framework", "company",
                "funding", "product", "service", "enterprise", "solution"
            ]
        }
        
        keywords = quality_keywords.get(category, [])
        matches = sum(1 for keyword in keywords if keyword in full_text)
        
        # INCREASED: Require 3+ keyword matches for better relevance
        if matches < 3:
            print(f"   ❌ Rejected: Low relevance ({matches} keyword matches)")
            return False
        
        # BONUS: Penalize promotional/spam content
        spam_indicators = [
            "click here", "buy now", "limited offer", "sign up today",
            "exclusive deal", "download now", "free trial", "subscribe"
        ]
        spam_count = sum(1 for spam in spam_indicators if spam in full_text)
        
        if spam_count >= 2:
            print(f"   ❌ Rejected: Too promotional ({spam_count} spam indicators)")
            return False
        
        # BONUS: Prefer content with technical depth indicators
        depth_indicators = [
            "implementation", "architecture", "algorithm", "framework",
            "methodology", "approach", "technique", "system", "design",
            "evaluation", "analysis", "experiment", "benchmark"
        ]
        depth_score = sum(1 for indicator in depth_indicators if indicator in full_text)
        
        print(f"   ✅ Quality: {word_count} words, {matches} keywords, {depth_score} depth indicators")
        return True
    
    def format_article(res, article_type, image_pool=[], index=0):
        """Format article with comprehensive metadata"""
        if not res:
            return None
        
        url_val = res.get("url", "#")
        content_val = res.get("content") or res.get("snippet") or res.get("title") or ""
        
        if not is_quality_content(res, article_type):
            return None
        
        image = get_high_quality_image(res, image_pool, article_type, index)
        video_id = extract_video_id(url_val)
        
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
        """Pick BEST, MOST RELEVANT article"""
        if not results:
            return None
        
        quality_results = []
        for idx, res in enumerate(results):
            article = format_article(res, category, images, idx)
            if article:
                quality_results.append((article, res.get("score", 0)))
        
        if not quality_results:
            return None
        
        # Prioritize video content
        video_articles = [(a, s) for a, s in quality_results if a.get("video_id")]
        if video_articles:
            return max(video_articles, key=lambda x: x[1])[0]
        
        return max(quality_results, key=lambda x: x[1])[0]
    
    development = get_best_article(developments_results, dev_images, "development")
    training = get_best_article(training_results, train_images, "training")
    research = get_best_article(research_results, research_images, "research")
    startup = get_best_article(startups_results, startups_images, "startup")
    
    # Fetch trending GenAI tools
    trending_tools = fetch_trending_genai_tools()
    
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
        "tools": trending_tools,
        "total_articles": total,
        "video_count": videos,
    }


def fetch_trending_genai_tools():
    """Fetch CURATED trending GenAI/LLM tools with CLEAN descriptions"""
    
    # FALLBACK: Curated list of top GenAI tools with clean descriptions
    curated_tools = [
        {
            "name": "LangChain",
            "description": "Framework for developing applications powered by language models. Build LLM apps with chains, agents, and memory components.",
            "link": "https://langchain.com"
        },
        {
            "name": "Pinecone",
            "description": "Vector database for AI applications. Store and retrieve embeddings at scale for semantic search and RAG systems.",
            "link": "https://pinecone.io"
        },
        {
            "name": "AutoGPT",
            "description": "Autonomous AI agents that can execute complex tasks with minimal human input using GPT-4 and chain-of-thought reasoning.",
            "link": "https://github.com/Significant-Gravitas/AutoGPT"
        },
        {
            "name": "LlamaIndex",
            "description": "Data framework for LLM applications. Connect custom data sources to large language models with ease.",
            "link": "https://llamaindex.ai"
        }
    ]
    
    # Try to fetch from API, but use curated list as fallback
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": os.getenv("TAVILY_API_KEY"),
        "query": "LangChain Pinecone vector database LlamaIndex AI agent frameworks 2025",
        "search_depth": "basic",
        "max_results": 6,
        "include_images": False,
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        result = resp.json()
        results = result.get("results", [])
        
        if not results:
            return curated_tools
        
        tools_list = []
        seen_names = set()
        
        # Known GenAI tools for matching
        known_tools = ["langchain", "pinecone", "autogpt", "llamaindex", "weaviate",
                      "chroma", "milvus", "qdrant", "haystack", "semantic kernel"]
        
        for res in results:
            title = res.get("title", "").lower()
            content = (res.get("content") or res.get("snippet") or "").lower()
            url_link = res.get("url", "#")
            
            # Check if it's a known tool
            tool_found = None
            for known in known_tools:
                if known in title or known in url_link.lower():
                    tool_found = known.title().replace("gpt", "GPT")
                    break
            
            if not tool_found:
                continue
            
            if tool_found.lower() in seen_names:
                continue
            
            # Clean description - remove URLs, markdown, etc.
            clean_content = content.replace("[", "").replace("]", "").replace("(https://", "")
            sentences = clean_content.split(".")
            description = sentences[0][:120] + "..." if len(sentences[0]) > 120 else sentences[0] + "."
            
            tools_list.append({
                "name": tool_found,
                "description": description.strip(),
                "link": url_link
            })
            seen_names.add(tool_found.lower())
            
            if len(tools_list) >= 4:
                break
        
        # Return curated list if API results are poor
        if len(tools_list) < 2:
            return curated_tools
        
        return tools_list
        
    except Exception as e:
        print(f"❌ Error fetching tools, using curated list: {e}")
        return curated_tools
