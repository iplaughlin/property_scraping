# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 17:08:54 2021

@author: Ian
"""
import sqlite3
import mysql.connector

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def create_sql_connection(host, user, password, database):
    """ create a database connection to the MySQL database
        specificied by db_file.
        :param db_file: mysql file
        :return: connection object or None
    """
    connection = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
        )
    return connection
