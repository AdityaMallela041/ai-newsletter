# feedback_api/app.py

"""Simple FastAPI for newsletter feedback collection"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from newsletter.database import save_feedback

app = FastAPI(title="VBIT Newsletter Feedback API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "active", "message": "VBIT Newsletter Feedback API"}


@app.get("/feedback", response_class=HTMLResponse)
def submit_feedback(newsletter_id: int, email: str, rating: int, request: Request):
    """Handle feedback submission from email links"""
    
    if not (1 <= rating <= 5):
        return get_error_page("Invalid rating. Must be 1-5 stars.")
    
    user_agent = request.headers.get('user-agent', 'Unknown')
    ip_address = request.client.host if request.client else 'Unknown'
    
    try:
        success = save_feedback(
            newsletter_id=newsletter_id,
            user_email=email,
            rating=rating,
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        if success:
            return get_thank_you_page(rating)
        else:
            return get_error_page("Failed to save feedback.")
    
    except Exception as e:
        print(f"Error: {e}")
        return get_error_page("Something went wrong.")


def get_thank_you_page(rating: int) -> str:
    """Beautiful thank you page"""
    
    stars = "⭐" * rating
    messages = {
        5: "Excellent! We're thrilled you loved it! 🎉",
        4: "Great! Thanks for the positive feedback! 😊",
        3: "Good! We'll keep improving! 💪",
        2: "Thanks! We'll do better! 🔧",
        1: "We appreciate your feedback! 📈"
    }
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You - VBIT Newsletter</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .card {{
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
        }}
        .emoji {{ font-size: 80px; margin-bottom: 20px; animation: bounce 1s ease; }}
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-20px); }}
        }}
        h1 {{ color: #002B5B; margin-bottom: 15px; }}
        .stars {{ font-size: 48px; color: #F97316; margin: 20px 0; }}
        p {{ color: #4B5563; font-size: 18px; line-height: 1.6; }}
        .small {{ font-size: 14px; color: #9CA3AF; margin-top: 25px; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="emoji">🎉</div>
        <h1>Thank You!</h1>
        <div class="stars">{stars}</div>
        <p><strong>{messages.get(rating)}</strong></p>
        <p class="small">Your feedback helps us improve our weekly AI & ML newsletter.</p>
    </div>
</body>
</html>
    """


def get_error_page(message: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }}
        .card {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #DC2626; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>⚠️ Oops!</h1>
        <p>{message}</p>
    </div>
</body>
</html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
