# newsletter/summarizer.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_with_groq(text: str, category: str = "development") -> str | None:
    """
    Category-specific AI summarization:
    - development: Latest AI/ML breakthroughs
    - training: AI training techniques and courses
    - research: Academic research and papers
    - tool: AI tools and platforms
    - startup: New AI companies and startups
    """
    if not GROQ_API_KEY:
        return f"{text[:150]}..."

    # Category-specific prompts
    prompts = {
        "development": (
            "Summarize this AI/ML breakthrough in 3-4 sentences. "
            "Focus on: what happened, why it matters, and potential impact. "
            "Be clear and engaging. Return ONLY the summary:\n\n"
        ),
        "training": (
            "Summarize this AI training resource in 2-3 sentences. "
            "Focus on: what's covered, who it's for, and key learnings. "
            "Return ONLY the summary:\n\n"
        ),
        "research": (
            "Summarize this AI research in 3-4 sentences. "
            "Focus on: research question, methodology, and key findings. "
            "Return ONLY the summary:\n\n"
        ),
        "tool": (
            "Summarize this AI tool in 2-3 sentences. "
            "Focus on: what it does, key features, and use cases. "
            "Return ONLY the summary:\n\n"
        ),
        "startup": (
            "Summarize this AI startup in 2-3 sentences. "
            "Focus on: what they build, their unique approach, and target market. "
            "Return ONLY the summary:\n\n"
        )
    }
    
    prompt = prompts.get(category, prompts["development"]) + text
    max_tokens = 200

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
                "content": "You are an expert tech writer for AI newsletters. Write clear, engaging summaries."
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
        bad_prefixes = ["here is", "summary:", "this article", "the article"]
        summary_lower = summary.lower()
        for bp in bad_prefixes:
            if summary_lower.startswith(bp):
                summary = summary[len(bp):].lstrip(" :-.,")
                if summary:
                    summary = summary[0].upper() + summary[1:]
                break
        
        return summary
        
    except Exception as e:
        print(f"❌ Groq error for {category}: {e}")
        return None
