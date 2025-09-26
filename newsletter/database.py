import sqlite3

DB_FILE = "articles.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            summary TEXT,
            image TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_articles(articles):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    for article in articles:
        cur.execute("INSERT INTO articles (title, url, summary, image) VALUES (?, ?, ?, ?)",
                    (article["title"], article["url"], article["summary"], article["image"]))
    conn.commit()
    conn.close()
