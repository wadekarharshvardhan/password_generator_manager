"""
database.py
-----------
SecureVault – Advanced Password Generator and Manager
SynthBay Solutions | Founder: Harshvardhan Wadekar

Manages all SQLite database operations for the SecureVault application.
Passwords are stored in ENCRYPTED form only — never in plaintext.

Schema:
    vault (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        website          TEXT NOT NULL,
        username         TEXT NOT NULL,
        encrypted_pass   TEXT NOT NULL,
        date_created     TEXT NOT NULL
    )
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional


# Default database file location (same directory as the script)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "securevault.db")


def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.

    Returns:
        sqlite3.Connection: Active database connection object.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn


def initialize_database() -> None:
    """
    Initialize the SQLite database and create the 'vault' table if it
    does not already exist. Called once at application startup.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                website        TEXT    NOT NULL,
                username       TEXT    NOT NULL,
                encrypted_pass TEXT    NOT NULL,
                date_created   TEXT    NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_entry(website: str, username: str, encrypted_pass: str) -> None:
    """
    Insert a new password entry into the vault table.

    Args:
        website (str): The website or service name.
        username (str): The username / email for the account.
        encrypted_pass (str): The AES-256 encrypted password token.

    Raises:
        ValueError: If any required field is empty.
    """
    if not website.strip():
        raise ValueError("Website field cannot be empty.")
    if not username.strip():
        raise ValueError("Username field cannot be empty.")
    if not encrypted_pass.strip():
        raise ValueError("Encrypted password cannot be empty.")

    # Capture current date/time at save time
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vault (website, username, encrypted_pass, date_created) VALUES (?, ?, ?, ?)",
            (website.strip(), username.strip(), encrypted_pass, date_created),
        )
        conn.commit()
    finally:
        conn.close()


def fetch_all_entries() -> List[Tuple]:
    """
    Retrieve all entries from the vault table, ordered by most recent first.

    Returns:
        List[Tuple]: A list of tuples (id, website, username, encrypted_pass, date_created).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, website, username, encrypted_pass, date_created FROM vault ORDER BY id DESC"
        )
        rows = cursor.fetchall()
        # Convert Row objects to plain tuples for easier unpacking
        return [tuple(row) for row in rows]
    finally:
        conn.close()


def delete_entry(entry_id: int) -> None:
    """
    Delete a specific password entry from the vault by its ID.

    Args:
        entry_id (int): The unique ID of the entry to delete.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vault WHERE id = ?", (entry_id,))
        conn.commit()
    finally:
        conn.close()


def search_entries(keyword: str) -> List[Tuple]:
    """
    Search entries in the vault by website or username (case-insensitive).

    Args:
        keyword (str): Search term to match against website or username.

    Returns:
        List[Tuple]: Matching entries as list of tuples.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        search_pattern = f"%{keyword.strip()}%"
        cursor.execute(
            """
            SELECT id, website, username, encrypted_pass, date_created
            FROM vault
            WHERE website LIKE ? OR username LIKE ?
            ORDER BY id DESC
            """,
            (search_pattern, search_pattern),
        )
        return [tuple(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_total_count() -> int:
    """
    Return the total number of stored password entries in the vault.

    Returns:
        int: Count of all records in the vault table.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vault")
        return cursor.fetchone()[0]
    finally:
        conn.close()
