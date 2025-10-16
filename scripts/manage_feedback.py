#!/usr/bin/env python3
"""Complete Feedback Management Tool for VBIT Newsletter"""

import os
import sys
import webbrowser
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to Python path so we can import newsletter modules
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from newsletter.database import (
    init_db, save_feedback, get_newsletter_stats, 
    save_newsletter, SessionLocal, Newsletter, Feedback
)

load_dotenv()

def test_feedback_url():
    """Generate and open test feedback URLs"""
    print("🌐 Testing Feedback URLs...")
    
    # Test URLs for different ratings
    base_url = "http://localhost:8000/feedback"
    test_email = "test@vbit.edu"
    newsletter_id = 1
    
    test_urls = []
    for rating in range(1, 6):
        url = f"{base_url}?newsletter_id={newsletter_id}&email={test_email}&rating={rating}"
        test_urls.append((rating, url))
        print(f"   {rating}⭐: {url}")
    
    print("\nWould you like to open these URLs in your browser to test?")
    choice = input("Enter 'y' to open URLs: ").lower()
    
    if choice == 'y':
        for rating, url in test_urls:
            print(f"Opening {rating}⭐ test URL...")
            webbrowser.open(url)
            input("Press Enter to continue to next rating...")

def view_all_feedback():
    """View all feedback in the database"""
    db = SessionLocal()
    try:
        print("📋 All Feedback in Database:")
        print("=" * 80)
        
        feedback_records = db.query(Feedback).all()
        
        if not feedback_records:
            print("No feedback records found.")
            return
            
        for feedback in feedback_records:
            print(f"ID: {feedback.feedback_id}")
            print(f"Newsletter: #{feedback.newsletter_id}")
            print(f"Rating: {'⭐' * feedback.rating} ({feedback.rating}/5)")
            print(f"Email: {feedback.recipient_email}")
            print(f"Comments: {feedback.comments or 'None'}")
            print(f"Submitted: {feedback.submitted_at}")
            print(f"IP: {feedback.ip_address}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error viewing feedback: {e}")
    finally:
        db.close()

