import sqlite3

class ExecuteQuery:
    def __init__(self, db, query, param):
        self.db = db
        self.query = query
        self.param = param
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        cursor = self.conn.cursor() 
        cursor.execute(self.query, (self.param,)) 
        results = cursor.fetchall()
        return results

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
    

with ExecuteQuery("users.db","SELECT * FROM users WHERE age > ?", 25) as result: 
    print(result)