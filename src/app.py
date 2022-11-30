from twitchio.ext import commands
from decouple import config
from src.sqlite import Sqlite
from src.vote import Vote
from apscheduler.schedulers.background import BackgroundScheduler

import logging
import os
import sqlite3 
import pytz
import os
import time

os.environ['TZ'] = 'America/Chicago'

logging.getLogger('apscheduler.executors.default').propagate = False
logging.basicConfig(encoding='utf-8', level=logging.INFO)

class Bot(commands.Bot):

    def __init__(self):
        self.__database = Sqlite()
        self._init_database()
        self.__vote = Vote(self)
        
        super().__init__(
            token=config('TOKEN'),
            prefix='!',
            initial_channels=[config('CHANNEL_MONITORING')]
        )
        
        for file in sorted(os.listdir("src/cogs")):
            if file.endswith(".py"):
                self.load_module(f"src.cogs.{file[:-3]}")
                
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.clear_polls, 'interval', seconds=5, timezone='America/Sao_Paulo')
        scheduler.start()
        
    def clear_polls(self) -> bool:        
        poll_id = self.__vote.get_expired_poll()
        if not poll_id:
            return False
        
        self.__vote.update_poll_to_expired(poll_id)
        return True

    def _init_database(self):
        self.__database.connect()
        self.__database.initialize_database()
        
    def vote(self):
        return self.__vote

    def database(self) -> sqlite3.Connection:
        return self.__database.get_connection()

    async def event_ready(self):
        logging.info(f'Logged in as {self.nick} - {self.user_id}')