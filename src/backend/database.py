"""Database layer for Task 2 - manages SQLite submissions storage."""
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import threading

DB_PATH = Path(__file__).parent / "submissions.db"
_lock = threading.Lock()


def init_db():
    """Initialize the database with submissions table."""
    with _lock:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating INTEGER NOT NULL,
                review TEXT NOT NULL,
                ai_response TEXT,
                ai_summary TEXT,
                ai_recommended_action TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()


def add_submission(
    rating: int,
    review: str,
    ai_response: str,
    ai_summary: str,
    ai_recommended_action: str
) -> int:
    """Add a new submission and return its ID."""
    with _lock:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO submissions (rating, review, ai_response, ai_summary, ai_recommended_action)
            VALUES (?, ?, ?, ?, ?)
        """, (rating, review, ai_response, ai_summary, ai_recommended_action))
        submission_id = cursor.lastrowid
        conn.commit()
        conn.close()
    return submission_id


def get_all_submissions() -> List[Dict]:
    """Retrieve all submissions ordered by newest first."""
    with _lock:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, rating, review, ai_response, ai_summary, ai_recommended_action, created_at
            FROM submissions
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
    return [dict(row) for row in rows]


def get_submission_by_id(submission_id: int) -> Optional[Dict]:
    """Retrieve a single submission by ID."""
    with _lock:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, rating, review, ai_response, ai_summary, ai_recommended_action, created_at
            FROM submissions
            WHERE id = ?
        """, (submission_id,))
        row = cursor.fetchone()
        conn.close()
    return dict(row) if row else None


def get_analytics() -> Dict:
    """Compute simple analytics from all submissions."""
    with _lock:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM submissions")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(rating) as avg_rating FROM submissions")
        avg_rating = cursor.fetchone()[0] or 0.0
        cursor.execute("SELECT rating, COUNT(*) as count FROM submissions GROUP BY rating")
        rating_dist = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
    return {
        "total_submissions": total,
        "average_rating": round(avg_rating, 2),
        "rating_distribution": rating_dist
    }


# Initialize DB on import
init_db()
