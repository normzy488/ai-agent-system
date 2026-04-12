import sqlite3

DB_NAME = "agent.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_log(log_type, content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO logs (type, content) VALUES (?, ?)",
        (log_type, content)
    )

    conn.commit()
    conn.close()


def get_logs(limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT type, content, timestamp FROM logs ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows
