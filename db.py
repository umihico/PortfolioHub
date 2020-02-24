
import os
import mysql.connector as mydb
import env

kw = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('MYSQL_PORTFOLIOHUB_DATABASENAME')
}


def get_db():
    conn = mydb.connect(**kw)
    conn.autocommit = True
    return conn


def test_get_db():
    print('is_connected', get_db().is_connected())


if __name__ == '__main__':
    test_get_db()
