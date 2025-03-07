"""
===================================================
Script Name:       database_handler.py
Author:            Tim Tanner, tim.tanner@gmail.com
Description:       Abstraction class to handle sql database connections
Version:           1.0.0
Release History:
    07mar2025: 1.0.0 - Initial release

Created on:        07mar2025
===================================================
"""

__author__ = "Tim Tanner, tim.tanner@gmail.com"
__version__ = "1.0.0"
__date__ = "07mar2025"
__license__ = "MIT"

import sqlite3
from typing import Any, List, Tuple

class SQLDatabaseHandler:
    """
    A class to handle interactions with an SQL database, primarily SQLite.
    This class supports opening and closing connections, creating tables,
    inserting data, and retrieving data based on queries. Future extensions
    may include support for other SQL databases like MySQL or PostgreSQL.
    """

    def __init__(self, db_name: str = "database.db"):
        """
        Initialize the database handler.
        :param db_name: The name of the SQLite database file.
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def open_connection(self):
        """Open a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print("Database connection opened successfully.")
        except sqlite3.Error as e:
            print(f"Error opening database connection: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def create_table(self, table_name: str, columns: str):
        """
        Create a table in the database.
        :param table_name: Name of the table.
        :param columns: Column definitions in SQL syntax (e.g., "id INTEGER PRIMARY KEY, name TEXT").
        """
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
            self.connection.commit()
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, table_name: str, columns: str, values: Tuple[Any, ...]):
        """
        Insert data into a table.
        :param table_name: Name of the table.
        :param columns: Columns to insert data into (e.g., "name, age").
        :param values: Tuple containing values to insert.
        """
        try:
            placeholders = ', '.join(['?' for _ in values])
            self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
            self.connection.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def retrieve_data(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple]:
        """
        Retrieve data from the database based on a query.
        :param query: SQL SELECT query.
        :param params: Optional parameters for the query.
        :return: List of tuples containing query results.
        """
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return []

# Example usage
if __name__ == "__main__":
    db_handler = SQLDatabaseHandler("stock_data.db")
    db_handler.open_connection()
    db_handler.create_table("stocks", "id INTEGER PRIMARY KEY, ticker TEXT, price REAL, date TEXT")
    db_handler.insert_data("stocks", "ticker, price, date", ("AAPL", 150.25, "2024-03-07"))
    data = db_handler.retrieve_data("SELECT * FROM stocks")
    print("Retrieved Data:", data)
    db_handler.close_connection()

