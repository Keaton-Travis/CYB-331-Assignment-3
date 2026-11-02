import re
import sqlite3
from typing import Optional, Tuple, Any


def get_user_by_username(
    conn: sqlite3.Connection, username: str
) -> Optional[Tuple[Any, ...]]:
  """Looks up a user by username in the database securely.

  Args:
      conn: An active sqlite3.Connection object.
      username: The username string to search for.

  Returns:
      A tuple representing the database row if found, or None otherwise.

  Raises:
      ValueError: If the username does not meet validation requirements.
  """
  # Validate: Must be strictly alphanumeric and between 3 and 32 characters long
  if not isinstance(username, str) or not re.match(
      r"^[a-zA-Z0-9]{3,32}$", username
  ):
    raise ValueError("Invalid username provided.")

  cursor = conn.cursor()

  # Use a parameterized query (?) to protect against SQL injection.
  # SQLite safely treats the second argument as data, never as executable code.
  query = "SELECT * FROM users WHERE username = ?"
  cursor.execute(query, (username,))

  row = cursor.fetchone()
  return row