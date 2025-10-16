# newsletter/summarizer.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_with_groq(text: str, category: str = "story") -> str | None:
    """
    ENHANCED: Generate STRUCTURED summaries with HTML formatting (side headings and bullet points)
    """
    if not GROQ_API_KEY:
        return f"{text[:150]}..."
    
    # UPDATED: Structured prompts that request HTML output
    prompts = {
        "development": {
            "prompt": (
                "You are a GenAI & LLM expert newsletter writer. Create a STRUCTURED summary with this exact HTML format:\n\n"
                "<p><strong>🚀 What's New</strong><br>\n"
                "Write 1-2 sentences about the breakthrough/announcement.</p>\n\n"
                "<p><strong>💡 Key Highlights</strong></p>\n"
                "<ul>\n"
                "<li>First major feature or innovation</li>\n"
                "<li>Second major feature or innovation</li>\n"
                "<li>Third major feature or innovation</li>\n"
                "</ul>\n\n"
                "<p><strong>🎯 Why It Matters</strong><br>\n"
                "Write 1-2 sentences about real-world impact and significance for AI developers.</p>\n\n"
                "Use technical terms like 'transformer', 'RAG', 'multimodal', 'fine-tuning', 'agent' when relevant. "
                "Return ONLY the HTML formatted summary without any meta-commentary:\n\n"
            ),
            "tokens": 350
        },
        "training": {
            "prompt": (
                "Summarize this LLM/GenAI training resource with this STRUCTURED HTML format:\n\n"
                "<p><strong>📚 What You'll Learn</strong><br>\n"
                "Write 1-2 sentences about the main topics (LLM training, fine-tuning, agents, etc.).</p>\n\n"
                "<p><strong>🎓 Key Topics</strong></p>\n"
                "<ul>\n"
                "<li>First major topic covered</li>\n"
                "<li>Second major topic covered</li>\n"
                "<li>Third major topic covered</li>\n"
                "</ul>\n\n"
                "<p><strong>👥 Best For</strong><br>\n"
                "Write 1 sentence about target audience (developers/researchers/students) and skill level.</p>\n\n"
                "Return ONLY the HTML formatted summary:\n\n"
            ),
            "tokens": 320
        },
        "research": {
            "prompt": (
                "Summarize this LLM/GenAI research paper with this STRUCTURED HTML format:\n\n"
                "<p><strong>🔬 Research Focus</strong><br>\n"
                "Write 1-2 sentences about the research question (transformers, reasoning, agents, etc.).</p>\n\n"
                "<p><strong>⚙️ Key Contributions</strong></p>\n"
                "<ul>\n"
                "<li>Novel methodology or architecture</li>\n"
                "<li>Main experimental findings</li>\n"
                "<li>Performance benchmarks or improvements</li>\n"
                "</ul>\n\n"
                "<p><strong>📊 Impact</strong><br>\n"
                "Write 1-2 sentences about significance for the AI/ML field.</p>\n\n"
                "Use technical language. Return ONLY the HTML formatted summary:\n\n"
            ),
            "tokens": 350
        },
        "startup": {
            "prompt": (
                "Summarize this GenAI/LLM startup or tool with this STRUCTURED HTML format:\n\n"
                "<p><strong>🏢 What They Built</strong><br>\n"
                "Write 1-2 sentences about their product (LLM platform, agent framework, vector DB, etc.).</p>\n\n"
                "<p><strong>✨ Key Features</strong></p>\n"
                "<ul>\n"
                "<li>First major feature or capability</li>\n"
                "<li>Second major feature or capability</li>\n"
                "<li>Third major feature or capability</li>\n"
                "</ul>\n\n"
                "<p><strong>💼 Use Cases</strong><br>\n"
                "Write 1 sentence about primary applications and target market.</p>\n\n"
                "Return ONLY the HTML formatted summary:\n\n"
            ),
            "tokens": 320
        },
        "tool": {
            "prompt": (
                "Describe this GenAI/LLM tool in exactly 2-3 sentences. "
                "Explain: (1) What it does (LangChain, vector DB, agent framework, etc.), "
                "(2) Key features for LLM developers, (3) Primary use case. "
                "Be concise and technical. Return as a single paragraph:\n\n"
            ),
            "tokens": 120
        },
        "featured": {
            "prompt": (
                "You are a GenAI expert. Summarize this AI breakthrough with this STRUCTURED HTML format:\n\n"
                "<p><strong>🚀 What Happened</strong><br>\n"
                "Write 1-2 sentences about the breakthrough.</p>\n\n"
                "<p><strong>💡 Key Details</strong></p>\n"
                "<ul>\n"
                "<li>First major point</li>\n"
                "<li>Second major point</li>\n"
                "<li>Third major point</li>\n"
                "</ul>\n\n"
                "<p><strong>🎯 Impact</strong><br>\n"
                "Write 1-2 sentences about significance for the AI field.</p>\n\n"
                "Return ONLY the HTML formatted summary:\n\n"
            ),
            "tokens": 320
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
                    "Write STRUCTURED summaries with HTML formatting (use <strong> for bold, <ul><li> for bullet points, <p> for paragraphs). "
                    "Use proper terminology (transformers, embeddings, RAG, fine-tuning, RLHF, chain-of-thought). "
                    "Follow the exact HTML format requested with proper tags. "
                    "Do NOT add any meta-commentary like 'here is' or 'summary:'. Return ONLY valid HTML."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": max_tokens,
        "stream": False,
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"].strip()
        
        # Clean up unwanted prefixes and HTML artifacts
        bad_prefixes = [
            "here is", "here's", "summary:", "in summary",
            "this article", "the article", "according to",
            "the research", "researchers", "the text", "this text",
            "sure", "certainly", "of course", "``````"
        ]
        
        summary_lower = summary.lower()
        for bp in bad_prefixes:
            if summary_lower.startswith(bp):
                summary = summary[len(bp):].lstrip(" :-.,")
                break
        
        # Remove code block markers if present
        summary = summary.replace("``````", "").strip()
        
        # Ensure proper HTML structure
        summary = ensure_html_formatting(summary)
        
        return summary
        
    except requests.Timeout:
        print(f"⏱️ Groq timeout for {category}")
        return None
    except Exception as e:
        print(f"❌ Groq error for {category}: {e}")
        return None


def ensure_html_formatting(text):
    """Ensure summary has proper HTML formatting"""
    import re
    
    # If no HTML tags found, wrap in paragraph
    if '<' not in text:
        return f"<p>{text}</p>"
    
    # Fix markdown bold (**text**) to HTML bold if accidentally returned
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Fix markdown bullets (- item) to HTML bullets if accidentally returned
    if '\n- ' in text or '\n-' in text:
        lines = text.split('\n')
        formatted_lines = []
        in_list = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('- '):
                if not in_list:
                    formatted_lines.append('<ul>')
                    in_list = True
                formatted_lines.append(f'<li>{stripped[2:]}</li>')
            else:
                if in_list:
                    formatted_lines.append('</ul>')
                    in_list = False
                if stripped:
                    if not stripped.startswith('<'):
                        formatted_lines.append(f'<p>{stripped}</p>')
                    else:
                        formatted_lines.append(stripped)
        
        if in_list:
            formatted_lines.append('</ul>')
        
        text = '\n'.join(formatted_lines)
    
    return text


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
                    article["summary"] = f"<p>{content[:180]}...</p>"
    
    return articles_data
