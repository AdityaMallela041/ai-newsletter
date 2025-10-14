# newsletter/summarizer.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_with_groq(text: str, category: str = "story") -> str | None:
    """
    ENHANCED: Consistent summaries with better prompts and token limits
    """
    if not GROQ_API_KEY:
        return f"{text[:150]}..."

    # ENHANCED: More specific prompts with consistent length
    prompts = {
        "featured": {
            "prompt": (
                "You are a tech newsletter writer. Summarize this AI breakthrough in exactly 4-5 sentences. "
                "Structure: (1) What happened, (2) Why it matters, (3) Technical details, (4) Impact/implications. "
                "Be clear, engaging, and informative. Return ONLY the summary:\n\n"
            ),
            "tokens": 200
        },
        "story": {
            "prompt": (
                "Summarize this AI news in exactly 3-4 sentences. "
                "Focus on: what happened, why it's significant, and key takeaways. "
                "Be concise and factual. Return ONLY the summary:\n\n"
            ),
            "tokens": 180
        },
        "training": {
            "prompt": (
                "Summarize this AI training resource in exactly 2-3 sentences. "
                "Cover: what it teaches, who it's for, and key learning outcomes. "
                "Return ONLY the summary:\n\n"
            ),
            "tokens": 140
        },
        "research": {
            "prompt": (
                "Summarize this AI research in exactly 3-4 sentences. "
                "Include: research question, methodology, key findings, and significance. "
                "Use accessible language. Return ONLY the summary:\n\n"
            ),
            "tokens": 180
        },
        "tool": {
            "prompt": (
                "Describe this AI tool in exactly 2-3 sentences. "
                "Explain: what it does, key features, and primary use case. "
                "Return ONLY the description:\n\n"
            ),
            "tokens": 140
        },
        "startup": {
            "prompt": (
                "Summarize this AI startup in exactly 2-3 sentences. "
                "Cover: what they build, unique value proposition, and target market. "
                "Return ONLY the summary:\n\n"
            ),
            "tokens": 140
        }
    }
    
    config = prompts.get(category, prompts["story"])
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
                    "You are an expert tech newsletter writer. "
                    "Write clear, engaging summaries that are informative yet accessible. "
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
            "the research", "researchers"
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
