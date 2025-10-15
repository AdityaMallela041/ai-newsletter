
# 🤖 CSE(AI&ML) Newsletter Automation System - v4.0

**Automated AI & Machine Learning Newsletter with Deep Search, AI Summaries & Brevo SMTP**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Brevo](https://img.shields.io/badge/Email-Brevo_SMTP-00A699.svg)](https://www.brevo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [What's New in v4.0](#whats-new-in-v40)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Brevo SMTP Setup](#brevo-smtp-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Sending Limits](#sending-limits)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Performance Metrics](#performance-metrics)
- [License](#license)

---

## 🎯 Overview

An intelligent newsletter automation system that curates AI & Machine Learning content from across the web, generates structured summaries using LLM, and delivers beautifully designed HTML newsletters via **Brevo SMTP** (formerly Sendinblue).

**Built for:** Department of Computer Science & Engineering (AI & ML)  
**Delivery Schedule:** Every Friday at 4 PM IST  
**Content Categories:** Latest Developments, Training, Research, Trending Tools, Startups  
**Email Delivery:** Brevo SMTP (300 emails/day on free tier)

---

## 🚀 What's New in v4.0

### **Major Improvements:**

#### **1. Brevo SMTP Integration**
- ✅ **Free tier:** 300 emails/day (perfect for demos)
- ✅ **Simple SMTP setup** (no API complexity)
- ✅ **Reliable delivery** (99%+ success rate)
- ✅ **Email tracking** (opens, clicks, bounces)
- ✅ **No credit card** required for free tier

#### **2. Deep Search Engine (60-90s search)**
- ✅ **10 results per category** (previously 3)
- ✅ **Advanced search depth** with Tavily API
- ✅ **Full content extraction** (4000 chars)
- ✅ **Guaranteed quality** (minimum 30 words)
- ✅ **Better image matching** (article's own image first)

#### **3. Structured AI Summaries**
- ✅ **Category-specific prompts** (Development, Training, Research, Startup)
- ✅ **Paragraph + Bullet Points + Conclusion** format
- ✅ **Side headings** ("Key Highlights", "What You'll Learn")
- ✅ **4-5 sentences** (more detailed)
- ✅ **Groq's Llama 3.1** for fast generation

#### **4. Enhanced Newsletter Design**
- ✅ **Less congested layout** (increased spacing)
- ✅ **Black section headers** for all categories
- ✅ **Interactive star rating** with color coding
- ✅ **Hover effects** showing labels (Excellent, Good, Poor)
- ✅ **Clean feedback section** (no gradient)

#### **5. Interactive Star Rating**
- 🟢 5 Stars = Green = "Excellent"
- 🔵 4 Stars = Blue = "Good"
- 🟡 3 Stars = Yellow = "Average"
- 🟠 2 Stars = Orange = "Poor"
- 🔴 1 Star = Red = "Very Poor"

---

## ✨ Features

### **Content Curation**
- 🔍 **Deep web search** (10+ sources per category)
- 📰 **4 content categories** with unique articles
- 🎥 **YouTube video detection** with embedded players
- 🖼️ **High-quality images** matched to each article
- 🔧 **4 trending AI tools** with descriptions

### **AI-Powered Summarization**
- 🤖 **Groq LLM** (Llama 3.1-8B-Instant)
- 📝 **Structured summaries** (intro + bullets + conclusion)
- 🎯 **Category-specific formatting**
- ⚡ **Fast generation** (2-3 seconds per summary)
- 🧹 **Clean output** (no meta phrases)

### **Email Delivery (Brevo SMTP)**
- 📧 **Brevo SMTP** integration
- 🆓 **Free tier:** 300 emails/day
- 💰 **Paid plans:** Starting $25/month for 20,000/month
- 👥 **Multi-recipient** support
- 📊 **Delivery tracking** and analytics
- ✅ **High deliverability** (99%+ inbox rate)

### **Newsletter Design**
- 🎨 **Modern, responsive HTML** template
- 📱 **Mobile-optimized** layout
- 🌟 **Interactive elements** (hover effects, star rating)
- 🎭 **Professional typography** (Inter font)
- 🖱️ **Color-coded feedback** system

### **Database Integration**
- 🗄️ **PostgreSQL storage**
- 📊 **Tracking metrics** (sends, opens, clicks)
- 📧 **Recipient management**
- 📈 **Analytics ready**

---

## 🏗️ System Architecture

```

┌─────────────────────────────────────────────────────┐
│              NEWSLETTER PIPELINE v4.0               │
└─────────────────────────────────────────────────────┘
│
┌───────────────┴───────────────┐
▼                               ▼
┌──────────────────┐         ┌──────────────────┐
│  DEEP SEARCH     │         │  AI SUMMARY      │
│  (Tavily API)    │────────▶│  (Groq LLM)      │
│  10 results/cat  │         │  Structured      │
└────────┬─────────┘         └────────┬─────────┘
│                            │
▼                            ▼
┌──────────────────────────────────────────────┐
│         HTML RENDERING (Jinja2)              │
│         Interactive Template                 │
└────────┬─────────────────────────────────────┘
│
▼
┌──────────────────┐         ┌──────────────────┐
│  DATABASE        │◀────────│  BREVO SMTP      │
│  (PostgreSQL)    │         │  Email Delivery  │
│  Archive \& Track │         │  300/day free    │
└──────────────────┘         └──────────────────┘

```

---

## 📦 Installation

### **Prerequisites**
- Python 3.9+
- PostgreSQL 12+
- Brevo account (free tier works!)

### **Step 1: Clone Repository**
```

git clone https://github.com/your-username/ai-newsletter.git
cd ai-newsletter

```

### **Step 2: Create Virtual Environment**
```

python -m venv venv

# Windows

venv\Scripts\activate

# macOS/Linux

source venv/bin/activate

```

### **Step 3: Install Dependencies**
```

pip install -r requirements.txt

```

**`requirements.txt`:**
```

python-dotenv>=1.0.0
requests>=2.31.0
jinja2>=3.1.2
psycopg2-binary>=2.9.9
groq>=0.4.0

```

---

## 📧 Brevo SMTP Setup

### **Step 1: Create Brevo Account**

1. Go to [Brevo.com](https://www.brevo.com)
2. Click **"Sign Up Free"**
3. Verify your email

### **Step 2: Get SMTP Credentials**

1. Login to Brevo Dashboard
2. Go to **Settings** → **SMTP & API**
3. Click **SMTP** tab
4. Click **"Create a new SMTP key"**
5. Name it "Newsletter Demo"
6. **Copy the key** (you can't see it again!)

You'll get:
```

SMTP Server: smtp-relay.brevo.com
Port: 587
Login: your-email@example.com
Password: [Your SMTP key]

```

### **Step 3: Verify Sender Email**

1. Go to **Senders & IP** → **Senders**
2. Click **"Add a sender"**
3. Enter your sender email
4. Check your inbox for verification email
5. Click verification link
6. ✅ Email verified!

### **Step 4: Create Emailer**

Create `newsletter/emailer.py`:

```


# newsletter/emailer.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(html_content, subject, recipients):
"""Send email using Brevo SMTP"""

    # Brevo SMTP Configuration
    SMTP_SERVER = "smtp-relay.brevo.com"
    SMTP_PORT = 587
    SMTP_LOGIN = os.getenv("BREVO_LOGIN")
    SMTP_PASSWORD = os.getenv("BREVO_SMTP_KEY")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_NAME = os.getenv("SENDER_NAME", "CSE(AI&ML) Newsletter")
    
    if not SMTP_LOGIN or not SMTP_PASSWORD:
        print("❌ Missing Brevo credentials in .env")
        return False
    
    try:
        print(f"📧 Sending to {len(recipients)} recipients via Brevo SMTP...")
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message["To"] = ", ".join(recipients)
        
        # Attach HTML
        html_part = MIMEText(html_content, "html", "utf-8")
        message.attach(html_part)
        
        # Send via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipients, message.as_string())
        
        print(f"✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ SMTP Error: {e}")
        return False
    ```

---

## ⚙️ Configuration

### **Create `.env` File**

```


# ============================================

# BREVO SMTP CONFIGURATION (Required)

# ============================================

BREVO_LOGIN=your-email@example.com
BREVO_SMTP_KEY=your-smtp-key-here

# Sender Information (must be verified in Brevo)

SENDER_EMAIL=newsletter@yourdomain.com
SENDER_NAME=CSE(AI\&ML) Newsletter

# Recipients (comma-separated, max 300/day on free tier)

RECIPIENT_EMAILS=student1@example.com,student2@example.com,student3@example.com

# ============================================

# API KEYS (Required)

# ============================================

TAVILY_API_KEY=tvly-your-key-here
GROQ_API_KEY=gsk_your-key-here

# ============================================

# DATABASE (Required)

# ============================================

DATABASE_URL=postgresql://username:password@localhost:5432/newsletter_db

# ============================================

# NEWSLETTER SETTINGS

# ============================================

SEND_EMAIL=true
RECIPIENT_NAME=Student

# Optional URLs

FEEDBACK_URL=https://yourdomain.com/feedback
UNSUBSCRIBE_URL=https://yourdomain.com/unsubscribe
PREFERENCES_URL=https://yourdomain.com/preferences
ARCHIVE_URL=https://yourdomain.com/archive

```

### **Database Setup**

```

-- Create database
CREATE DATABASE newsletter_db;

-- Create user
CREATE USER newsletter_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE newsletter_db TO newsletter_user;

```

Initialize tables:
```

python -m newsletter.database

```

---

## 🚀 Usage

### **Run Full Pipeline**

```

python -m newsletter.pipeline

```

### **Expected Output**

```

🔎 DEEP SEARCH MODE - Comprehensive Content Discovery
================================================================================
⏱️  Expected time: 60-90 seconds
📊 Searching 10 results per category

🔍 Deep searching: latest AI breakthroughs...
✅ Found 10 results, 15 images in 8.2s

[... more searches ...]

📊 DEEP SEARCH COMPLETE
================================================================================
Latest Developments: 📰 (347 words)
AI Training: 🎥 (156 words)
AI Research: 📰 (289 words)
AI Startups: 📰 (201 words)
Trending Tools: 4 tools
📈 Total: 4 articles (1 videos)

[3/7] Generating category-specific summaries...
🤖 Generating development summary...
✅ Generated 47 word summary

[7/7] Email delivery...
📧 Sending to 3 recipients via Brevo SMTP...
✅ Email sent successfully!

✅ NEWSLETTER COMPLETED!

```

### **Test Email Sending**

Create `test_email.py`:

```

from newsletter.emailer import send_email

html = """

<html>
<body style="font-family: Arial; padding: 20px;">
    ```
    <h1 style="color: #667eea;">🧪 Test Newsletter</h1>
    ```
    <p>This is a test from your newsletter system!</p>
</body>
</html>
"""

recipients = ["your-email@example.com"]
send_email(html, "Test Newsletter", recipients)

```

Run:
```

python test_email.py

```

---

## 📁 Project Structure

```

ai-newsletter/
├── newsletter/
│   ├── __init__.py
│   ├── pipeline.py          \# Main orchestration
│   ├── fetcher.py            \# Deep search (v4.0)
│   ├── summarizer.py         \# AI summaries (v4.0)
│   ├── emailer.py            \# Brevo SMTP (NEW)
│   ├── database.py           \# PostgreSQL
│   ├── templates.py          \# Template renderer
│   └── output/
│       └── newsletter_*.html
├── templates/
│   └── newsletter.html       \# Jinja2 template (v4.0)
├── .env                      \# Configuration
├── requirements.txt
├── README.md
└── test_email.py            \# Email testing

```

---

## 📊 Sending Limits

### **Brevo Free Tier:**

| Plan | Emails/Day | Emails/Month | Cost | Best For |
|------|------------|--------------|------|----------|
| **Free** | **300** | ~9,000 | $0 | **Demo, Testing** |
| **Starter** | ~667 | 20,000 | $25/mo | 100-600 students |
| **Business** | ~667 | 20,000 | $65/mo | Advanced features |

### **Recipient Calculations:**

```


# Demo (5-50 recipients) - FREE TIER ✅

RECIPIENT_EMAILS=s1@ex.com,s2@ex.com,s3@ex.com  \# 3 recipients

# Small class (100 students) - FREE TIER ✅

# Send once/week = 100 emails/week (well within 300/day)

# Medium class (300 students) - FREE TIER ✅

# Send once/week = 300 emails (exactly at limit)

# Large class (600 students) - STARTER PLAN (\$25/mo) 📈

# Need 600 emails/week = need paid plan

```

### **Best Practices:**

1. **Start with free tier** for demo/testing
2. **Verify all sender emails** in Brevo dashboard
3. **Monitor daily limits** in Brevo analytics
4. **Upgrade when needed** (600+ recipients)

---

## 🎨 Customization

### **Modify Search Queries**

Edit `newsletter/fetcher.py` (lines 45-60):

```

developments_results, dev_images, dev_answer = search(
"YOUR CUSTOM QUERY HERE",
max_results=10
)

```

### **Change Summary Style**

Edit `newsletter/summarizer.py` (lines 20-50):

```

prompts = {
"development": "YOUR CUSTOM PROMPT HERE",
\# ... other categories
}

```

### **Update Email Template**

Edit `templates/newsletter.html`:

- **Colors:** Search for `#667eea` (primary color)
- **Spacing:** Adjust `padding` values
- **Fonts:** Change `font-family`

---

## 🐛 Troubleshooting

### **Email Issues**

| Issue | Solution |
|-------|----------|
| "Authentication failed" | Check `BREVO_LOGIN` and `BREVO_SMTP_KEY` in `.env` |
| "Sender not verified" | Verify sender email in Brevo dashboard |
| "Daily limit exceeded" | You've sent 300 emails today. Wait 24h or upgrade |
| "Emails in spam" | Set up SPF/DKIM in Brevo → Senders & IP → Authentication |

### **Content Issues**

| Issue | Solution |
|-------|----------|
| "No content fetched" | Check `TAVILY_API_KEY` is valid |
| "Summary too short" | Content insufficient, using fallback excerpt |
| "No images" | Using placeholder images (normal) |

### **Database Issues**

```


# Check PostgreSQL is running

sudo systemctl status postgresql

# Start PostgreSQL

sudo systemctl start postgresql

# Test connection

psql -U newsletter_user -d newsletter_db

```

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| **Deep Search Time** | 60-90 seconds |
| **Summary Generation** | 2-3 seconds per article |
| **Total Pipeline** | ~90-120 seconds |
| **Email Delivery** | 99%+ success rate |
| **Search Results** | 10 per category |
| **Content Quality** | 30+ words guaranteed |

---

## 🔐 Security

- ✅ Never commit `.env` to Git
- ✅ Use environment variables for secrets
- ✅ Rotate API keys monthly
- ✅ Enable Brevo two-factor authentication
- ✅ Use separate database user
- ✅ Validate external inputs

---

## 📝 Changelog

### **v4.0 (October 2025)**
- ✨ **Brevo SMTP integration** (replaced SendGrid)
- ✨ Deep search with 10 results/category
- ✨ Structured AI summaries with bullets
- ✨ Interactive color-coded star rating
- ✨ Enhanced newsletter design
- 🐛 Fixed bullet alignment
- 🐛 Removed gradient from feedback
- 🐛 Fixed thumbnail/content matching

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👥 Contact

**Department of CSE (AI & ML)**  
📧 Email: newsletter@yourdomain.com  
🌐 Website: https://yourdomain.com  
💬 Issues: [GitHub Issues](https://github.com/your-username/ai-newsletter/issues)

---

## 🙏 Acknowledgments

- [Brevo](https://www.brevo.com) - SMTP email delivery
- [Tavily](https://tavily.com) - Deep web search API
- [Groq](https://groq.com) - Fast LLM inference
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Jinja2](https://jinja.palletsprojects.com/) - Templates

---

<div align="center">

**Made with ❤️ by CSE(AI&ML) Department**

⭐ **Star this repo if you find it helpful!**

📧 **Free tier: 300 emails/day** | 🚀 **Perfect for demos & small classes**

</div>


