# newsletter/emailer.py

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Load environment variables
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "VBIT AI Newsletter <onboarding@resend.dev>")
SENDER_NAME = os.getenv("SENDER_NAME", "VBIT AI Newsletter")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "")


def send_email(newsletter_html: str, subject: str = None) -> bool:
    """
    Send newsletter to all recipients using Resend REST API
    Compatible with existing pipeline.py
    """
    
    # Validation
    if not RESEND_API_KEY:
        print("❌ Missing Resend API key (RESEND_API_KEY in .env)")
        return False
    
    if not RECIPIENT_EMAIL:
        print("❌ Missing recipient emails (RECIPIENT_EMAIL in .env)")
        return False
    
    # Default subject
    if not subject:
        subject = f"🤖 VBIT AI Newsletter - {datetime.now().strftime('%B %d, %Y')}"
    
    # Parse recipients
    recipients = [email.strip() for email in RECIPIENT_EMAIL.split(',') if email.strip()]
    
    if not recipients:
        print("❌ No valid recipients found")
        return False
    
    print(f"\n📧 Sending newsletter to {len(recipients)} recipients...")
    
    # Prepare API request
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": SENDER_EMAIL,
        "to": recipients,
        "subject": subject,
        "html": newsletter_html
    }
    
    try:
        # Send POST request to Resend API
        response = requests.post(url, json=payload, headers=headers)
        
        # Check response
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Email sent successfully!")
            print(f"   📬 To: {len(recipients)} recipients")
            print(f"   📝 Subject: {subject}")
            print(f"   🆔 Message ID: {data.get('id', 'N/A')}")
            return True
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            return False
    
    except Exception as e:
        print(f"   ❌ Error sending email: {str(e)}")
        return False


def send_test_email(newsletter_html: str, test_email: str, subject: str = None) -> bool:
    """
    Send test newsletter to a single email address
    """
    
    if not RESEND_API_KEY:
        print("❌ Missing Resend API key")
        return False
    
    # Default subject
    if not subject:
        subject = f"🧪 TEST: VBIT AI Newsletter - {datetime.now().strftime('%B %d, %Y')}"
    
    print(f"\n🧪 Sending test email...")
    
    # API request
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": SENDER_EMAIL,
        "to": [test_email],
        "subject": subject,
        "html": newsletter_html
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Test email sent!")
            print(f"   📬 To: {test_email}")
            print(f"   📝 Subject: {subject}")
            print(f"   🆔 Message ID: {data.get('id', 'N/A')}")
            return True
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            return False
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False


def send_email_batched(newsletter_html: str, subject: str = None, batch_size: int = 50) -> bool:
    """
    Send newsletter in batches
    """
    
    if not RESEND_API_KEY:
        print("❌ Missing Resend API key")
        return False
    
    if not RECIPIENT_EMAIL:
        print("❌ Missing recipient emails")
        return False
    
    # Default subject
    if not subject:
        subject = f"🤖 VBIT AI Newsletter - {datetime.now().strftime('%B %d, %Y')}"
    
    # Parse recipients
    recipients = [email.strip() for email in RECIPIENT_EMAIL.split(',') if email.strip()]
    
    if not recipients:
        print("❌ No valid recipients")
        return False
    
    # Calculate batches
    total_batches = (len(recipients) + batch_size - 1) // batch_size
    
    print(f"\n📧 Sending newsletter in {total_batches} batches...")
    print(f"   Total recipients: {len(recipients)}")
    print(f"   Batch size: {batch_size}")
    
    success_count = 0
    failed_count = 0
    
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Send in batches
    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        payload = {
            "from": SENDER_EMAIL,
            "to": batch,
            "subject": subject,
            "html": newsletter_html
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                success_count += len(batch)
                print(f"   ✅ Batch {batch_num}/{total_batches}: Sent to {len(batch)} recipients")
            else:
                failed_count += len(batch)
                print(f"   ❌ Batch {batch_num}/{total_batches} failed: {response.text}")
            
            # Small delay between batches
            import time
            if i + batch_size < len(recipients):
                time.sleep(0.5)
        
        except Exception as e:
            failed_count += len(batch)
            print(f"   ❌ Batch {batch_num}/{total_batches} error: {str(e)}")
    
    # Final summary
    print(f"\n🎉 Batch sending complete!")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {failed_count}")
    
    return failed_count == 0


# Backward compatibility
def send_to_contacts_list(newsletter_html: str, subject: str = None, list_id: int = None) -> bool:
    """Legacy function for compatibility"""
    print("ℹ️  Note: Using Resend instead of Brevo contact lists")
    return send_email(newsletter_html, subject)
