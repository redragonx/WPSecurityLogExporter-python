# You must install the python mysql connector via pip or package manager
# apt-get install python-mysql.connector
# Created by Stephen Chavez on Feb 28th, 2016
#

import mysql.connector
from mysql.connector import errorcode

import sys
import time
import csv

config = {
    'user': 'root',
    'password': 'bitnami',
    'host': '192.168.56.101',
    'database': 'bitnami_wordpress',
    'raise_on_warnings': True,
}


def run():
    cnx = connect()

    query1 = ("SELECT `occurrence_id`, `name`, `value` FROM `wp_wsal_metadata` ")
    query2 = ("SELECT `id`, `site_id`, `alert_id`, `created_on` FROM `wp_wsal_occurrences` ORDER BY `id`")

    cur_wsal_metadata = cnx.cursor(buffered=True)
    cur_occurrence = cnx.cursor(buffered=True)

    cur_wsal_metadata.execute(query1)
    cur_occurrence.execute(query2)

    occurrence_table_row_list = list(cur_occurrence.fetchall())

    old_id = 1
    changed = False

    csv_file_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    csv_file_path = 'wpSecurityMainLog' + csv_file_date + '.csv'

    import HTMLParser

    h = HTMLParser.HTMLParser()


# Iterate through the result of curA

    with open(csv_file_path, 'w') as csvfile:

        csv_writer = csv.writer(csvfile)

        # Each event has multiple lines in the database table, so to filter an event, use the occurrence_id
        for (wsal_occurrence_id, name, value) in cur_wsal_metadata:

            metadata_row = wsal_occurrence_id, name, h.unescape(value).encode('utf-8')
            print(metadata_row)
            csv_writer.writerow(metadata_row)

            if old_id != wsal_occurrence_id:
                changed = True

            # This loop appends information from the 2nd table at the end of every event.
            for (occurrence_id, site_id, alert_id, created_on) in occurrence_table_row_list:
                if changed and occurrence_id == wsal_occurrence_id:
                    new_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created_on))
                    occurrence_row = occurrence_id, site_id, alert_id, new_date

                    print(occurrence_row)
                    csv_writer.writerow(occurrence_row)

            old_id = wsal_occurrence_id
            changed = False


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