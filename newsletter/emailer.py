import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")


def send_email(newsletter_html: str):
    if not SENDGRID_API_KEY:
        print("❌ Missing SendGrid API key")
        return

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECIPIENT_EMAIL,
        subject="Weekly AI Newsletter 📰",
        html_content=newsletter_html
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Email sent! Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
