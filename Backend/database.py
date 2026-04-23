


import sqlite3
from typing import Optional


def init_db(conn: sqlite3.Connection):
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS teacher(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                pw TEXT NOT NULL,
                authkey TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students(
                first TEXT NOT NULL,
                last TEXT NOT NULL,
                pagerid TEXT NOT NULL UNIQUE,
                grade INTEGER NOT NULL,
                authkey TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages(
                msgid INTEGER PRIMARY KEY,
                sender TEXT NOT NULL,
                msgtype TEXT NOT NULL,
                content TEXT NOT NULL,
                grade INTEGER,
                pagerid TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS setuprequests(
                pagerid TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS newpagers(
                first TEXT NOT NULL,
                last TEXT NOT NULL,
                authkey TEXT NOT NULL,
                pagerid TEXT NOT NULL UNIQUE,
                grade INTEGER
            )
            """
        )


def get_teacher_pw(conn: sqlite3.Connection, username: str):
    with conn:
        pw = conn.execute(
            "SELECT pw FROM teacher WHERE username = ?",
            (username,)
        ).fetchone()
        return pw[0] if pw else None


def get_teacher_authkey(conn: sqlite3.Connection, username: str):
    with conn:
        authkey = conn.execute(
            "SELECT authkey FROM teacher WHERE username = ?",
            (username,)
        ).fetchone()
        return authkey[0] if authkey else None


def add_teacher(conn: sqlite3.Connection, username: str, hashpw: str, authkey: str):
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO teacher (username, pw, authkey) VALUES (?, ?, ?)",
            (username, hashpw, authkey)
        )


def remove_teacher(conn: sqlite3.Connection, username: str):
    with conn:
        conn.execute(
            "DELETE FROM teacher WHERE username = ?",
            (username,)
        )


def add_pager(conn: sqlite3.Connection, first: str, last: str, pagerid: str, grade: int, authkey: str):
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO students (first, last, pagerid, grade, authkey) VALUES (?, ?, ?, ?, ?)",
            (first, last, pagerid, grade, authkey)
        )


def add_pager_replace(conn: sqlite3.Connection, first: str, last: str, pagerid: str, grade: int, authkey: str):
    with conn:
        conn.execute(
            "INSERT OR REPLACE INTO students (first, last, pagerid, grade, authkey) VALUES (?, ?, ?, ?, ?)",
            (first, last, pagerid, grade, authkey)
        )


def remove_pager(conn: sqlite3.Connection, pagerid: str):
    with conn:
        conn.execute("DELETE FROM students WHERE pagerid = ?", (pagerid,))
        conn.execute("DELETE FROM messages WHERE pagerid = ? AND msgtype = 'pager'", (pagerid,))


def get_pagers(conn: sqlite3.Connection):
    with conn:
        pages = conn.execute("SELECT * FROM students").fetchall()
        return pages if pages else None


def add_message(conn: sqlite3.Connection, sender: str, msgtype: str, content: str, pagerid: Optional[str] = None, grade: Optional[int] = None):
    with conn:
        if pagerid:
            conn.execute(
                "INSERT INTO messages (sender, msgtype, content, pagerid) VALUES (?, ?, ?, ?)",
                (sender, msgtype, content, pagerid)
            )
        elif grade is not None:
            conn.execute(
                "INSERT INTO messages (sender, msgtype, content, grade) VALUES (?, ?, ?, ?)",
                (sender, msgtype, content, grade)
            )
        else:
            conn.execute(
                "INSERT INTO messages (sender, msgtype, content) VALUES (?, ?, ?)",
                (sender, msgtype, content)
            )


def remove_message(conn: sqlite3.Connection, msgid: str):
    with conn:
        conn.execute("DELETE FROM messages WHERE msgid = ?", (msgid,))


def get_messages(conn: sqlite3.Connection, pagerid: Optional[str] = None, grade: Optional[int] = None):
    with conn:
        if pagerid and grade is None:
            messages = conn.execute(
                """
                SELECT * FROM messages
                WHERE pagerid = ?
                   OR (msgtype = 'all' AND pagerid IS NULL)
                """,
                (pagerid,)
            ).fetchall()

        elif grade is not None and pagerid is None:
            messages = conn.execute(
                """
                SELECT * FROM messages
                WHERE (msgtype = 'grade' AND grade = ?)
                   OR (msgtype = 'all' AND pagerid IS NULL)
                """,
                (grade,)
            ).fetchall()

        elif grade is not None and pagerid:
            messages = conn.execute(
                """
                SELECT * FROM messages
                WHERE pagerid = ?
                   OR (msgtype = 'grade' AND grade = ?)
                   OR (msgtype = 'all' AND pagerid IS NULL)
                """,
                (pagerid, grade)
            ).fetchall()

        else:
            messages = conn.execute(
                """
                SELECT * FROM messages
                WHERE msgtype = 'all' AND pagerid IS NULL
                """
            ).fetchall()

        return messages


def get_pager_authkey(conn: sqlite3.Connection, pagerid: str):
    with conn:
        authkey = conn.execute(
            "SELECT authkey FROM students WHERE pagerid = ?",
            (pagerid,)
        ).fetchone()
        return authkey[0] if authkey else None


def add_setup_request(conn: sqlite3.Connection, pagerid: str):
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO setuprequests (pagerid) VALUES (?)",
            (pagerid,)
        )


def remove_setup_request(conn: sqlite3.Connection, pagerid: str):
    with conn:
        conn.execute("DELETE FROM setuprequests WHERE pagerid = ?", (pagerid,))


def add_new_pager_info(conn: sqlite3.Connection, pagerid: str, authkey: str, first: str, last: str, grade: str):
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO newpagers (first, last, authkey, pagerid, grade) VALUES (?, ?, ?, ?, ?)",
            (first, last, authkey, pagerid, grade)
        )


def get_setup_requests(conn: sqlite3.Connection):
    with conn:
        result = conn.execute("SELECT * FROM setuprequests").fetchall()
        return result if result else None


def remove_new_pager_info(conn: sqlite3.Connection, pagerid: str):
    with conn:
        conn.execute("DELETE FROM newpagers WHERE pagerid = ?", (pagerid,))


def get_new_pager_info(conn: sqlite3.Connection, pagerid: str):
    with conn:
        info = conn.execute(
            "SELECT first, last, authkey, pagerid, grade FROM newpagers WHERE pagerid = ?",
            (pagerid,)
        ).fetchone()
        return info if info else None