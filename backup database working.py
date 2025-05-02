# database.py
import sqlite3
from datetime import datetime

DATABASE_NAME = "meetings.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS meetings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  agenda TEXT,
                  transcript TEXT,
                  minutes TEXT,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                  is_draft BOOLEAN)''')
    conn.commit()
    conn.close()

def save_meeting(title, agenda, transcript, minutes, is_draft=0, meeting_id=None):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    if meeting_id:  # Update existing meeting
        c.execute('''UPDATE meetings 
                     SET title=?, agenda=?, transcript=?, minutes=?, is_draft=?
                     WHERE id=?''',
                  (title, agenda, transcript, minutes, is_draft, meeting_id))
    else:  # Insert new meeting
        c.execute('''INSERT INTO meetings 
                     (title, agenda, transcript, minutes, is_draft)
                     VALUES (?, ?, ?, ?, ?)''',
                  (title, agenda, transcript, minutes, is_draft))
    
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id if not meeting_id else meeting_id

def get_all_recordings():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''SELECT id, title, is_draft FROM meetings 
                 ORDER BY created_at DESC''')
    results = c.fetchall()
    conn.close()
    return results


def get_meeting_by_id(meeting_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''SELECT title, agenda, transcript, minutes 
                 FROM meetings WHERE id=?''', (meeting_id,))
    result = c.fetchone()
    conn.close()
    return result or (None, None, None, None)

def delete_meeting_by_id(meeting_id):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute('DELETE FROM meetings WHERE id=?', (meeting_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False