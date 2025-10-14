# newsletter/pipeline.py
import os
from datetime import datetime
from newsletter.fetcher import fetch_articles
from newsletter.summarizer import summarize_with_groq
from newsletter.database import init_db, save_newsletter, log_newsletter_sent
from newsletter.templates import render_newsletter
from newsletter.emailer import send_email

OUTPUT_DIR = "newsletter/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_pipeline():
    """SIMPLIFIED: Pipeline for 1 article per category"""
    print("=" * 80)
    print("🚀 CSE(AI&ML) Newsletter Pipeline - FINAL v3.0")
    print("=" * 80)
    
    try:
        # Step 1: Database
        print("\n[1/7] Initializing PostgreSQL...")
        init_db()
        
        # Step 2: Fetch (1 per category + tools)
        print("\n[2/7] Fetching content...")
        data = fetch_articles()
        
        development = data.get("development")
        training = data.get("training")
        research = data.get("research")
        startup = data.get("startup")
        trending_tools = data.get("trending_tools", [])
        
        # DEBUG: Print tools
        print(f"\n🔧 DEBUG - Trending Tools: {len(trending_tools)}")
        for tool in trending_tools:
            print(f"   - {tool.get('name', 'Unknown')}")
        
        total = data.get("total_articles", 0)
        if total == 0:
            print("❌ No content fetched. Aborting.")
            return
        
        # Step 3: Summarize
        print(f"\n[3/7] Generating summaries for {total} articles...")
        
        if development and development.get("content"):
            summary = summarize_with_groq(development["content"], "story")
            if summary:
                development["summary"] = summary
                print(f"   ✅ Development: {development['title'][:50]}...")
        
        if training and training.get("content"):
            summary = summarize_with_groq(training["content"], "training")
            if summary:
                training["summary"] = summary
                print(f"   ✅ Training: {training['title'][:50]}...")
        
        if research and research.get("content"):
            summary = summarize_with_groq(research["content"], "research")
            if summary:
                research["summary"] = summary
                print(f"   ✅ Research: {research['title'][:50]}...")
        
        if startup and startup.get("content"):
            summary = summarize_with_groq(startup["content"], "startup")
            if summary:
                startup["summary"] = summary
                print(f"   ✅ Startup: {startup['title'][:50]}...")
        
        # Step 4: Prepare data
        print("\n[4/7] Preparing newsletter...")
        
        newsletter_data = {
            "development": development,
            "training": training,
            "research": research,
            "startup": startup,
            "trending_tools": trending_tools,  # PASS TOOLS
            "total_articles": total,
            "video_count": data.get("video_count", 0),
            "recipient_name": os.getenv("RECIPIENT_NAME", "Student"),
            "feedback_url": os.getenv("FEEDBACK_URL", "#"),
            "unsubscribe_url": os.getenv("UNSUBSCRIBE_URL", "#"),
            "preferences_url": os.getenv("PREFERENCES_URL", "#"),
            "archive_url": os.getenv("ARCHIVE_URL", "#"),
        }
        
        # Step 5: Render
        print("\n[5/7] Rendering HTML...")
        newsletter_html = render_newsletter(newsletter_data)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(OUTPUT_DIR, f"newsletter_{timestamp}.html")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(newsletter_html)
        print(f"   ✅ Saved: {output_path}")
        
        # Step 6: Save to database
        print("\n[6/7] Saving to database...")
        subject = f"🤖 CSE(AI&ML) Weekly Newsletter - {datetime.now().strftime('%B %d, %Y')}"
        sender_email = os.getenv("SENDER_EMAIL", "newsletter@vbit.ac.in")
        
        newsletter_id = save_newsletter(
            title=subject,
            content_html=newsletter_html,
            created_by_email=sender_email,
            total_articles=total
        )
        
        # Step 7: Email
        print("\n[7/7] Email delivery...")
        send_enabled = os.getenv("SEND_EMAIL", "false").lower() == "true"
        recipients = os.getenv("RECIPIENT_EMAILS", "").split(",")
        recipients = [e.strip() for e in recipients if e.strip()]
        
        if send_enabled and recipients:
            send_email(newsletter_html, subject, recipients)
            if newsletter_id:
                log_newsletter_sent(newsletter_id, recipients, "success")
        else:
            print(f"   ⚠️ Email DISABLED (testing mode)")
            print(f"   📬 Would send to: {len(recipients)} recipient(s)")
        
        # Summary
        print("\n" + "=" * 80)
        print("✅ NEWSLETTER COMPLETED!")
        print("=" * 80)
        print(f"\n📊 Statistics:")
        print(f"   Total Articles: {total}")
        print(f"   Videos: {data.get('video_count', 0)}")
        print(f"   Trending Tools: {len(trending_tools)}")
        print(f"   Newsletter ID: #{newsletter_id}")
        print(f"   Output: {output_path.split(os.sep)[-1]}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_pipeline()
