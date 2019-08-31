# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from wikicrawler.wikicrawler import settings
from wikicrawler.wikicrawler.models import DeclarativeBase


class Database:
    def __init__(self):
        self.__database_url = URL(**settings.DATABASE)
        self.engine = None

    def db_connect(self):
        self.engine = create_engine(self.__database_url)

    def create_tables(self):
        DeclarativeBase.metadata.create_all(self.engine)
