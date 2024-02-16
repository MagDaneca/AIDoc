import sqlite3

def create_connection():
    conn = sqlite3.connect(r'C:\Users\MSI\Desktop\AIDoc\aidoc.db')
    return conn