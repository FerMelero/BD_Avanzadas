"""
Authentication model: SQLite database for users and password hashes.

- Independent from PostgreSQL; used only for login.
- Passwords are stored hashed (Werkzeug); never plain text.
- Code in English.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

import bcrypt

from config import get_sqlite_db_path


# conexion a la BD sqlite
@contextmanager
def get_sqlite_connection():
    """Yield a connection to the auth SQLite database."""
    path = get_sqlite_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

# buscar al usuario
def get_user_by_username(username: str) -> sqlite3.Row | None:
    """Return the user row for the given username, or None if not found."""
    with get_sqlite_connection() as conn:
        cur = conn.execute(
            "SELECT id, username, password FROM usuarios WHERE username = ?;",
            (username.strip(),),
        )
        return cur.fetchone()


# por temas de consistencia con el dag, se usará bcrypt aquí también
def verify_password(username: str, password: str) -> bool:
    row = get_user_by_username(username)
    if not row:
        return False

    return bcrypt.checkpw(
        password.encode("utf-8"),
        row["password"].encode("utf-8")
    )

