# -*- coding: utf-8 -*-
import os

from wikicrawler.wikicrawler.database import Database


def init_db():
    db = Database()

    try:
        db.db_connect()
        print("Connect to database!")
        db.create_tables()
        print("Tables was created success!")
    except Exception as exception:
        raise exception


def reset_db():
    os.system('cmds/reset_db.sh')
