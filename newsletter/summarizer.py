import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def summarize_with_groq(text: str, section: str = "story") -> str | None:
    """Summarize text using Groq's LLaMA model with section-specific prompts.
    Returns None for invalid/empty event summaries.
    """
    if not GROQ_API_KEY:
        return f"[Groq fallback summary] {text[:150]}..."

    if section == "featured":
        prompt = (
            "Summarize the following article in 5-6 sentences. "
            "Return ONLY the summary, no preface or extra wording:\n\n"
            f"{text}"
        )
    elif section == "events":
        prompt = (
            "Extract event details (date, topic, registration info) in 1-2 sentences. "
            "If no clear event details exist, respond with exactly: NO_EVENT. "
            "Return ONLY the summary, no preface or explanation:\n\n"
            f"{text}"
        )
    else:  # default story
        prompt = (
            "Summarize the following article in 2-3 sentences. "
            "Return ONLY the summary, no preface or extra wording:\n\n"
            f"{text}"
        )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 200,
        "stream": False,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"].strip()

        # --- Post-processing filters ---
        if section == "events":
            if not summary or "NO_EVENT" in summary.upper():
                return None
            if len(summary.split()) < 4:  # too short to be useful
                return None

        # Strip common unwanted phrases
        bad_prefixes = [
            "here is a summary",
            "summary:",
            "in summary",
            "this article discusses",
        ]
        for bp in bad_prefixes:
            if summary.lower().startswith(bp):
                summary = summary[len(bp):].lstrip(" :-")

        return summary

    except Exception as e:
        return f"[Groq error: {e}] {text[:150]}..."
