#!/usr/bin/python
__author__ = 'Seqian Wang'

import MySQLdb

# the Database (Initiate connection, read, write, update)

class SqlDatabase:
    def __init__(self, location, username, password, database):
        # Insert default values

        #Open database connection
        db = MySQLdb.connect(location, username, password, database)
        # Prepare a cursor object using cursor() method
        cursor = db.cursor()

    def insert:
        #Parepare SQL query to INSERT a record into the database
        sql_command = "INSERT "
        self.execute(sql_command)

    def execute(self, command):
        try:
            # Execute the SQL command
            cursor.execute(command)
            # Commit changes into the database
            self.commit()
        except:
            # Rollback in case of error
            self.rollback()

    def commit(self):
        db.commit()

    def rollback(self):
        db.rollback()

    def close(self):
        db.close()