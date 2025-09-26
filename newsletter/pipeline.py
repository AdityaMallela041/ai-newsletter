import os
from newsletter.fetcher import fetch_articles
from newsletter.summarizer import summarize_with_groq
from newsletter.database import init_db, save_articles
from newsletter.templates import render_newsletter
from newsletter.emailer import send_email

OUTPUT_DIR = "newsletter/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_pipeline():
    print("🔄 Starting AI Newsletter pipeline...")

    # Step 1: Init DB
    init_db()

    # Step 2: Fetch structured articles
    data = fetch_articles()
    featured, stories, events = data["featured"], data["stories"], data["events"]

    print(f"✅ Fetched {len(stories)} stories, {len(events)} events")

    # Step 3: Summarize & filter
    if featured:
        summary = summarize_with_groq(featured["content"], section="featured")
        if summary:
            featured["summary"] = summary
        else:
            featured = None  # drop if unusable

    valid_stories = []
    for s in stories:
        summary = summarize_with_groq(s["content"], section="story")
        if summary:
            s["summary"] = summary
            valid_stories.append(s)
    stories = valid_stories

    valid_events = []
    for e in events:
        summary = summarize_with_groq(e["content"], section="events")
        if summary:
            e["summary"] = summary
            valid_events.append(e)
    events = valid_events

    print(f"✅ Summaries generated → {len(stories)} stories, {len(events)} events kept")

    # Step 4: Save to DB (only valid items)
    all_articles = []
    if featured:
        all_articles.append(featured)
    all_articles.extend(stories)
    all_articles.extend(events)

    if all_articles:
        save_articles(all_articles)
        print(f"✅ Saved {len(all_articles)} articles to DB")
    else:
        print("⚠️ No valid articles to save")

    # Step 5: Render HTML
    newsletter_html = render_newsletter({
        "featured": featured,
        "stories": stories,
        "events": events,
    })
    output_path = os.path.join(OUTPUT_DIR, "newsletter.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(newsletter_html)
    print(f"✅ Newsletter saved to {output_path}")

    # Step 6: Send Email
    send_email(newsletter_html)


if __name__ == "__main__":
    run_pipeline()
