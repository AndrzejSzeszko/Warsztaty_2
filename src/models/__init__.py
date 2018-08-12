#!/usr/bin/python3.7
from psycopg2 import connect


def create_db(db_name, db_conf):
    with connect(user=db_conf['user'], password=db_conf['password'], host=db_conf['host']) as con:
        con.autocommit = True
        sql = f"CREATE DATABASE {db_name}"
        with con.cursor() as curs:
            curs.execute(sql, (db_name,))


def nuke_db(db_name, db_conf):
    with connect(user=db_conf['user'], password=db_conf['password'], host=db_conf['host']) as con:
        con.autocommit = True
        sql = f"DROP DATABASE {db_name}"
        with con.cursor() as curs:
            curs.execute(sql, (db_name,))


if __name__ == '__main__':
    db_conf = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'coderslab'
    }
    create_db('new_db', db_conf)
