import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = os.getenv("MYSQL_PORT", "3306")
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DATABASE", "airfare_index")
        self.connection = None

    def connect(self):
        print("Connecting to MySQL...")
        print(f"Database: {self.database}")
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Database connection: SUCCESS")
                return True
        except Error as e:
            print(f"Database connection: FAILED")
            print(f"Error: {e}")
            return False
        return False

    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_transaction(self, queries):
        """
        Executes a list of queries (tuples of (query, params)) in a single transaction.
        Rolls back if any query fails.
        """
        if not self.get_connection():
            return False
            
        cursor = self.connection.cursor()
        try:
            # Disable autocommit to start a transaction
            self.connection.autocommit = False
            
            for query, params in queries:
                cursor.execute(query, params)
                
            # Commit the transaction if all queries succeed
            self.connection.commit()
            return True
            
        except Error as e:
            # Rollback in case of error
            self.connection.rollback()
            print(f"Transaction failed and rolled back. Error: {e}")
            return False
            
        finally:
            cursor.close()
            # Restore autocommit
            self.connection.autocommit = True
