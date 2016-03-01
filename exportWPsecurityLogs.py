# You must install apt-get install python-mysql.connector

import mysql.connector
from mysql.connector import errorcode

import sys

config = {
    'user': 'root',
    'password': 'bitnami',
    'host': '192.168.56.101',
    'database': 'bitnami_wordpress',
    'raise_on_warnings': True,
}


def run():
    cnx = connect()

    query = ("SELECT `occurrence_id`, `name`, `value`, `alert_id` FROM `wp_wsal_metadata` CROSS JOIN JOIN wp_wsal_occurrences ON occurrence_id = wp_wsal_occurrences.id ORDER BY `wp_wsal_metadata`.`occurrence_id` ASC ")

    curA = cnx.cursor()

    curA.execute(query)


    # Iterate through the result of curA
    for (db_id, occurrence_id, name, value) in curA:

        print(db_id, occurrence_id, name, value)


def connect():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
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

run()