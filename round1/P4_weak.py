import hashlib
import os
import sqlite3

# Define the database file name
DB_NAME = "users.db"


def init_db():
  """Initializes the SQLite database and creates the users table if it doesn't exist."""
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)
  conn.commit()
  conn.close()


def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
  """Hashes a password using PBKDF2-HMAC-SHA256 with a secure random salt."""
  if salt is None:
    salt = os.urandom(16)  # Generate a 16-byte random salt

  # Hash the password with 100,000 iterations
  pwd_hash = hashlib.pbkdf2_hmac(
      "sha256", password.encode("utf-8"), salt, 100000
  )
  return pwd_hash.hex(), salt.hex()


def register_user(username: str, password: str):
  """Registers a new user and stores their username, password hash, and salt."""
  init_db()

  # Hash the password and get the hex representation along with the salt
  password_hash, salt = hash_password(password)

  try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insert user into the database
    cursor.execute(
        "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
        (username, password_hash, salt),
    )
    conn.commit()
    print(f"\n[Success] User '{username}' has been registered successfully!")

  except sqlite3.IntegrityError:
    print(f"\n[Error] The username '{username}' is already taken. Try another.")

  finally:
    conn.close()


if __name__ == "__main__":
  print("=== User Registration System ===")
  input_username = input("Enter username: ").strip()
  input_password = input("Enter password: ").strip()

  if not input_username or not input_password:
    print("[Error] Username and password cannot be empty.")
  else:
    register_user(input_username, input_password)