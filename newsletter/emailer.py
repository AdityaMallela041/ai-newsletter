# newsletter/emailer.py
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def send_email(newsletter_html: str, subject: str = None):
    """Send newsletter via SendGrid with enhanced error handling"""
    if not SENDGRID_API_KEY:
        print("❌ Missing SendGrid API key")
        print("   Set SENDGRID_API_KEY in .env file")
        return False
    
    if not SENDER_EMAIL or not RECIPIENT_EMAIL:
        print("❌ Missing sender or recipient email")
        return False
    
    # Default subject if not provided
    if not subject:
        from datetime import datetime
        subject = f"🤖 Weekly AI Newsletter - {datetime.now().strftime('%B %d, %Y')}"
    
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECIPIENT_EMAIL,
        subject=subject,
        html_content=newsletter_html
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        if response.status_code in [200, 201, 202]:
            print(f"   ✅ Email sent successfully!")
            print(f"   📬 To: {RECIPIENT_EMAIL}")
            print(f"   📝 Subject: {subject}")
            print(f"   📊 Status Code: {response.status_code}")
            return True
        else:
            print(f"   ⚠️ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error sending email: {e}")
        return False
