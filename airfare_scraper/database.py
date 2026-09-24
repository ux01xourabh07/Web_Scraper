import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Reads connection parameters from environment variables.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "airfare_index")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL Database: {err}")
        return None

# For backward compatibility with simpler imports
connection = get_db_connection()
