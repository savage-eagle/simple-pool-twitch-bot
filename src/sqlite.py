import sqlite3

class Sqlite():
    def __init__(self):
        self.__connection = None
        
    def connect(self):
        self.__connection = sqlite3.connect("poll_twitch.db", check_same_thread=False)
        
    def get_connection(self) -> sqlite3.Connection:
        return self.__connection
    
    def get_cursor(self) -> sqlite3.Cursor:
        return self.__connection.cursor()
        
    def initialize_database(self):
        cursor = self.get_cursor()
        
        with open('dump.sql', 'r') as sql_file:
            sql_script = sql_file.read()
    
        cursor.executescript(sql_script)
        self.get_connection().commit()