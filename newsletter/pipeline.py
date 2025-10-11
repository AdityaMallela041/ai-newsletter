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
    """Production newsletter pipeline with enhanced content processing"""
    print("=" * 60)
    print("🚀 CSE(AI&ML) Newsletter Pipeline - Starting")
    print("=" * 60)
    
    # Step 1: Initialize database
    init_db()
    
    # Step 2: Fetch content from Tavily
    print("\n📡 Fetching latest AI/ML content...")
    data = fetch_articles()
    
    featured = data.get("featured")
    stories = data.get("stories", [])
    quick_hits = data.get("quick_hits", [])
    trending_tools = data.get("trending_tools", [])
    events = data.get("events", [])
    
    # Step 3: Enhance with AI summaries
    print("\n🤖 Generating AI summaries...")
    
    # Summarize featured article
    if featured and featured.get("content"):
        summary = summarize_with_groq(featured["content"], section="featured")
        if summary:
            featured["summary"] = summary
            print(f"   ✅ Featured: {featured['title'][:50]}...")
        else:
            featured["summary"] = featured["content"][:300] + "..."
    
    # Summarize stories
    valid_stories = []
    for idx, story in enumerate(stories, 1):
        if story.get("content"):
            summary = summarize_with_groq(story["content"], section="story")
            if summary:
                story["summary"] = summary
                valid_stories.append(story)
                print(f"   ✅ Story {idx}: {story['title'][:40]}...")
            else:
                story["summary"] = story["content"][:200] + "..."
                valid_stories.append(story)
    stories = valid_stories
    
    # Summarize events
    valid_events = []
    for event in events:
        if event.get("content"):
            summary = summarize_with_groq(event["content"], section="events")
            if summary:
                event["summary"] = summary
                valid_events.append(event)
                print(f"   ✅ Event: {event['title'][:40]}...")
    events = valid_events
    
    print(f"\n📊 Content Summary:")
    print(f"   Featured: {1 if featured else 0}")
    print(f"   Stories: {len(stories)}")
    print(f"   Quick Hits: {len(quick_hits)}")
    print(f"   Trending Tools: {len(trending_tools)}")
    print(f"   Events: {len(events)}")
    
    # Step 4: Save to database
    print("\n💾 Saving to database...")
    total_saved = 0
    
    if featured:
        total_saved += save_articles([featured], "featured")
    total_saved += save_articles(stories, "story")
    total_saved += save_articles(events, "event")
    
    print(f"   ✅ Saved {total_saved} new articles")
    
    # Step 5: Convert events to highlights
    highlights = []
    if events:
        highlights = [
            {
                "icon": "📅",
                "title": e.get("title", ""),
                "link": e.get("link", "#")
            }
            for e in events
        ]
    
    # Step 6: Prepare newsletter data
    newsletter_data = {
        "featured": featured,
        "stories": stories,
        "quick_hits": quick_hits,
        "trending_tools": trending_tools,
        "highlights": highlights,
        "events": events,
        
        # Additional metadata
        "recipient_name": os.getenv("RECIPIENT_NAME", "Student"),
        "feedback_url": os.getenv("FEEDBACK_URL", "#"),
        "total_views": 0,
        "avg_rating": 0.0,
        "unsubscribe_url": os.getenv("UNSUBSCRIBE_URL", "#"),
        "preferences_url": os.getenv("PREFERENCES_URL", "#"),
        "archive_url": os.getenv("ARCHIVE_URL", "#"),
        "team_signature": "CSE(AI&ML) Newsletter Team",
    }
    
    # Step 7: Render HTML template
    print("\n🎨 Rendering newsletter template...")
    newsletter_html = render_newsletter(newsletter_data)
    
    # Save to output file
    output_path = os.path.join(OUTPUT_DIR, f"newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(newsletter_html)
    print(f"   ✅ Saved to: {output_path}")
    
    # Step 8: Send email
    print("\n📧 Sending newsletter...")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    subject = f"🤖 CSE(AI&ML) Weekly Newsletter - {datetime.now().strftime('%B %d, %Y')}"
    
    send_email(newsletter_html, subject)
    
    # Log newsletter delivery
    total_articles = (1 if featured else 0) + len(stories) + len(events)
    log_newsletter_sent(recipient_email, subject, total_articles)
    
    print("\n" + "=" * 60)
    print("✅ Newsletter pipeline completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
