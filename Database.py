import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / 'notes.db'


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                header TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()


def add_note(header, text):
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with get_connection() as conn:
        cur = conn.execute(
            'INSERT INTO notes (header, text, created_at) VALUES (?, ?, ?)',
            (header, text, created_at)
        )
        conn.commit()
        return cur.lastrowid


def get_note(note_id):
    with get_connection() as conn:
        return conn.execute(
            'SELECT * FROM notes WHERE id = ?', (note_id,)
        ).fetchone()


def update_note(note_id, header=None, text=None):
    note = get_note(note_id)
    if note is None:
        return False
    new_header = header if header is not None else note['header']
    new_text = text if text is not None else note['text']
    with get_connection() as conn:
        conn.execute(
            'UPDATE notes SET header = ?, text = ? WHERE id = ?',
            (new_header, new_text, note_id)
        )
        conn.commit()
    return True


def delete_note(note_id):
    with get_connection() as conn:
        cur = conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        return cur.rowcount > 0


def get_all_notes(sort_by='id', descending=False):
    # Whitelist sort columns to prevent SQL injection
    valid_sorts = {
        'id': 'id',
        'name': 'header',
        'header': 'header',
        'date': 'created_at',
        'created_at': 'created_at',
    }
    column = valid_sorts.get(sort_by.lower(), 'id')
    direction = 'DESC' if descending else 'ASC'
    with get_connection() as conn:
        return conn.execute(
            f'SELECT * FROM notes ORDER BY {column} {direction}'
        ).fetchall()
