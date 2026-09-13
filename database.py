import sqlite3

DB_NAME = "plagiarism.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Pairwise comparison results
    cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file1 TEXT,
        file2 TEXT,
        score REAL
    )
    """)

    # Analysis history
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        files_uploaded INTEGER,
        comparisons INTEGER,
        highest_similarity REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def insert_result(file1, file2, score):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO results (file1, file2, score)
    VALUES (?, ?, ?)
    """, (file1, file2, score))

    conn.commit()
    conn.close()

def insert_history(files_uploaded,
                   comparisons,
                   highest_similarity):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO history
    (
        files_uploaded,
        comparisons,
        highest_similarity
    )
    VALUES (?, ?, ?)
    """,
    (
        files_uploaded,
        comparisons,
        highest_similarity
    ))

    conn.commit()
    conn.close()

def get_history():

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute("""
    SELECT
        id,
        files_uploaded,
        comparisons,
        highest_similarity,
        created_at
    FROM history
    ORDER BY id DESC
    """).fetchall()

    conn.close()

    return rows

