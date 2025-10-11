# newsletter/database.py
import sqlite3
from datetime import datetime

DB_FILE = "articles.db"

def init_db():
    """Initialize database with enhanced schema"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Enhanced articles table with metadata
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE,
            summary TEXT,
            content TEXT,
            image TEXT,
            source TEXT,
            published_date TEXT,
            article_type TEXT,
            score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Newsletter tracking table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS newsletters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            recipient_email TEXT,
            subject TEXT,
            status TEXT,
            total_articles INTEGER,
            views INTEGER DEFAULT 0,
            rating REAL DEFAULT 0.0
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def save_articles(articles, article_type="story"):
    """Save articles with metadata, avoiding duplicates"""
    if not articles:
        return 0
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    saved_count = 0
    
    for article in articles:
        try:
            cur.execute("""
                INSERT OR IGNORE INTO articles 
                (title, url, summary, content, image, source, published_date, article_type, score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.get("title"),
                article.get("url") or article.get("link"),
                article.get("summary"),
                article.get("content"),
                article.get("image"),
                article.get("source"),
                article.get("published_date"),
                article_type,
                article.get("score", 0.0)
            ))
            if cur.rowcount > 0:
                saved_count += 1
        except sqlite3.IntegrityError:
            continue
    
    conn.commit()
    conn.close()
    return saved_count

def log_newsletter_sent(recipient_email, subject, total_articles):
    """Log newsletter delivery"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO newsletters (recipient_email, subject, status, total_articles)
        VALUES (?, ?, ?, ?)
    """, (recipient_email, subject, "sent", total_articles))
    
    newsletter_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    return newsletter_id
