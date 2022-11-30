import logging
import sqlite3

from typing import Union
from datetime import datetime, timedelta

class Vote():
    def __init__(self, app):
        self.__app = app
        
    def get_database(self):
        return self.__app.database()
    
    def get_latest_poll(self) -> Union[int, None]:
        """ 
            Return the latest poll id
        """
        database = self.get_database()
        cursor = database.cursor()
        
        try:
            cursor.execute("SELECT id FROM pools ORDER BY id DESC LIMIT 1")
            database.commit()     
        except sqlite3.Error as error:
            logging.error(error)
            return None
        
        return cursor.fetchone()[0]
    
    def get_poll_results(self, pool_id: int) -> Union[dict, None]:
        """ 
            Return the results of a specify pool.
        """
        
        database = self.get_database()
        cursor = database.cursor()
        
        try:
            cursor.execute("SELECT vote FROM poll_users WHERE poll_id = ?", (pool_id,))
            database.commit()     
        except sqlite3.Error as error:
            logging.error(error)
            return None
    
        pool_data = cursor.fetchall()
        
        total_votes = len(pool_data)
        yes_vote = no_vote = 0
        for data in pool_data:
            user_vote = data[0]
            if user_vote == "yes":
                yes_vote += 1
            elif user_vote == "no":
                no_vote += 1
        
        return {
            "yes": round((yes_vote / total_votes) * 100),
            "no": round((no_vote / total_votes) * 100)
        }
        
    
    def get_poll_running(self) -> int:
        """
            Return the latest pool running
        """
        
        database = self.get_database()
        cursor = database.cursor()
        cursor.execute("SELECT id FROM pools WHERE finished_at IS NULL")

        data = cursor.fetchone()
        return data[0] if data else None
    
    def get_expired_poll(self) -> int:
        """ 
            Return poll that is expired but not yet updated
        """
        
        database = self.get_database()
        cursor = database.cursor()
        cursor.execute("SELECT id FROM pools WHERE finished_at IS NULL and created_at < ?", ((datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"),))

        data = cursor.fetchone()
        return data[0] if data else None
    
    def update_poll_to_expired(self, pool_id: int) -> bool:
        """
            Update poll to expired
        """
        database = self.get_database()
        cursor = database.cursor()
        
        try:
            cursor.execute("UPDATE pools SET finished_at = ? WHERE id = ?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pool_id))
            database.commit()     
        except sqlite3.Error as error:
            logging.error(error)
            return False
        
        return True        
    
    def has_voted(self, voter_id: int, poll_id: int) -> bool:
        """
            Check if user has voted in poll
        """
        
        database = self.get_database()
        cursor = database.cursor()
        cursor.execute("SELECT id FROM poll_users WHERE voter_id = ? AND poll_id = ?", (voter_id, poll_id))

        data = cursor.fetchone()
        return bool(data)
    
    def vote(self, poll_id: int, author_id: int, vote: str) -> bool:
        """
            Vote in a specify poll
        """
        database = self.get_database()
        cursor = database.cursor()

        if vote not in ["yes", "no"]:
            return False

        try:
            cursor.execute("INSERT INTO poll_users (voter_id, poll_id, vote) VALUES (?, ?, ?)", (author_id, poll_id, vote))
            database.commit()     
        except sqlite3.Error as error:
            logging.error(error)
            return False

        return True
    
    def create_poll(self, question: str, author_id: int) -> bool:
        database = self.get_database()
        cursor = database.cursor()
        
        try:
            cursor.execute("INSERT INTO pools (question, author_id) VALUES (?, ?)", (question, author_id))
            database.commit()     
        except sqlite3.Error as error:
            logging.error(error)
            return False

        return True