import sqlite3

def create_connection():
    conn = sqlite3.connect(r'AIDoc/aidoc.db')
    return conn
