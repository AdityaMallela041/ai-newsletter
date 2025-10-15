# 🤖 CSE(AI&ML) Newsletter Automation System - v4.0

**Automated AI & Machine Learning Newsletter with Deep Search, Interactive Features & Brevo SMTP**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)](https://github.com)
[![Email](https://img.shields.io/badge/Email-Brevo%20SMTP-orange.svg)](https://brevo.com)

---

## 📋 Table of Contents

- [Overview](#overview)
- [What's New in v4.0](#whats-new-in-v40)
- [Features](#features)
- [Email Delivery System](#email-delivery-system)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

An intelligent newsletter automation system that curates AI & Machine Learning content from across the web, generates structured summaries using LLM, and delivers beautifully designed HTML newsletters to subscribers via **Brevo SMTP**.

**Built for:** Department of Computer Science & Engineering (AI & ML)  
**Delivery Schedule:** Every Friday at 4 PM IST  
**Content Categories:** Latest Developments, AI Training, Research Papers, Trending Tools, AI Startups  
**Email Service:** Brevo (formerly Sendinblue) SMTP

---

## 🚀 What's New in v4.0

### **Major Improvements:**

#### **1. Deep Search Engine (60-90s search)**
- ✅ **10 results per category** (previously 3)
- ✅ **Advanced search depth** with Tavily API
- ✅ **Full content extraction** (raw_content + fallbacks)
- ✅ **Guaranteed content quality** (minimum 30 words)
- ✅ **Multiple fallback strategies** for content
- ✅ **Better image matching** (article's own image prioritized)

#### **2. Structured AI Summaries**
- ✅ **Category-specific prompts** (Development, Training, Research, Startup)
- ✅ **Paragraph + Bullet Points + Conclusion** format
- ✅ **Side headings** ("Key Highlights", "What You'll Learn", etc.)
- ✅ **4-5 sentences** (more detailed than before)
- ✅ **Aggressive cleaning** (removes meta phrases like "here is a summary")
- ✅ **Uses Groq's Llama 3.1** for fast generation

#### **3. Enhanced Newsletter Design**
- ✅ **Less congested layout** (increased padding and spacing)
- ✅ **Black section headers** for all categories (including Tools)
- ✅ **Better bullet alignment** in header summary
- ✅ **Interactive star rating** with color coding
- ✅ **Hover effects** showing rating labels (Excellent, Good, Poor, etc.)
- ✅ **Clean feedback section** (removed gradient, added border)

#### **4. Interactive Star Rating System**
- ✅ **5-star hover system** with dynamic colors:
  - 🟢 5 Stars = Green = "Excellent"
  - 🔵 4 Stars = Blue = "Good"
  - 🟡 3 Stars = Yellow = "Average"
  - 🟠 2 Stars = Orange = "Poor"
  - 🔴 1 Star = Red = "Very Poor"
- ✅ **Real-time label updates** on hover
- ✅ **Smooth animations** and transitions

#### **5. Brevo SMTP Integration**
- ✅ **Professional email delivery** via Brevo SMTP
- ✅ **Free tier: 300 emails/day** (perfect for demos)
- ✅ **Reliable delivery rates** (98%+ success)
- ✅ **Email authentication** (SPF, DKIM support)
- ✅ **Delivery tracking** and analytics

---

## ✨ Features

### **Content Curation**
- 🔍 **Deep web search** across 10+ sources per category
- 📰 **4 main content categories** with unique articles
- 🎥 **YouTube video detection** with embedded players
- 🖼️ **High-quality images** matched to each article
- 🔧 **4 trending AI tools** with descriptions

### **AI-Powered Summarization**
- 🤖 **Groq LLM integration** (Llama 3.1-8B-Instant)
- 📝 **Structured summaries** with intro, bullets, and conclusion
- 🎯 **Category-specific formatting**
- ⚡ **Fast generation** (average 2-3 seconds per summary)
- 🧹 **Clean output** (no meta phrases or filler)

### **Newsletter Design**
- 🎨 **Modern, responsive HTML** template
- 📱 **Mobile-optimized** layout
- 🌟 **Interactive elements** (hover effects, star rating)
- 🎭 **Professional typography** (Inter font family)
- 🖱️ **Color-coded feedback** system

### **Database Integration**
- 🗄️ **PostgreSQL storage** for newsletters
- 📊 **Tracking metrics** (opens, clicks, feedback)
- 📧 **Recipient management**
- 📈 **Analytics dashboard** (future enhancement)

### **Email Delivery via Brevo**
- 📬 **Brevo SMTP integration** for reliable delivery
- 👥 **Multi-recipient support** (300 emails/day free)
- ✅ **Delivery logging** and error tracking
- 🔔 **Scheduled CRON execution** (Fridays at 4 PM)
- 📊 **Real-time delivery analytics**

---

## 📧 Email Delivery System

### **Brevo SMTP Integration**

| Plan | Daily Limit | Monthly Limit | Cost | Best For |
|------|-------------|---------------|------|----------|
| **Free** | **300 emails/day** | 9,000/month | $0 | Demos, Small Classes |
| **Starter** | **667 emails/day** | 20,000/month | $25/mo | Medium Classes |
| **Business** | **667+ emails/day** | 20,000+/month | $65/mo | Large Departments |

### **Features:**
- ✅ **High deliverability** (98%+ inbox placement)
- ✅ **Real-time tracking** (sent, delivered, opened, clicked)
- ✅ **Email authentication** (SPF, DKIM, DMARC)
- ✅ **Spam compliance** (CAN-SPAM, GDPR)
- ✅ **Professional templates** with HTML support

### **Perfect for:**
- 📚 **Academic newsletters** (student body up to 300)
- 🎓 **Department updates** (faculty and students)
- 🚀 **Demo purposes** (free tier covers most needs)

---

## 📦 Installation

### **Prerequisites**
- Python 3.9+
- PostgreSQL 12+
- Git
- Brevo account (free at [brevo.com](https://brevo.com))

### **Step 1: Clone Repository**
```bash
git clone https://github.com/your-username/ai-newsletter.git
cd ai-newsletter
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Set Up Brevo Account**
1. Go to [brevo.com](https://brevo.com) and create free account
2. Verify your email address
3. Go to **Profile** → **SMTP & API** → **SMTP**
4. Click **"Create a new SMTP key"**
5. **Copy and save the key** (you can't see it again!)
6. Go to **Senders & IP** → **Senders** → **Add a sender**
7. Verify your sender email address

### **Step 5: Set Up Environment Variables**

Create a `.env` file in the project root:

```env
# Brevo SMTP Configuration
BREVO_LOGIN=your-email@example.com
BREVO_SMTP_KEY=your-smtp-key-from-brevo

# Sender Information (must be verified in Brevo)
SENDER_EMAIL=newsletter@yourdomain.com
SENDER_NAME=CSE(AI&ML) Newsletter

# Recipients (comma-separated)
RECIPIENT_EMAILS=student1@example.com,student2@example.com,student3@example.com
RECIPIENT_NAME=Student

# API Keys
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# PostgreSQL Database
DATABASE_URL=postgresql://username:password@localhost:5432/newsletter_db

# URLs (optional)
FEEDBACK_URL=https://yourdomain.com/feedback
UNSUBSCRIBE_URL=https://yourdomain.com/unsubscribe
PREFERENCES_URL=https://yourdomain.com/preferences
ARCHIVE_URL=https://yourdomain.com/archive

# Newsletter Settings
SEND_EMAIL=false  # Set to 'true' for production
```

### **Step 6: Initialize Database**
```bash
python -m newsletter.database
```

---

## ⚙️ Configuration

### **API Keys Setup**

#### **1. Brevo SMTP (Email Delivery)**
1. Visit [brevo.com](https://brevo.com) and create account
2. Go to **Profile** → **SMTP & API** → **SMTP**
3. Create new SMTP key
4. Add to `.env`: `BREVO_SMTP_KEY=your-key`
5. **Important:** Verify your sender email in Brevo dashboard

#### **2. Tavily API (Content Search)**
1. Visit [tavily.com](https://tavily.com)
2. Sign up and get your API key
3. Add to `.env`: `TAVILY_API_KEY=tvly-xxx...`

#### **3. Groq API (AI Summaries)**
1. Visit [console.groq.com](https://console.groq.com)
2. Create account and generate API key
3. Add to `.env`: `GROQ_API_KEY=gsk_xxx...`

### **Database Configuration**

#### **PostgreSQL Setup**
```sql
-- Create database
CREATE DATABASE newsletter_db;

-- Create user
CREATE USER newsletter_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE newsletter_db TO newsletter_user;
```

Update `.env`:
```env
DATABASE_URL=postgresql://newsletter_user:your_password@localhost:5432/newsletter_db
```

---

## 🚀 Usage

### **Quick Test**

#### **Test Brevo Email Delivery:**
```python
# test_brevo.py
from newsletter.emailer import send_email

html_content = """
<html>
<body style="font-family: Arial; padding: 20px;">
    <h1 style="color: #667eea;">🤖 Test Newsletter</h1>
    <p>This is a test email from your newsletter system!</p>
    <p>✅ Brevo SMTP is working correctly!</p>
</body>
</html>
"""

recipients = ["your-email@example.com"]
subject = "🧪 Newsletter System Test"

success = send_email(html_content, subject, recipients)
print("✅ Check your inbox!" if success else "❌ Check configuration")
```

```bash
python test_brevo.py
```

### **Manual Execution**

#### **Run Complete Pipeline**
```bash
python -m newsletter.pipeline
```

#### **Test Individual Components**

**1. Test Content Fetching:**
```bash
python -c "from newsletter.fetcher import fetch_articles; print(fetch_articles())"
```

**2. Test Summarization:**
```bash
python -c "from newsletter.summarizer import summarize_with_groq; print(summarize_with_groq('Your content here', 'development'))"
```

### **Automated Scheduling (CRON)**

#### **Linux/macOS**
```bash
# Edit crontab
crontab -e

# Add this line (runs every Friday at 4 PM)
0 16 * * 5 cd /path/to/ai-newsletter && /path/to/venv/bin/python -m newsletter.pipeline
```

#### **Windows Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly (Friday at 4 PM)
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `-m newsletter.pipeline`
   - Start in: `C:\path\to\ai-newsletter`

---

## 📁 Project Structure

```
ai-newsletter/
├── newsletter/
│   ├── __init__.py
│   ├── pipeline.py          # Main orchestration
│   ├── fetcher.py            # Deep search & content extraction  
│   ├── summarizer.py         # AI-powered summaries
│   ├── emailer.py            # Brevo SMTP integration
│   ├── database.py           # PostgreSQL operations
│   ├── templates/
│   │   └── newsletter.html   # Interactive Jinja2 template
│   └── output/
│       └── newsletter_*.html # Generated newsletters
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── test_brevo.py            # Email testing script
└── LICENSE
```

---

## 🎨 Customization

### **Modify Search Queries**

Edit `newsletter/fetcher.py`:

```python
# Line 45-60: Customize search queries
developments_results, dev_images, dev_answer = search(
    "YOUR CUSTOM QUERY HERE",  # ← Change this
    max_results=10
)
```

### **Adjust Summary Length**

Edit `newsletter/summarizer.py`:

```python
# Line 95: Change max_tokens for longer/shorter summaries
"max_tokens": 500,  # ← Increase for longer summaries
```

### **Change Email Settings**

Edit `newsletter/emailer.py`:

```python
# SMTP Configuration
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
```

### **Update Newsletter Template**

Edit `newsletter/templates/newsletter.html`:

- **Colors:** Search for hex codes like `#667eea` (primary color)
- **Spacing:** Adjust padding values (e.g., `padding: 40px 32px;`)
- **Fonts:** Change `font-family: 'Inter'` to your preferred font
- **Star Rating Colors:** Modify the color mapping in JavaScript

---

## 🐛 Troubleshooting

### **Common Issues**

#### **1. "BREVO_SMTP_KEY not found"**
**Solution:** 
- Check `.env` file has correct key
- Regenerate SMTP key in Brevo dashboard
- Make sure no spaces around `=` in `.env`

#### **2. "Sender not verified" (Email)**
**Solution:**
- Go to Brevo → **Senders & IP** → **Senders**
- Add and verify your sender email
- Check verification email (may be in spam)

#### **3. "Daily limit exceeded" (Brevo)**
**Solution:**
- Free plan: 300 emails/day limit reached
- Wait 24 hours OR upgrade to paid plan
- Check usage in Brevo dashboard → **Statistics**

#### **4. "Connection refused" (Database)**
**Solution:** 
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql
```

#### **5. Emails going to spam**
**Solution:**
- Set up SPF/DKIM in Brevo → **Senders & IP** → **Authentication**
- Use verified domain instead of Gmail
- Ask recipients to whitelist your email
- Avoid spam trigger words in subject

### **Debugging Email Delivery**

**Check Brevo Dashboard:**
1. Login to Brevo
2. Go to **Statistics** → **Email**
3. Check **Sent**, **Delivered**, **Bounced** counts
4. View **Logs** for individual delivery status

**Test SMTP Connection:**
```python
import smtplib

try:
    server = smtplib.SMTP("smtp-relay.brevo.com", 587)
    server.starttls()
    server.login("your-email@example.com", "your-smtp-key")
    print("✅ SMTP connection successful")
    server.quit()
except Exception as e:
    print(f"❌ SMTP error: {e}")
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Deep Search Time** | 60-90 seconds |
| **Summary Generation** | 2-3 seconds per article |
| **Total Pipeline Time** | ~90-120 seconds |
| **Content Quality** | 30+ words guaranteed |
| **Search Results** | 10 per category |
| **Email Delivery Rate** | 98%+ (Brevo SMTP) |
| **Free Email Limit** | 300 emails/day |

---

## 📊 Email Capacity Planning

### **Subscriber Limits by Plan:**

| Subscribers | Recommended Plan | Daily Sends | Monthly Cost |
|-------------|------------------|-------------|--------------|
| **1-300** | Brevo Free | 300/day | **$0** |
| **301-600** | Brevo Starter | 667/day | **$25** |
| **600+** | Brevo Business | 667+/day | **$65** |

### **Use Cases:**
- 🎓 **Small class (50 students):** Free plan perfect
- 🏫 **Department (200 students):** Free plan works
- 🎯 **Multiple departments (500+ students):** Consider Starter plan
- 🚀 **University-wide (1000+ students):** Business plan recommended

---

## 🔐 Security Best Practices

- ✅ Never commit `.env` file to Git
- ✅ Use environment variables for all secrets
- ✅ Rotate SMTP keys regularly
- ✅ Use separate database user with limited permissions
- ✅ Enable Brevo two-factor authentication
- ✅ Validate all external inputs
- ✅ Use HTTPS for all webhook URLs
- ✅ Keep sender email verified and authenticated

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 Changelog

### **v4.0 (October 2025)**
- ✨ Deep search with 10 results per category
- ✨ Structured AI summaries with bullets and side headings
- ✨ Interactive color-coded star rating system
- ✨ Enhanced newsletter design with better spacing
- ✨ **Brevo SMTP integration** for reliable email delivery
- ✨ Better content quality guarantees (30+ words)
- 🐛 Fixed bullet alignment issues in header
- 🐛 Removed gradient from feedback section
- 🐛 Fixed thumbnail/content matching problems
- 🐛 Improved email deliverability and tracking

### **v3.0 (September 2025)**
- Initial release with basic functionality

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**Department of Computer Science & Engineering (AI & ML)**  
📧 Contact: newsletter@yourdomain.com  
🌐 Website: https://yourdomain.com

---

## 🙏 Acknowledgments

- [Brevo](https://brevo.com) - Professional email delivery platform
- [Tavily](https://tavily.com) - Deep web search API
- [Groq](https://groq.com) - Lightning-fast LLM inference
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [PostgreSQL](https://www.postgresql.org/) - Database system

---

## 📞 Support

For issues, questions, or suggestions:

- 📧 Email: support@yourdomain.com
- 🐛 GitHub Issues: [Create Issue](https://github.com/your-username/ai-newsletter/issues)
- 💬 Discord: [Join Server](https://discord.gg/your-server)
- 📖 Brevo Docs: [SMTP Guide](https://developers.brevo.com/docs/send-emails-with-smtp)

---

<div align="center">

**Made with ❤️ by CSE(AI&ML) Department**

⭐ Star this repo if you find it helpful!

**🚀 Ready for production with Brevo SMTP! 📧**

</div>