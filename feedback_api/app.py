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
            user_email=email,  # Changed from email to user_email
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
    """Beautiful glassmorphism thank you page"""
    
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f5576c 50%, #4facfe 75%, #00f2fe 100%);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        @keyframes gradient {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .card {{
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 60px 50px;
            border-radius: 24px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            text-align: center;
            max-width: 500px;
            animation: slideUp 0.5s ease-out;
        }}
        @keyframes slideUp {{
            from {{ transform: translateY(30px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        .emoji {{ 
            font-size: 100px; 
            margin-bottom: 25px; 
            animation: bounce 1s ease infinite;
        }}
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-15px); }}
        }}
        h1 {{ 
            color: #002B5B; 
            margin-bottom: 20px; 
            font-size: 32px;
            font-weight: 900;
        }}
        .stars {{ 
            font-size: 56px; 
            color: #F97316; 
            margin: 25px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        p {{ 
            color: #1F2937; 
            font-size: 20px; 
            line-height: 1.6; 
            font-weight: 600;
        }}
        .small {{ 
            font-size: 15px; 
            color: #4B5563; 
            margin-top: 30px; 
            font-weight: 400;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="emoji">🎉</div>
        <h1>Thank You!</h1>
        <div class="stars">{stars}</div>
        <p>{messages.get(rating)}</p>
        <p class="small">Your feedback helps us improve our weekly AI & ML newsletter.</p>
    </div>
</body>
</html>
    """

def get_error_page(message: str) -> str:
    """Error page with glassmorphism"""
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
            background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 50px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            max-width: 500px;
        }}
        h1 {{ color: #DC2626; font-size: 48px; margin-bottom: 15px; }}
        p {{ color: #4B5563; font-size: 18px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>⚠️</h1>
        <h2 style="color: #DC2626; margin-bottom: 15px;">Oops!</h2>
        <p>{message}</p>
    </div>
</body>
</html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
