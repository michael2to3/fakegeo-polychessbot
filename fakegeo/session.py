import sqlite3
from sqlite3 import Connection, Cursor
from typing import Iterable

from telethon import TelegramClient

from type import Api, UserInfo
from user import User


class Session:
    _path_db: str
    _connect: Connection
    _cursor: Cursor

    def __init__(self, path_db: str):
        self._path_db = path_db

    def connection(self):
        self._connect = sqlite3.connect(self._path_db)
        return self

    def close(self):
        self._connect.close()
        return self

    def cursor(self):
        self._cursor = self._connect.cursor()
        return self

    def createTable(self):
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                api_id TEXT,
                api_hash TEXT,
                session_name TEXT,
                username TEXT,
                chat_id INTEGER,
                phone TEXT,
                auth_code INTEGER,
                schedule TEXT
                ):
            )
        ''')
        return self

    def commit(self):
        self._connect.commit()
        return self

    def save(self, user: User):
        api = user._api
        info = user._info
        self._cursor.execute('''
            INSERT INTO users (
                api_id,
                api_hash,
                session_name,
                username,
                chat_id,
                phone,
                auth_code,
                schedule
 )
            VALUES (?,?,?,?,?,?,?)
        ''', (
            api._api_id,
            api._api_hash,
            info._session_name,
            info._username,
            info._chat_id,
            info._phone,
            info._auth_code,
            info._schedule
        ))
        return self

    def loadAll(self) -> Iterable[User]:
        self._cursor.execute('SELECT * FROM users')
        rows = self._cursor.fetchall()
        for row in rows:
            yield self._generate(row)

    def load(self, chat_id: int) -> User:
        id = str(chat_id)
        self._cursor.execute('SELECT * FROM users WHERE chat_id=?', (id))
        row = self._cursor.fetchone()

        return self._generate(row)

    def _generate(self, row) -> User:
        (api_id,
         api_hash,
         session_name,
         username,
         chat_id,
         phone,
         auth_code,
         schedule) = row
        client = TelegramClient(
            session=session_name,
            api_id=api_id,
            api_hash=api_hash)
        user_info = UserInfo(
            session_name,
            username,
            int(chat_id),
            phone,
            auth_code,
            schedule
        )
        api = Api(api_id, api_hash)
        return User(api, user_info, client, self._path_db)

