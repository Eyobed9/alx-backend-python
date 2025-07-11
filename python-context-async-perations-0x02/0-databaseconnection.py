import sqlite3

class DatabaseConnection:
    def __init__(self, db):
        self.db = db
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
    

with DatabaseConnection("users.db") as conn: 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users") 
    results = cursor.fetchall()
    print(results)