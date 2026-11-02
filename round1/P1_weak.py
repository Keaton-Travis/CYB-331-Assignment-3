import sqlite3

def get_user_by_username(db_path, username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query executed directly via string formatting
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    user_row = cursor.fetchone()
    conn.close()
    
    return user_row