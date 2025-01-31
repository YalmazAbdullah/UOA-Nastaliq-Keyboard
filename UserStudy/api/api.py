from fastapi import FastAPI
import sqlite3
import random

app = FastAPI()

# Create SQLite database and table
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        data TEXT,
        condition TEXT
    )
""")
conn.commit()

# Experimental conditions
conditions = ["Condition A", "Condition B", "Condition C"]

@app.post("/register/")
def register_user(name: str, data: list[str]):
    condition = random.choice(conditions)  # Randomly assign a condition
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, data, condition) VALUES (?, ?, ?)", 
                   (name, str(data), condition))
    conn.commit()
    user_id = cursor.lastrowid
    return {"id": user_id, "condition": condition}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, data, condition FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        return {"name": user[0], "data": user[1], "condition": user[2]}
    return {"error": "User not found"}
