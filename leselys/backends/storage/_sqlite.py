# -*- coding: utf-8 -*-
import sqlite3

from _storage import Storage

class Sqlite(Storage):
    def __init__(self, **kwargs):
        if not kwargs.get('path'):
            raise Exception('Sqlite backend need path option')
        self.path = kwargs['path']
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()

    def __initialize(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not self.fetchone():
            self.c.execute("CREATE TABLE users (username text, password text);")
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feeds';")
        if not self.fetchone():
            self.c.execute("CREATE TABLE users (username text, password text);")
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stories';")
        if not self.fetchone():
            self.c.execute("CREATE TABLE users (username text, password text);")
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stories';")
        if not self.fetchone():
            self.c.execute("CREATE TABLE users (username text, password text);")
