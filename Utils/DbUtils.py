__author__ = 'Seqian Wang'

import mysql.connector
import Config.DBConfig as dbConfig

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

    def __init__(self, location=dbConfig.DBParams['host'], username=dbConfig.DBParams['user'], password=dbConfig.DBParams['userPass'], database=dbConfig.DBParams['dbName']):
        self.location = location
        self.username = username
        self.password = password
        self.database = database
        self.conn = mysql.connector.connect(host=self.location,
                                       database=self.database,
                                       user=self.username,
                                       password=self.password)
        self.cursor = self.conn.cursor()

    def insertIfNotExist(self, values, uniqueTestFields='', uniqueTestValues = ''):
        # Send SQL query to INSERT a record into the database if record does not already exist
        #sql_command = "INSERT INTO Sorting VALUES (%s) WHERE NOT EXISTS (SELECT * FROM Sorting WHERE (%s)=(%s))" % (values, uniqueTestFields, uniqueTestValues)
        sql_command = "INSERT IGNORE INTO Sorting VALUES (%s) " % (values)
        self.executeNoResult(sql_command)

    def executeNoResult(self, sqlStr):
        try:
            self.cursor.execute(sqlStr)
            self.commit()
        except:
            self.rollback()
            raise

    def executeAllResults(self, sqlStr):
        pass

    def executeSomeResults(self, sqlStr, numOfResults):
        pass

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()
