from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "quotes.db"
QUOTES_FILE = "naglgol.txt"  # نام فایل نقل قول‌ها

@app.on_event("startup")
def startup():
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    ''')
    count = conn.execute('SELECT COUNT(*) FROM quotes').fetchone()[0]
    if count == 0:
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            quotes = [line.strip() for line in f if line.strip()]
        for q in quotes:
            conn.execute('INSERT INTO quotes (text) VALUES (?)', (q,))
        conn.commit()
    conn.close()

@app.get("/quote/random")
def get_random_quote():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT * FROM quotes').fetchall()
    conn.close()
    if not rows:
        return {"id": 0, "text": "هیچ نقل قولی موجود نیست."}
    row = random.choice(rows)
    return {"id": row["id"], "text": row["text"]}