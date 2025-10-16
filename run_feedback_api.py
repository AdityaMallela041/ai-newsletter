# run_feedback_api.py

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Newsletter Feedback API")
    print("📍 URL: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("📊 Test: http://localhost:8000")
    print("=" * 50)
    
    # Use import string instead of app object for reload to work
    uvicorn.run(
        "newsletter.feedback_api:app",  # Import string format
        host="0.0.0.0",
        port=8000,
        reload=True,  # Now reload will work properly
        log_level="info"
    )