def create_test_newsletter():
    """Create a test newsletter for feedback testing"""
    print("📰 Creating Test Newsletter...")
    
    title = f"Test Newsletter - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    content_html = """
    <html>
    <head><title>Test Newsletter</title></head>
    <body>
        <h1>Test Newsletter</h1>
        <p>This is a test newsletter for feedback testing.</p>
        <div>
            <p>Rate this newsletter:</p>
            <a href="http://localhost:8000/feedback?newsletter_id=__ID__&email=test@vbit.edu&rating=5">⭐⭐⭐⭐⭐</a>
        </div>
    </body>
    </html>
    """
    
    newsletter_id = save_newsletter(
        title=title,
        content_html=content_html,
        created_by_email="admin@vbit.edu"
    )
    
    if newsletter_id:
        print(f"✅ Test newsletter created with ID: {newsletter_id}")
        return newsletter_id
    else:
        print("❌ Failed to create test newsletter")
        return None

def simulate_realistic_feedback():
    """Add realistic feedback data"""
    print("🎭 Adding Realistic Feedback Data...")
    
    # Create test newsletter first
    newsletter_id = create_test_newsletter()
    if not newsletter_id:
        return
    
    # Realistic feedback data
    feedback_data = [
        ("aditya.student@vbit.edu", 5, "Excellent AI newsletter! Love the weekly updates."),
        ("priya.cse@vbit.edu", 4, "Very informative content about machine learning."),
        ("rahul.aiml@vbit.edu", 5, "The research section is particularly useful."),
        ("sneha.tech@vbit.edu", 3, "Good content but could be more beginner-friendly."),
        ("arjun.student@vbit.edu", 4, "Great resource for staying updated on AI trends."),
        ("kavya.cse@vbit.edu", 5, "The startup section provides great insights."),
        ("vikram.aiml@vbit.edu", 2, "Too technical for my current level."),
        ("anitha.student@vbit.edu", 4, "Helpful for my AI course studies."),
        ("ravi.tech@vbit.edu", 5, "Best AI newsletter I've subscribed to!"),
        ("meera.cse@vbit.edu", 3, "Content is good but emails are too long."),
    ]
    
    success_count = 0
    for email, rating, comments in feedback_data:
        success = save_feedback(
            newsletter_id=newsletter_id,
            user_email=email,
            rating=rating,
            comments=comments,
            user_agent="Chrome/120.0 (Test Data)",
            ip_address="192.168.1.100"
        )
        
        if success:
            success_count += 1
            print(f"   ✅ {email}: {rating}⭐")
        else:
            print(f"   ❌ {email}: Failed")
    
    print(f"\n✅ Added {success_count}/{len(feedback_data)} feedback records")
    
    # Show stats
    view_newsletter_stats(newsletter_id)

def view_newsletter_stats(newsletter_id):
    """View detailed statistics for a newsletter"""
    stats = get_newsletter_stats(newsletter_id)
    
    if not stats:
        print(f"No data found for Newsletter #{newsletter_id}")
        return
    
    print(f"\n📊 Newsletter #{newsletter_id} Statistics")
    print("=" * 50)
    print(f"Title: {stats['title']}")
    print(f"Created: {stats['sent_at'] or 'Not sent yet'}")
    print(f"Total Feedback: {stats['total_feedback']}")
    print(f"Average Rating: {stats['avg_rating']:.2f}⭐")
    print("\n📈 Rating Distribution:")
    
    total = stats['total_feedback']
    for i in range(5, 0, -1):
        count = stats['rating_breakdown'][f"{i}_stars"]
        percentage = (count / total * 100) if total > 0 else 0
        stars = "⭐" * i
        bar = "█" * int(percentage / 10)
        print(f"   {stars} ({i}): {count:2d} ({percentage:4.1f}%) {bar}")

def export_feedback_report():
    """Export feedback data to a simple report"""
    db = SessionLocal()
    try:
        print("📄 Generating Feedback Report...")
        
        # Get all feedback with newsletter info
        query = db.query(Feedback, Newsletter).join(Newsletter).all()
        
        if not query:
            print("No feedback data to export.")
            return
        
        report_file = f"feedback_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("VBIT AI & ML Newsletter - Feedback Report\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now()}\n\n")
            
            for feedback, newsletter in query:
                f.write(f"Newsletter: {newsletter.title}\n")
                f.write(f"Rating: {'⭐' * feedback.rating} ({feedback.rating}/5)\n")
                f.write(f"From: {feedback.recipient_email}\n")
                f.write(f"Date: {feedback.submitted_at}\n")
                f.write(f"Comments: {feedback.comments or 'None'}\n")
                f.write("-" * 40 + "\n")
        
        print(f"✅ Report exported to: {report_file}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    finally:
        db.close()

def main_menu():
    """Main interactive menu"""
    while True:
        print("\n🎯 VBIT Newsletter Feedback Manager")
        print("=" * 40)
        print("1. 🧪 Test feedback URLs in browser")
        print("2. 📊 View newsletter statistics") 
        print("3. 📋 View all feedback records")
        print("4. 🎭 Add realistic test data")
        print("5. 📰 Create test newsletter")
        print("6. 📄 Export feedback report")
        print("7. 🚀 Start feedback API server")
        print("8. ❌ Exit")
        
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "1":
            test_feedback_url()
        elif choice == "2":
            newsletter_id = int(input("Enter Newsletter ID: "))
            view_newsletter_stats(newsletter_id)
        elif choice == "3":
            view_all_feedback()
        elif choice == "4":
            simulate_realistic_feedback()
        elif choice == "5":
            create_test_newsletter()
        elif choice == "6":
            export_feedback_report()
        elif choice == "7":
            print("Starting feedback API server...")
            print("Run this command in a separate terminal:")
            print("python start_feedback_api.py")
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    print("🎯 VBIT Newsletter Feedback Management System")
    print("=" * 50)
    
    # Test database connection
    try:
        init_db()
        print("✅ Database connection successful!\n")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your PostgreSQL configuration in .env file")
        sys.exit(1)
    
    main_menu()