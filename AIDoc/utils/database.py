import sqlite3

def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(f"Error updating database: {e}")
