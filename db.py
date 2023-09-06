import sqlite3
from sqlite3 import Error
import os

class DB:
    def __init__(self):
        self.db_path = 'user_data.db'

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except Error as e:
            print(e)
            return None

    def init_db(self):
        if not os.path.exists(self.db_path):
            conn = self.create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS user_data
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                telegram_id INTEGER UNIQUE,
                                wear_device_model TEXT,
                                symbol_capacity TEXT)''')
                conn.commit()
                conn.close()

    def set_symbol_capacity(self, symbol_capacity, user_id):
        try:
            conn = self.create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user_data SET symbol_capacity = ? WHERE telegram_id = ?", (symbol_capacity, user_id))
                conn.commit()
                conn.close()
        except Error as e:
            print(e)

    def get_symbol_capacity(self, user_id):
        try:
            conn = self.create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT symbol_capacity FROM user_data WHERE telegram_id = ?", (user_id,))
                symbol_capacity = cursor.fetchone()
                conn.close()
                if symbol_capacity:
                    return int(symbol_capacity[0])
                else:
                    return None
        except Error as e:
            print(e)
