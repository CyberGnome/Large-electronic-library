# -*- coding: utf-8 -*-
from database import Database
from exceptions import CrawlException


def init_db():
    db = Database()
    db.db_connect()
    if db.engine:
        db.create_tables()
    else:
        raise CrawlException("Tables was not created!", CrawlException.DATABASE_TABLE_DOESNT_CREATE)


def reset_db():
    pass

