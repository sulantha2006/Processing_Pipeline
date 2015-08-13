#!/usr/bin/python
__author__ = 'Seqian Wang'

import MySQLdb

# Manage the Database interaction (Initiate connection, read, write, update)


class SqlDatabase:
    def __init__(self, location="localhost", username="wang030", password="firefox", database="Processing_Pipeline"):
        self.location = location
        self.username = username
        self.password = password
        self.database = database

        # Open database connection
        self.db = MySQLdb.connect(self.location, self.username, self.password, self.database)
        # Prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

    def insert(self,command):
        exist = False
        # Check if scan_session already exist in SQL database
        pass

        if not exist:
            # Send SQL query to INSERT a record into the database
            sql_command = "INSERT IF NOT EXIST unique_key" + command
            self.execute(sql_command)

    def execute(self, command):
        try:
            # Execute the SQL command
            self.cursor.execute(command)
            # Commit changes into the database
            self.commit()
        except:
            # Rollback in case of error
            self.rollback()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        # Disconnect from server
        self.db.close()