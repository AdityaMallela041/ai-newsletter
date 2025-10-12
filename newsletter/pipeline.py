# newsletter/pipeline.py
import os
from datetime import datetime
from newsletter.fetcher import fetch_articles
from newsletter.summarizer import summarize_with_groq
from newsletter.database import init_db, save_articles, log_newsletter_sent
from newsletter.templates import render_newsletter
from newsletter.emailer import send_email

OUTPUT_DIR = "newsletter/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_pipeline():
    """Production newsletter pipeline with categorized content"""
    print("=" * 70)
    print("🚀 CSE(AI&ML) Newsletter Pipeline - Production Mode")
    print("=" * 70)
    
    # Step 1: Initialize database
    init_db()
    
    # Step 2: Fetch categorized content
    print("\n📡 Fetching categorized AI/ML content...")
    data = fetch_articles()
    
    developments = data.get("developments", [])
    training = data.get("training", [])
    research = data.get("research", [])
    tools = data.get("tools", [])
    startups = data.get("startups", [])
    
    # Step 3: Enhance with AI summaries
    print("\n🤖 Generating category-specific summaries...")
    
    # Summarize developments
    valid_developments = []
    for idx, item in enumerate(developments, 1):
        if item.get("content"):
            summary = summarize_with_groq(item["content"], "development")
            if summary:
                item["summary"] = summary
                valid_developments.append(item)
                print(f"   ✅ Development {idx}: {item['title'][:45]}...")
    developments = valid_developments
    
    # Summarize training
    valid_training = []
    for idx, item in enumerate(training, 1):
        if item.get("content"):
            summary = summarize_with_groq(item["content"], "training")
            if summary:
                item["summary"] = summary
                valid_training.append(item)
                print(f"   ✅ Training {idx}: {item['title'][:45]}...")
    training = valid_training
    
    # Summarize research
    valid_research = []
    for idx, item in enumerate(research, 1):
        if item.get("content"):
            summary = summarize_with_groq(item["content"], "research")
            if summary:
                item["summary"] = summary
                valid_research.append(item)
                print(f"   ✅ Research {idx}: {item['title'][:45]}...")
    research = valid_research
    
    # Summarize tools
    valid_tools = []
    for idx, item in enumerate(tools, 1):
        if item.get("content"):
            summary = summarize_with_groq(item["content"], "tool")
            if summary:
                item["summary"] = summary
                valid_tools.append(item)
                print(f"   ✅ Tool {idx}: {item['title'][:45]}...")
    tools = valid_tools
    
    # Summarize startups
    valid_startups = []
    for idx, item in enumerate(startups, 1):
        if item.get("content"):
            summary = summarize_with_groq(item["content"], "startup")
            if summary:
                item["summary"] = summary
                valid_startups.append(item)
                print(f"   ✅ Startup {idx}: {item['title'][:45]}...")
    startups = valid_startups
    
    print(f"\n📊 Final Content Summary:")
    print(f"   Latest Developments: {len(developments)}")
    print(f"   AI Training: {len(training)}")
    print(f"   AI Research: {len(research)}")
    print(f"   AI Tools: {len(tools)}")
    print(f"   AI Startups: {len(startups)}")
    
    # Step 4: Save to database
    print("\n💾 Saving to database...")
    total_saved = 0
    total_saved += save_articles(developments, "development")
    total_saved += save_articles(training, "training")
    total_saved += save_articles(research, "research")
    total_saved += save_articles(tools, "tool")
    total_saved += save_articles(startups, "startup")
    print(f"   ✅ Saved {total_saved} new articles")
    
    # Step 5: Prepare newsletter data
    newsletter_data = {
        "developments": developments,
        "training": training,
        "research": research,
        "tools": tools,
        "startups": startups,
        
        # Metadata
        "recipient_name": os.getenv("RECIPIENT_NAME", "Student"),
        "feedback_url": os.getenv("FEEDBACK_URL", "#"),
        "unsubscribe_url": os.getenv("UNSUBSCRIBE_URL", "#"),
        "preferences_url": os.getenv("PREFERENCES_URL", "#"),
        "archive_url": os.getenv("ARCHIVE_URL", "#"),
    }
    
    # Step 6: Render HTML template
    print("\n🎨 Rendering newsletter template...")
    newsletter_html = render_newsletter(newsletter_data)
    
    # Save to output file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(OUTPUT_DIR, f"newsletter_{timestamp}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(newsletter_html)
    print(f"   ✅ Saved to: {output_path}")
    
    # Step 7: Send email
    print("\n📧 Sending newsletter...")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    subject = f"🤖 CSE(AI&ML) Weekly Newsletter - {datetime.now().strftime('%B %d, %Y')}"
    
    send_email(newsletter_html, subject)
    
    # Log newsletter delivery
    total_articles = len(developments) + len(training) + len(research) + len(tools) + len(startups)
    newsletter_id = log_newsletter_sent(subject, total_articles)
    
    print("\n" + "=" * 70)
    print(f"✅ Newsletter #{newsletter_id} sent successfully!")
    print(f"📊 Total Articles: {total_articles}")
    print("=" * 70)

if __name__ == "__main__":
    run_pipeline()
