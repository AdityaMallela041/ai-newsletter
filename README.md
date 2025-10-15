
# 📰 CSE(AI&ML) Newsletter Automation System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

An intelligent newsletter automation system that fetches, summarizes, and delivers the latest AI & Machine Learning news to the CSE(AI&ML) department every week.

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Configuration](#-configuration) • [Usage](#-usage)

</div>

---

## 🎯 Overview

The **CSE(AI&ML) Newsletter Automation System** is a fully automated pipeline that curates AI/ML content from across the web, generates intelligent summaries using LLMs, and delivers beautifully formatted newsletters to department stakeholders every Friday at 4 PM IST.

### Why This Project?

- ✅ **Saves Time**: Automates 5+ hours of manual content curation weekly
- ✅ **AI-Powered**: Uses Groq LLaMA 3 for intelligent summarization
- ✅ **Professional Design**: Newsletter styled like The Rundown AI
- ✅ **Categorized Content**: Organizes news into 5 distinct sections
- ✅ **Zero Maintenance**: Set it and forget it with CRON scheduling

---

## 🚀 Features

### Core Capabilities

- 🔍 **Smart Content Fetching**
  - Uses Tavily API for advanced web search
  - Fetches from 17+ sources across 5 categories
  - Extracts high-quality images and YouTube videos
  - Automatic source attribution and metadata

- 🧠 **AI-Powered Summarization**
  - Category-specific prompts for optimal results
  - Groq LLaMA 3.1-8B-Instant for fast processing
  - Fallback to Gemini for redundancy
  - Context-aware summaries (2-4 sentences each)

- 📊 **Categorized Content Sections**
  1. Latest Developments - Breaking AI/ML news
  2. AI Training - Courses, workshops, tutorials
  3. AI Research - Academic papers and findings
  4. AI Tools - New platforms and software
  5. New AI Startups - Emerging companies

- 🎨 **Professional Newsletter Design**
  - Responsive HTML template (680px width)
  - 16:9 aspect ratio images (no cutoff)
  - YouTube video embeds
  - Star-based rating system
  - Mobile-optimized layout

- 💾 **Database & Analytics**
  - SQLite database for article storage
  - User view tracking per newsletter
  - Rating collection and analysis
  - Duplicate content prevention

- 📧 **Flexible Email Delivery**
  - Support for SMTP, Gmail, SendGrid, Brevo
  - Bulk sending to multiple departments
  - Testing mode (no email sending)
  - Delivery status logging

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.10+ | Core automation logic |
| **Web Framework** | FastAPI | API endpoints (optional) |
| **Content Fetching** | Tavily API | AI-powered web search |
| **Summarization** | Groq LLaMA 3 | LLM-based summarization |
| **Templating** | Jinja2 | HTML newsletter rendering |
| **Database** | SQLite + SQLAlchemy | Article & analytics storage |
| **Email** | SMTP / SendGrid / Brevo | Newsletter delivery |
| **Scheduling** | APScheduler + CRON | Weekly automation |

---

## 📁 Project Structure

```

ai-newsletter/
│
├── newsletter/
│   ├── __init__.py
│   ├── fetcher.py          \# Tavily API integration \& content fetching
│   ├── summarizer.py       \# Groq LLM summarization
│   ├── database.py         \# SQLite database operations
│   ├── templates.py        \# Jinja2 template rendering
│   ├── emailer.py          \# Email delivery (multi-provider)
│   └── pipeline.py         \# Main automation pipeline
│
├── templates/
│   └── newsletter.html     \# Professional HTML newsletter template
│
├── newsletter/output/      \# Generated newsletters (HTML files)
│
├── .env                    \# Environment variables (not committed)
├── .gitignore
├── requirements.txt        \# Python dependencies
├── README.md
└── LICENSE

```

---

## 📋 Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)
- API Keys (see [Configuration](#-configuration))

---

## ⚙️ Installation

### 1. Clone the Repository

```

git clone https://github.com/AdityaMallela041/ai-newsletter.git
cd ai-newsletter

```

### 2. Create Virtual Environment

```


# Windows

python -m venv venv
venv\Scripts\activate

# Linux/Mac

python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```

pip install -r requirements.txt

```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```

cp .env.example .env  \# If example exists

# OR create manually:

touch .env

```

---

## 🔑 Configuration

### Required API Keys

Add these to your `.env` file:

```


# === API Keys ===

TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxx
GROQ_API_KEY=gsk-xxxxxxxxxxxxxxxxx

# === Email Configuration (Choose ONE) ===

# Option 1: College SMTP (Recommended - Ask IT Department)

SMTP_SERVER=smtp.vbithyd.ac.in
SMTP_PORT=587
SMTP_USERNAME=aiml@vbithyd.ac.in
SMTP_PASSWORD=your_password
SENDER_EMAIL=aiml@vbithyd.ac.in
RECIPIENT_EMAILS=cse@vbit.ac.in,ece@vbit.ac.in,eee@vbit.ac.in

# Option 2: Gmail SMTP (500 emails/day free)

# SMTP_SERVER=smtp.gmail.com

# SMTP_PORT=587

# SMTP_USERNAME=your_email@gmail.com

# SMTP_PASSWORD=your_app_password  \# Generate at myaccount.google.com/apppasswords

# SENDER_EMAIL=your_email@gmail.com

# RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com

# Option 3: SendGrid (100 emails/day free)

# SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxx

# SENDER_EMAIL=verified@yourdomain.com

# RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com

# === Control Flags ===

SEND_EMAIL=false  \# Set to 'true' for production
EMAIL_PROVIDER=smtp  \# smtp, gmail, or sendgrid

# === Optional Settings ===

RECIPIENT_NAME=Student
FEEDBACK_URL=https://forms.google.com/your-form
UNSUBSCRIBE_URL=https://yourdomain.com/unsubscribe
PREFERENCES_URL=https://yourdomain.com/preferences
ARCHIVE_URL=https://yourdomain.com/archive

```

### Getting API Keys

1. **Tavily API** (Content Fetching)
   - Sign up: https://tavily.com
   - Free tier: 1,000 searches/month
   - Get API key from dashboard

2. **Groq API** (AI Summarization)
   - Sign up: https://console.groq.com
   - Free tier: 14,400 requests/day
   - Generate API key

3. **Email Provider** (Choose one)
   - **College SMTP**: Contact IT department
   - **Gmail**: Enable 2FA, generate App Password
   - **SendGrid**: Free 100 emails/day
   - **Brevo**: Free 300 emails/day

---

## 🚀 Usage

### Testing Mode (No Emails Sent)

```


# Ensure SEND_EMAIL=false in .env

python -m newsletter.pipeline

```

**Output:**
- ✅ Fetches latest AI/ML content
- ✅ Generates summaries
- ✅ Saves to database
- ✅ Creates HTML file in `newsletter/output/`
- ⚠️ **Does NOT send emails**

### Production Mode (Sends Emails)

```


# Set SEND_EMAIL=true in .env

python -m newsletter.pipeline

```

**What Happens:**
1. Fetches 17+ articles across 5 categories
2. Summarizes using Groq LLaMA 3
3. Renders professional HTML template
4. Sends to all recipients
5. Logs delivery status to database

---

## 📅 Automated Scheduling

### Option 1: CRON (Linux/Mac)

```


# Edit crontab

crontab -e

# Add this line (runs every Friday at 4 PM IST)

0 16 * * FRI /path/to/venv/bin/python -m newsletter.pipeline

```

### Option 2: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly, Friday, 4:00 PM
4. Action: Start a Program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `-m newsletter.pipeline`
   - Start in: `C:\path\to\ai-newsletter`

---

## 📊 Database Schema

The system uses SQLite with 4 tables:

```

-- Articles table
articles (
id, title, url, summary, content, image, video_id,
source, published_date, category, score, created_at
)

-- Newsletters table
newsletters (
id, sent_date, subject, total_articles, status
)

-- User views tracking
newsletter_views (
id, newsletter_id, user_email, viewed_at
)

-- User ratings
newsletter_ratings (
id, newsletter_id, user_email, rating, feedback, rated_at
)

```

---

## 🎨 Newsletter Preview

The generated newsletter includes:

- **Header**: Purple gradient with branding
- **Summary Box**: Article count and breakdown
- **5 Content Sections**: Developments, Training, Research, Tools, Startups
- **Rich Media**: Images (16:9), YouTube embeds, infographics
- **Metadata**: Source badges, publish dates, read-more links
- **Engagement**: Star rating system, feedback button
- **Footer**: Department branding, unsubscribe links

---

## 🧪 Testing

### Test Individual Components

```


# Test content fetching

python -c "from newsletter.fetcher import fetch_articles; print(fetch_articles())"

# Test summarization

python -c "from newsletter.summarizer import summarize_with_groq; print(summarize_with_groq('AI text here', 'development'))"

# Test email (without sending)

# Set SEND_EMAIL=false in .env first

python -m newsletter.pipeline

```

### View Generated Newsletter

```


# Open latest generated file in browser

cd newsletter/output

# Double-click the newest .html file

```

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: No images displaying
- **Fix**: Check Tavily API quota, verify image URLs

**Issue**: Groq API timeout
- **Fix**: Reduce max_tokens or use fallback LLM

**Issue**: Email not sending
- **Fix**: Verify SMTP credentials, check firewall

**Issue**: Database locked
- **Fix**: Close other processes accessing `articles.db`

### Debug Mode

Add to `pipeline.py`:

```

import logging
logging.basicConfig(level=logging.DEBUG)

```

---

## 📈 Future Enhancements

- [ ] Web dashboard for newsletter preview
- [ ] Multi-language support
- [ ] PDF export functionality
- [ ] Custom content filtering
- [ ] Email open/click tracking
- [ ] RSS feed integration
- [ ] Slack/Teams integration

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Aditya Mallela**  
Department of Computer Science & Engineering (AI & ML)  
VNR Vignana Jyothi Institute of Engineering and Technology

- GitHub: [@AdityaMallela041](https://github.com/AdityaMallela041)
- Email: 22p61a6697@vbithyd.ac.in

---

## 🙏 Acknowledgments

- [Tavily](https://tavily.com) - AI-powered search API
- [Groq](https://groq.com) - Fast LLM inference
- [The Rundown AI](https://therundown.ai) - Newsletter design inspiration
- Department of CSE(AI&ML) - Project support

---

## 📞 Support

For issues or questions:

1. **Open an Issue**: [GitHub Issues](https://github.com/AdityaMallela041/ai-newsletter/issues)
2. **Email**: 22p61a6697@vbithyd.ac.in
3. **Documentation**: Check this README

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ by the CSE(AI&ML) Department

</div>
```


***

## **Additional Files to Add**

### **1. `.env.example`**

```env
# API Keys
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Email Configuration (SMTP)
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_password
SENDER_EMAIL=newsletter@example.com
RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com

# Control
SEND_EMAIL=false
EMAIL_PROVIDER=smtp

# Optional
RECIPIENT_NAME=Student
FEEDBACK_URL=#
UNSUBSCRIBE_URL=#
PREFERENCES_URL=#
ARCHIVE_URL=#
```


### **2. `LICENSE` (MIT License)**

```
MIT License

Copyright (c) 2025 Aditya Mallela

Permission is hereby granted, free of charge, to any person obtaining a copy...
(Full MIT license text)
