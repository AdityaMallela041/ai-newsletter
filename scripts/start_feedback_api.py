#!/usr/bin/env python3
"""Start the VBIT Newsletter Feedback API Server"""

import uvicorn
import sys
import os

# Add parent directory to Python path so we can import newsletter modules
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

if __name__ == "__main__":
    print("🚀 Starting VBIT Newsletter Feedback API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📍 Feedback endpoint: http://localhost:8000/feedback")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        uvicorn.run(
            "feedback_api.app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down feedback API server...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")