"""
Database Connection Module
Handles MySQL database connection for FitLife Wellness Centre
"""

import mysql.connector
from mysql.connector import Error
import sys


class FitLifeDB:
    """Database connection and management class"""
    
    def __init__(self):
        """Initialize database connection"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                database='fitlife_wellness',
                user='root',      
                password=''       
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                db_info = self.connection.get_server_info()
                print(f"✓ Successfully connected to MySQL Server version {db_info}")
                
                self.cursor.execute("SELECT DATABASE();")
                record = self.cursor.fetchone()
                print(f"✓ Connected to database: {record[0]}")
                
        except Error as e:
            print(f"✗ Error connecting to MySQL Database: {e}")
            sys.exit(1)
    
    def get_connection(self):
        """Return the database connection object"""
        return self.connection
    
    def get_cursor(self):
        """Return the database cursor object"""
        return self.cursor
    
    def commit(self):
        """Commit the current transaction"""
        try:
            self.connection.commit()
        except Error as e:
            print(f"✗ Error committing transaction: {e}")
    
    def rollback(self):
        """Rollback the current transaction"""
        try:
            self.connection.rollback()
        except Error as e:
            print(f"✗ Error rolling back transaction: {e}")
    
    def close_connection(self):
        """Close database connection"""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("✓ Database connection closed successfully")
    
    def execute_query(self, query, params=None):
        """
        Execute a query and return results
        
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for the query
            
        Returns:
            list: Query results or None if error
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
        
        except Error as e:
            print(f"✗ Error executing query: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for the query
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return True
        
        except Error as e:
            print(f"✗ Error executing update: {e}")
            self.connection.rollback()
            return False
    
    def get_last_insert_id(self):
        """Return the last inserted ID"""
        return self.cursor.lastrowid