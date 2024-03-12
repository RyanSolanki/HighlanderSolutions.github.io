import sqlite3
import pytest
import os

@pytest.fixture
def database_connection():
    # path to your database file
    dbDirectory = "../../instance/" 
    dbFilename = "database.db"
    
    # Combine the directory and filename to get the full path
    dbPath = os.path.abspath(os.path.join(os.path.dirname(__file__), dbDirectory, dbFilename))

    # Ensure the database file exists before attempting to connect
    if not os.path.exists(dbPath):
        raise FileNotFoundError(f"The database file '{dbPath}' does not exist.")

    # Establish a connection to the database
    connection = sqlite3.connect(dbPath)
    yield connection

    # Close the connection after the test is finished
    connection.close()

def test_database_connection(database_connection):
    # Check if the connection is successful
    assert database_connection is not None

    # Query from database table
    cursor = database_connection.cursor()
    cursor.execute("SELECT Name FROM Exercises LIMIT 1;")
    result = cursor.fetchone()

    # Check if the query result contains any value (not None)
    assert result is not None
