# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import settings
from models import DeclarativeBase


class Database:
    def __init__(self):
        self.__database_url = URL(**settings.DATABASE)
        self.engine = None

    def db_connect(self):
        try:
            self.engine = create_engine(self.__database_url)
        except Exception as error:
            print("Can`t create engine: %s" % str(error))

    def create_tables(self):
        try:
            DeclarativeBase.metadata.create_all(self.engine)
        except Exception as error:
            print("Can`t create tables: %s" % str(error))
