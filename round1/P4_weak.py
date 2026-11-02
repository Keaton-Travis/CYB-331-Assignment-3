import sqlite3

def register_user(username, password):
    # Connect to SQLite database (creates users.db if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Insert the username and password directly into the database
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    cursor.execute(query)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    print(f"User '{username}' registered successfully!")

if __name__ == "__main__":
    print("--- User Registration ---")
    user_input = input("Enter username: ")
    pass_input = input("Enter password: ")
    
    register_user(user_input, pass_input)