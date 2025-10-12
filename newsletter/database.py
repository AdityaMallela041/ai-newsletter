# newsletter/database.py
import sqlite3
from datetime import datetime

DB_FILE = "articles.db"

def init_db():
    """Initialize database with user view tracking"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Articles table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE,
            summary TEXT,
            content TEXT,
            image TEXT,
            video_id TEXT,
            source TEXT,
            published_date TEXT,
            category TEXT,
            score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Newsletters table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS newsletters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subject TEXT,
            total_articles INTEGER,
            status TEXT DEFAULT 'sent'
        )
    """)
    
    # User views table (tracks views per user per newsletter)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS newsletter_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newsletter_id INTEGER,
            user_email TEXT,
            viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newsletter_id) REFERENCES newsletters(id)
        )
    """)
    
    # User ratings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS newsletter_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newsletter_id INTEGER,
            user_email TEXT,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            feedback TEXT,
            rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newsletter_id) REFERENCES newsletters(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def save_articles(articles, category="development"):
    """Save articles with category"""
    if not articles:
        return 0
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    saved_count = 0
    
    for article in articles:
        try:
            cur.execute("""
                INSERT OR IGNORE INTO articles 
                (title, url, summary, content, image, video_id, source, published_date, category, score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.get("title"),
                article.get("url"),
                article.get("summary"),
                article.get("content"),
                article.get("image"),
                article.get("video_id"),
                article.get("source"),
                article.get("published_date"),
                category,
                article.get("score", 0.0)
            ))
            if cur.rowcount > 0:
                saved_count += 1
        except sqlite3.IntegrityError:
            continue
    
    conn.commit()
    conn.close()
    return saved_count

def log_newsletter_sent(subject, total_articles):
    """Log newsletter delivery"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO newsletters (subject, total_articles)
        VALUES (?, ?)
    """, (subject, total_articles))
    
    newsletter_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    return newsletter_id

def get_newsletter_stats(newsletter_id):
    """Get view count and average rating for a newsletter"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Get view count
    cur.execute("""
        SELECT COUNT(DISTINCT user_email) 
        FROM newsletter_views 
        WHERE newsletter_id = ?
    """, (newsletter_id,))
    view_count = cur.fetchone()[0] or 0
    
    # Get average rating
    cur.execute("""
        SELECT AVG(rating) 
        FROM newsletter_ratings 
        WHERE newsletter_id = ?
    """, (newsletter_id,))
    avg_rating = cur.fetchone()[0] or 0.0
    
    conn.close()
    
    return {
        "views": view_count,
        "avg_rating": round(avg_rating, 1)
    }
