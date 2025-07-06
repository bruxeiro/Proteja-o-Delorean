import sqlite3
from datetime import datetime

class DBProxy:
    def __init__(self, db_name: str = 'score.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY, name TEXT, score INTEGER, date TEXT)'''
        )
    def save(self, name: str, score: int):
        date = datetime.now().isoformat()
        self.conn.execute('INSERT INTO scores(name,score,date) VALUES(?,?,?)', (name,score,date))
        self.conn.commit()
    def retrieve_top10(self):
        cur = self.conn.execute('SELECT name,score,date FROM scores ORDER BY score DESC LIMIT 10')
        return cur.fetchall()
    def close(self):
        self.conn.close()