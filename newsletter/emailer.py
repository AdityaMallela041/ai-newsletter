# newsletter/emailer.py

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Gmail SMTP Configuration
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "")


def send_email(newsletter_html: str, subject: str = None) -> bool:
    """
    Send newsletter using Gmail SMTP
    NO domain verification, NO authorization needed!
    """
    
    # Validation
    if not GMAIL_USER:
        print("❌ Missing Gmail address (GMAIL_USER in .env)")
        return False
    
    if not GMAIL_APP_PASSWORD:
        print("❌ Missing Gmail app password (GMAIL_APP_PASSWORD in .env)")
        print("   Generate one at: https://myaccount.google.com/apppasswords")
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
        print("❌ No valid recipient emails found")
        return False
    
    if len(recipients) > 100:
        print("⚠️ Warning: Gmail allows max 100 recipients per email")
        print(f"   You have {len(recipients)} recipients. Truncating to first 100.")
        recipients = recipients[:100]
    
    print(f"📧 Sending newsletter to {len(recipients)} recipients via Gmail...")
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"VBIT AI Newsletter <{GMAIL_USER}>"
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        
        # Attach HTML content
        html_part = MIMEText(newsletter_html, 'html')
        msg.attach(html_part)
        
        # Connect to Gmail SMTP
        print("   🔗 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        print("   🔐 Authenticating...")
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        
        # Send email
        print("   📤 Sending email...")
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully via Gmail!")
        print(f"   Sent to: {len(recipients)} recipients")
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail authentication failed")
        print("   1. Make sure 2-Step Verification is ON")
        print("   2. Generate new App Password at: https://myaccount.google.com/apppasswords")
        print("   3. Use the 16-character password (remove spaces)")
        return False
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def send_test_email(test_recipient: str) -> bool:
    """Send a test email"""
    
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("❌ Missing Gmail credentials in .env")
        return False
    
    test_html = """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px;">
            <h1 style="color: #667eea;">🤖 Test Newsletter</h1>
            <p style="font-size: 16px; line-height: 1.6;">
                This is a test email from your VBIT newsletter system!
            </p>
            <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <p style="margin: 0; color: #065f46; font-weight: 600;">
                    ✅ Gmail SMTP is working correctly!
                </p>
                <p style="margin: 10px 0 0 0; color: #065f46;">
                    ✨ No domain verification needed<br>
                    ✨ No recipient authorization needed<br>
                    ✨ Works instantly!
                </p>
            </div>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
            <p style="color: #6b7280; font-size: 14px;">
                Sent via Gmail SMTP | VBIT CSE(AI&ML) Newsletter
            </p>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"VBIT AI Newsletter <{GMAIL_USER}>"
        msg['To'] = test_recipient
        msg['Subject'] = "🧪 VBIT Newsletter System Test"
        
        msg.attach(MIMEText(test_html, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Test email sent to {test_recipient}")
        print("   Check your inbox!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def send_to_contacts_list(html_content: str, subject: str = None, recipient_list: list = None) -> bool:
    """Legacy function for backward compatibility"""
    if recipient_list:
        global RECIPIENT_EMAIL
        old_recipients = RECIPIENT_EMAIL
        RECIPIENT_EMAIL = ",".join(recipient_list)
        result = send_email(html_content, subject)
        RECIPIENT_EMAIL = old_recipients
        return result
    else:
        return send_email(html_content, subject)


if __name__ == "__main__":
    print("🧪 Testing Gmail SMTP Integration...")
    print("=" * 60)
    
    if not GMAIL_USER:
        print("❌ GMAIL_USER not found in .env")
        print("   Please add: GMAIL_USER=your-email@gmail.com")
    elif not GMAIL_APP_PASSWORD:
        print("❌ GMAIL_APP_PASSWORD not found in .env")
        print("\n📝 How to get Gmail App Password:")
        print("   1. Go to: https://myaccount.google.com/security")
        print("   2. Enable '2-Step Verification'")
        print("   3. Search for 'App passwords'")
        print("   4. Select 'Mail' and 'Other (Custom name)'")
        print("   5. Copy the 16-character password")
        print("   6. Add to .env as: GMAIL_APP_PASSWORD=abcdefghijklmnop (no spaces)")
    else:
        print(f"✅ Gmail: {GMAIL_USER}")
        print(f"✅ App Password: {'*' * len(GMAIL_APP_PASSWORD)}")
        print()
        
        test_email = input("Enter test email address: ")
        if test_email:
            send_test_email(test_email)
        else:
            print("⚠️ No email provided")
