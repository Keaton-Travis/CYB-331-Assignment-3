import sqlite3
from typing import Optional

def get_user_by_username(db_path: str, username: str) -> Optional[sqlite3.Row]:
    """
    Looks up a user in a SQLite database by their username.

    Args:
        db_path (str): The file path to the SQLite database.
        username (str): The username to look up.

    Returns:
        Optional[sqlite3.Row]: The row corresponding to the user if found,
                               or None if no user exists.
    """
    # Parameterized query to prevent SQL Injection vulnerabilities
    query = "SELECT * FROM users WHERE username = ?"
    
    with sqlite3.connect(db_path) as conn:
        # Access columns by name (e.g., user["email"]) rather than integer index
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, (username,))
        user_row = cursor.fetchone()
        
    return user_row