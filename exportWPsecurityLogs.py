# You must install apt-get install python-mysql.connector

import mysql.connector
from mysql.connector import errorcode

import sys

config = {
    'user': 'scott',
    'password': 'tiger',
    'host': '127.0.0.1',
    'database': 'employees',
    'raise_on_warnings': True,
}


def run():
    cnx = connect()


def connect():
    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            sys.exit(1)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            sys.exit(1)
        else:
            print(err)
            sys.exit(1)
    else:
        cnx.close()
    return cnx

run()