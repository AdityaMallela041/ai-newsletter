#!/usr/bin/env python3
"""Test feedback system and view feedback data"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to Python path so we can import newsletter modules
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from newsletter.database import init_db, save_feedback, get_newsletter_stats

load_dotenv()

def test_database_connection():
    """Test if database connection works"""
    try:
        init_db()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def simulate_feedback():
    """Add some test feedback"""
    try:
        # Test feedback data
        test_data = [
            (1, "student1@vbit.edu", 5, "Excellent newsletter!"),
            (1, "student2@vbit.edu", 4, "Very informative"),
            (1, "student3@vbit.edu", 5, "Love the AI updates"),
            (1, "student4@vbit.edu", 3, "Good content"),
        ]
        
        print("\n📝 Adding test feedback...")
        for newsletter_id, email, rating, comments in test_data:
            success = save_feedback(
                newsletter_id=newsletter_id,
                user_email=email,
                rating=rating,
                comments=comments
            )
            if success:
                print(f"   ✅ {email}: {rating}⭐")
            else:
                print(f"   ❌ Failed to save feedback for {email}")
        
        return True
    except Exception as e:
        print(f"❌ Error adding test feedback: {e}")
        return False

def view_feedback_stats(newsletter_id=1):
    """View feedback statistics"""
    try:
        print(f"\n📊 Feedback Statistics for Newsletter #{newsletter_id}:")
        stats = get_newsletter_stats(newsletter_id)
        
        if stats:
            print(f"   Title: {stats['title']}")
            print(f"   Total Feedback: {stats['total_feedback']}")
            print(f"   Average Rating: {stats['avg_rating']:.2f}⭐")
            print(f"   Rating Breakdown:")
            for i in range(5, 0, -1):
                count = stats['rating_breakdown'][f"{i}_stars"]
                stars = "⭐" * i
                print(f"     {stars} ({i}): {count} responses")
        else:
            print("   No data found for this newsletter ID")
            
    except Exception as e:
        print(f"❌ Error getting stats: {e}")

def manual_feedback_test():
    """Test feedback submission manually"""
    print("\n🧪 Testing Manual Feedback Submission...")
    
    newsletter_id = int(input("Enter Newsletter ID (default 1): ") or "1")
    email = input("Enter your email: ")
    rating = int(input("Enter rating (1-5): "))
    comments = input("Enter comments (optional): ") or None
    
    success = save_feedback(
        newsletter_id=newsletter_id,
        user_email=email,
        rating=rating,
        comments=comments,
        user_agent="Manual Test",
        ip_address="127.0.0.1"
    )
    
    if success:
        print("✅ Feedback saved successfully!")
        view_feedback_stats(newsletter_id)
    else:
        print("❌ Failed to save feedback")

if __name__ == "__main__":
    print("🧪 VBIT Newsletter Feedback Testing Tool")
    print("="*50)
    
    # Test database connection
    if not test_database_connection():
        print("\n⚠️  Please check your PostgreSQL configuration in .env file")
        exit(1)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Add test feedback data")
        print("2. View feedback statistics") 
        print("3. Submit manual feedback")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            simulate_feedback()
            view_feedback_stats(1)
        elif choice == "2":
            newsletter_id = int(input("Enter Newsletter ID to view (default 1): ") or "1")
            view_feedback_stats(newsletter_id)
        elif choice == "3":
            manual_feedback_test()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")