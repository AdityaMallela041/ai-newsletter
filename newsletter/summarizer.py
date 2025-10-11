# newsletter/summarizer.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_with_groq(text: str, section: str = "story") -> str | None:
    """
    Summarize text using Groq's LLaMA model with enhanced prompts.
    Returns None for invalid/empty content.
    """
    if not GROQ_API_KEY:
        return f"{text[:150]}..."

    # Enhanced prompts for different sections
    if section == "featured":
        prompt = (
            "You are a tech newsletter writer. Summarize this AI/ML article in 4-5 engaging sentences "
            "that highlight the key breakthrough, its significance, and potential impact. "
            "Write in an informative yet accessible tone. Return ONLY the summary:\n\n"
            f"{text}"
        )
        max_tokens = 250
        
    elif section == "events":
        prompt = (
            "Extract event details from this text. Include: event name, date/time, topic, and how to register. "
            "If no clear event information exists, respond with exactly: NO_EVENT. "
            "Return ONLY the event summary in 2-3 sentences:\n\n"
            f"{text}"
        )
        max_tokens = 150
        
    elif section == "quick_hit":
        prompt = (
            "Summarize this AI news in 1-2 punchy sentences. Be concise and highlight what's newsworthy. "
            "Return ONLY the summary:\n\n"
            f"{text}"
        )
        max_tokens = 100
        
    elif section == "tool":
        prompt = (
            "Describe this AI tool/platform in 2-3 sentences. Focus on: what it does, key features, "
            "and who it's for. Return ONLY the description:\n\n"
            f"{text}"
        )
        max_tokens = 150
        
    else:  # default story
        prompt = (
            "You are a tech newsletter writer. Summarize this AI/ML article in 3-4 clear sentences. "
            "Focus on the key points and why it matters. Return ONLY the summary:\n\n"
            f"{text}"
        )
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
                "content": "You are an expert tech writer specializing in AI and machine learning newsletters."
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
        
        # Filter out unwanted responses
        if section == "events":
            if not summary or "NO_EVENT" in summary.upper():
                return None
            if len(summary.split()) < 5:
                return None
        
        # Clean up common prefixes
        bad_prefixes = [
            "here is a summary", "summary:", "in summary",
            "this article discusses", "the article", "according to",
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
        print(f"⏱️ Groq timeout for {section}")
        return None
    except Exception as e:
        print(f"❌ Groq error for {section}: {e}")
        return None
