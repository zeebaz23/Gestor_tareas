import sqlite3

def create_connection():
    return sqlite3.connect('tasks.db')

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        text TEXT,
                        created_at TEXT DEFAULT (datetime('now', 'localtime')),
                        category TEXT,
                        status TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

create_tables()

