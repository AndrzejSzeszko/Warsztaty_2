#!/usr/bin/python3.7
from psycopg2 import connect
from src.clcrypto import generate_salt, password_hash
from datetime import datetime


def create_db(db_name, db_conf):
    with connect(user=db_conf['user'], password=db_conf['password'], host=db_conf['host']) as con:
        con.autocommit = True
        sql = f"CREATE DATABASE {db_name}"
        with con.cursor() as curs:
            curs.execute(sql, (db_name,))


def nuke_db(db_name, db_conf):
    with connect(user=db_conf['user'], password=db_conf['password'], host=db_conf['host'], database=db_name) as con:
        con.autocommit = True
        sql = f"DROP DATABASE {db_name}"
        with con.cursor() as curs:
            curs.execute(sql, (db_name,))


class User:

    def __init__(self):
        self.__id = -1
        self.email = ''
        self.username = ''
        self.__hashed_password = ''

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt=''):
        self.__hashed_password = password_hash(password, generate_salt())

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO users(username, email, hashed_password)
            VALUES (%s, %s, %s) RETURNING id;"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE users SET username = %s, email = %s, hashed_password = %s WHERE id = %s"""
            values = (self.username, self.email, self.__hashed_password, self.__id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = """SELECT * FROM users WHERE id = %s;"""
        cursor.execute(sql, (user_id, ))
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data['id']
            loaded_user.username = data['username']
            loaded_user.__hashed_password = data['hashed_password']
            loaded_user.email = data['email']
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = """SELECT * FROM users ORDER BY username;"""
        cursor.execute(sql)
        ret = []
        for user in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = user['id']
            loaded_user.username = user['username']
            loaded_user.__hashed_password = user['hashed_password']
            loaded_user.email = user['email']
            ret.append(loaded_user)
        return ret

    def delete_from_db(self, cursor):
        sql = """DELETE FROM users WHERE id=%s;"""
        cursor.execute(sql, (self.__id,))
        self.__id = -1
        return True


class Message:

    def __init__(self):
        self.__id = -1
        self.from_id = ''
        self.to_id = ''
        self.text = ''
        self.__creation_datetime = datetime.now()

    @property
    def id(self):
        return self.__id

    @property
    def creation_datetime(self):
        return self.__creation_datetime

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date)
            VALUES (%s, %s, %s, %s) RETURNING id;"""
            values = (self.from_id, self.to_id, self.text, self.__creation_datetime)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()['id']
            return True
        return False

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = """SELECT * FROM messages WHERE id = %s;"""
        cursor.execute(sql, (message_id, ))
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data['id']
            loaded_message.from_id = data['from_id']
            loaded_message.to_id = data['to_id']
            loaded_message.text = data['text']
            loaded_message.__creation_datetime = data['creation_date']
            return loaded_message

    @staticmethod
    def load_messages_for_user(cursor, user_id):
        sql = """SELECT * FROM messages WHERE to_id = %s ORDER BY creation_date DESC;"""
        cursor.execute(sql, (user_id, ))
        ret = []
        for message in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = message['id']
            loaded_message.from_id = message['from_id']
            loaded_message.to_id = message['to_id']
            loaded_message.text = message['text']
            loaded_message.__creation_datetime = message['creation_date']
            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages(cursor):
        sql = """SELECT * FROM messages ORDER BY creation_date DESC;"""
        cursor.execute(sql)
        ret = []
        for message in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = message['id']
            loaded_message.from_id = message['from_id']
            loaded_message.to_id = message['to_id']
            loaded_message.text = message['text']
            loaded_message.__creation_datetime = message['creation_date']
            ret.append(loaded_message)
        return ret


if __name__ == '__main__':
    db_conf = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'coderslab'
    }
    create_db('messhub_db', db_conf)

# from Warsztaty_2.src.models import *
# from psycopg2.extras import RealDictCursor
# with connect(user='postgres', password='coderslab', host='localhost', database='messhub_db') as con:
#     with con.cursor(cursor_factory=RealDictCursor) as cur:
#         user1.save_to_db(cur)
