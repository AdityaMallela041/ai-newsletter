# newsletter/feedback_api.py

import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from newsletter.database import save_feedback, get_newsletter_stats, init_db

load_dotenv()

app = FastAPI(title="Newsletter Feedback API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Feedback API started successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "active",
        "service": "Newsletter Feedback API",
        "version": "1.0",
        "endpoints": {
            "submit_feedback": "/feedback",
            "stats": "/api/stats/{newsletter_id}"
        }
    }

@app.get("/feedback", response_class=HTMLResponse)
async def submit_feedback_via_url(
    request: Request,
    newsletter_id: int = Query(..., description="Newsletter ID"),
    email: str = Query(..., description="User email"),
    rating: int = Query(..., ge=1, le=5, description="Rating 1-5")
):
    """
    Simple URL-based feedback submission (works with email links)
    Example: http://localhost:8000/feedback?newsletter_id=1&email=user@test.com&rating=5
    """
    
    # Extract user agent and IP
    user_agent = request.headers.get("user-agent", "Unknown")
    ip_address = request.headers.get("x-forwarded-for")
    if ip_address:
        ip_address = ip_address.split(",")[0].strip()
    else:
        ip_address = request.client.host if request.client else "Unknown"
    
    # Save feedback to database
    success = save_feedback(
        newsletter_id=newsletter_id,
        user_email=email,
        rating=rating,
        comments=f"Rated via email link",
        user_agent=user_agent,
        ip_address=ip_address
    )
    
    # Return success page
    if success:
        return get_success_page(rating)
    else:
        return get_error_page()

@app.get("/api/stats/{newsletter_id}")
async def get_stats(newsletter_id: int):
    """Get newsletter statistics"""
    stats = get_newsletter_stats(newsletter_id)
    
    if not stats:
        return {"error": "Newsletter not found"}
    
    return stats


def get_success_page(rating: int):
    """Generate success HTML page"""
    rating_messages = {
        5: "Excellent! We're thrilled you loved it! 🌟",
        4: "Great! Thanks for the positive feedback! 👍",
        3: "Thanks for your feedback. We'll keep improving! 💪",
        2: "We appreciate your honesty. We'll do better! 🔧",
        1: "Sorry to hear that. We'll work harder! 🙏"
    }
    
    stars = "⭐" * rating
    message = rating_messages.get(rating, "Thank you for your feedback!")
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Feedback Received</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                background: white;
                padding: 50px 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 500px;
                width: 100%;
            }}
            .success-icon {{
                font-size: 80px;
                margin-bottom: 20px;
                animation: bounce 0.6s ease;
            }}
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-20px); }}
            }}
            h1 {{
                color: #10b981;
                margin-bottom: 15px;
                font-size: 32px;
            }}
            .stars {{
                font-size: 40px;
                margin: 20px 0;
            }}
            p {{
                color: #6b7280;
                font-size: 18px;
                line-height: 1.6;
            }}
            .close-btn {{
                margin-top: 30px;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }}
            .close-btn:hover {{
                transform: scale(1.05);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-icon">✅</div>
            <h1>Thank You!</h1>
            <div class="stars">{stars}</div>
            <p><strong>{message}</strong></p>
            <p>Your feedback helps us improve our newsletter content.</p>
            <button class="close-btn" onclick="window.close()">Close Window</button>
        </div>
    </body>
    </html>
    """


def get_error_page():
    """Generate error HTML page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                background: white;
                padding: 50px 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 500px;
            }}
            h1 {{
                color: #ef4444;
                margin-bottom: 15px;
            }}
            p {{
                color: #6b7280;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div style="font-size: 80px; margin-bottom: 20px;">❌</div>
            <h1>Oops!</h1>
            <p>Something went wrong. Please try again later.</p>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
