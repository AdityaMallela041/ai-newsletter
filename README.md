# 📰 AI Newsletter Automation System

An automated newsletter generation system built for the **Department of CSE (AI & ML)** that fetches the latest news on Artificial Intelligence and Machine Learning, summarizes them using LLMs (Groq/Gemini), and sends a beautifully formatted newsletter every week.

---

## 🚀 Features

- 🔍 **Automated Content Fetching** – Uses Tavily API to gather the latest AI/ML news, events, and research.
- 🧠 **Smart Summarization** – Summaries generated using Groq’s LLaMA 3 or Gemini models.
- 📅 **Automated Scheduling** – Runs every Friday at 4 PM via CRON.
- 📬 **Email Delivery** – Automatically emails the generated newsletter using SendGrid.
- 💾 **Database Storage** – Stores all fetched and summarized articles for reference.
- 🎨 **Beautiful HTML Template** – Newsletter is styled like a professional tech bulletin.

---

## 🛠️ Tech Stack

| Component         | Technology Used            |
|------------------|---------------------------|
| Backend API      | FastAPI (Python)          |
| Scheduler        | APScheduler + CRON       |
| Content Fetching | Tavily API               |
| LLM Summarizer   | Groq LLaMA 3 / Gemini    |
| Database         | SQLite (via SQLAlchemy)  |
| Email Delivery   | SendGrid                 |
| Templating       | Jinja2 HTML templates    |

---

## 📁 Project Structure

```
ai-newsletter/
│
├─ newsletter/
│  ├─ fetcher.py         # Fetches latest AI/ML articles
│  ├─ summarizer.py      # Summarizes articles with LLM
│  ├─ templates.py       # Renders newsletter using Jinja2
│  ├─ emailer.py         # Sends email with SendGrid
│  ├─ database.py        # SQLite DB integration
│  └─ pipeline.py        # Main automation pipeline
│
├─ templates/
│  └─ newsletter.html    # HTML structure for newsletter
│
├─ .env                  # API keys (not committed)
├─ requirements.txt      # Dependencies
├─ README.md             # Documentation
└─ main.py               # FastAPI entrypoint (optional)
```

---

## 🔑 Environment Variables

Create a `.env` file with the following:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key   # optional
SENDGRID_API_KEY=your_sendgrid_api_key
SENDER_EMAIL=your_verified_sender_email
RECIPIENT_EMAIL=test@example.com
```

---

## ⚙️ Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/AdityaMallela041/ai-newsletter.git
cd ai-newsletter
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up your `.env`** with API keys.

5. **Run the pipeline:**

```bash
python -m newsletter.pipeline
```

6. **(Optional) Run the FastAPI server:**

```bash
uvicorn main:app --reload
```

---

## 🗓️ Scheduling with CRON

To run the pipeline every Friday at 4 PM:

```bash
0 16 * * FRI /path/to/venv/bin/python -m newsletter.pipeline
```

---

## 📬 Email Delivery (SendGrid)

- Go to [https://sendgrid.com](https://sendgrid.com) and create an account.
- Create an API key and add it to your `.env`.
- Verify your sender email before sending newsletters.

---

## 📜 Future Improvements

- 🔄 Add web dashboard for managing newsletters  
- 🧠 Integrate custom LLM models  
- 📊 Include trending research charts  
- 📰 Add PDF export support

---

## 👨‍💻 Author

**Aditya Mallela**  
Department of CSE (AI & ML)  
📧 [Email me](mailto:your.email@example.com)  

---

## 📝 License

This project is licensed under the MIT License. See `LICENSE` for details.
