import sqlite3
import bcrypt

def register_user(db_path: str, username: str, password: str) -> bool:
    """
    Securely registers a user by hashing their password with bcrypt (work factor >= 12)
    and using parameterized SQL queries to prevent injection.
    
    Raises a sanitized exception on error to prevent database leakage.
    """
    if not username or not password:
        raise ValueError("Username and password cannot be empty.")

    # Convert password to bytes for bcrypt processing
    password_bytes = password.encode('utf-8')

    try:
        # Generate salt with a work factor (cost) of 12
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(password_bytes, salt)

        # Connect to the SQLite database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Ensure the users table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash BLOB NOT NULL
                )
            """)
            
            # Use parameterized queries (?) to prevent SQL injection
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            return True

    except sqlite3.IntegrityError:
        # Handle duplicate username or constraint violations gracefully
        raise ValueError("Registration failed: Username is already taken.") from None
    except Exception:
        # Catch any underlying database or unexpected errors and raise a sanitized 
        # exception to avoid leaking file paths, schema details, or raw SQL errors.
        raise RuntimeError("An unexpected error occurred during registration.") from None

# --- Example Usage ---
if __name__ == "__main__":
    db_name = "secure_users.db"
    try:
        register_user(db_name, "alice_smith", "SuperSecretPassword123!")
        print("User registered successfully!")
    except (ValueError, RuntimeError) as err:
        print(f"Error: {err}")