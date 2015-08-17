__author__ = 'Seqian Wang'

import MySQLdb
# import Config.DBConfig as dbConfig

"""
Manage the Database interaction (Initiate connection, read, write, update)
"""


class DBUtils:
    """
    def __init__(self):
        pass

    @staticmethod
    def execute_query(query, **kwargs):
        con = MySQLdb.msqlDB.connect(dbConfig.DBParams['host'], dbConfig.DBParams['user'], dbConfig.DBParams['userPass'],
                             dbConfig.DBParams['dbName'])
        con.autocommit(True)
        cursor = con.cursor()
        cursor.execute(query)
        if 'numOfResults' in kwargs:
            return cursor.fetchmany(kwargs['numOfResults'])
        else:
            return cursor.fetchall()
    """

    def __init__(self, location="localhost", username="wang030", password="firefox", database="Processing_Pipeline"):
        self.location = location
        self.username = username
        self.password = password
        self.database = database

        # Open database connection
        self.db = MySQLdb.connect(self.location, self.username, self.password, self.database)
        # Prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

    def insert(self, command, uniqueTest = ''):
        # Send SQL query to INSERT a record into the database if record does not already exist
        sql_command = "IF NOT EXIST WHERE (%s) \
                      INSERT INTO Sorting VALUES (%s)" % (uniqueTest, command)
        self.execute(sql_command)

    @staticmethod
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
