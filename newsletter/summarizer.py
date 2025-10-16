# newsletter/summarizer.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_with_groq(text: str, category: str = "story") -> str | None:
    """
    ENHANCED: Summaries focused on GenAI, LLMs, Agents, and Deep Learning
    """
    if not GROQ_API_KEY:
        return f"{text[:150]}..."
    
    # UPDATED: Category-specific prompts for GenAI/LLM content
    prompts = {
        "development": {
            "prompt": (
                "You are a GenAI & LLM expert newsletter writer. Summarize this breakthrough in exactly 4-5 sentences. "
                "Focus on: (1) What's new in LLMs/GenAI/Agents, (2) Technical innovation, "
                "(3) Why it matters for AI development, (4) Real-world implications. "
                "Use terms like 'transformer', 'RAG', 'multimodal', 'fine-tuning' when relevant. "
                "Be technical yet accessible. Return ONLY the summary:\n\n"
            ),
            "tokens": 200
        },
        "training": {
            "prompt": (
                "Summarize this LLM/GenAI training resource in exactly 3-4 sentences. "
                "Cover: (1) What it teaches (LLM training, fine-tuning, agents, etc.), "
                "(2) Target audience (developers/researchers/students), (3) Key learning outcomes. "
                "Focus on practical skills for building with LLMs. Return ONLY the summary:\n\n"
            ),
            "tokens": 160
        },
        "research": {
            "prompt": (
                "Summarize this LLM/GenAI research paper in exactly 3-4 sentences. "
                "Include: (1) Research question (transformers, reasoning, agents, etc.), "
                "(2) Novel methodology or architecture, (3) Key findings and benchmarks, "
                "(4) Significance for the field. Use technical language. Return ONLY the summary:\n\n"
            ),
            "tokens": 180
        },
        "startup": {
            "prompt": (
                "Summarize this GenAI/LLM startup or tool in exactly 3-4 sentences. "
                "Cover: (1) What they're building (LLM platform, agent framework, vector DB, etc.), "
                "(2) Unique technology or approach, (3) Use cases and target market. "
                "Emphasize innovation in the GenAI space. Return ONLY the summary:\n\n"
            ),
            "tokens": 160
        },
        "tool": {
            "prompt": (
                "Describe this GenAI/LLM tool in exactly 2-3 sentences. "
                "Explain: (1) What it does (LangChain, vector DB, agent framework, etc.), "
                "(2) Key features for LLM developers, (3) Primary use case. "
                "Be concise and technical. Return ONLY the description:\n\n"
            ),
            "tokens": 120
        },
        "featured": {
            "prompt": (
                "You are a GenAI expert. Summarize this AI breakthrough in exactly 4-5 sentences. "
                "Structure: (1) What happened, (2) Why it matters for LLMs/GenAI, "
                "(3) Technical details, (4) Impact on the field. "
                "Be clear, engaging, and informative. Return ONLY the summary:\n\n"
            ),
            "tokens": 200
        }
    }
    
    # Use category-specific prompt or default to 'development'
    config = prompts.get(category, prompts["development"])
    prompt = config["prompt"] + text
    max_tokens = config["tokens"]
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert in Generative AI, Large Language Models, AI Agents, and Deep Learning. "
                    "Write clear, technically accurate summaries for an audience of AI/ML students and developers. "
                    "Use proper terminology (transformers, embeddings, RAG, fine-tuning, RLHF, chain-of-thought, etc.). "
                    "Be concise and stick to the requested length exactly."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6,
        "max_tokens": max_tokens,
        "stream": False,
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"].strip()
        
        # Clean up unwanted prefixes
        bad_prefixes = [
            "here is", "here's", "summary:", "in summary",
            "this article", "the article", "according to",
            "the research", "researchers", "the text", "this text"
        ]
        
        summary_lower = summary.lower()
        for bp in bad_prefixes:
            if summary_lower.startswith(bp):
                summary = summary[len(bp):].lstrip(" :-.,")
                if summary:
                    summary = summary[0].upper() + summary[1:]
                break
        
        return summary
    
    except requests.Timeout:
        print(f"⏱️ Groq timeout for {category}")
        return None
    
    except Exception as e:
        print(f"❌ Groq error for {category}: {e}")
        return None


def summarize_articles(articles_data):
    """
    Summarize articles with category-appropriate prompts
    """
    if not articles_data:
        return articles_data
    
    # Process single articles (not lists)
    for category in ["development", "training", "research", "startup"]:
        article = articles_data.get(category)
        if article and isinstance(article, dict):
            content = article.get("content", "")
            if content:
                print(f"📝 Summarizing {category}...")
                summary = summarize_with_groq(content, category=category)
                if summary:
                    article["summary"] = summary
                else:
                    # Fallback to truncated content
                    article["summary"] = content[:180] + "..."
    
    return articles_data
