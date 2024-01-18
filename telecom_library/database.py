from typing import Any, Dict, List
from urllib.parse import urlparse

import psycopg2


def get_database_credentials_from_url(db_url):
    parsed_url = urlparse(db_url)
    return {
        "db_host": parsed_url.hostname,
        "db_port": parsed_url.port,
        "db_name": parsed_url.path[1:],
        "db_user": parsed_url.username,
        "db_password": parsed_url.password,
    }


class DatabaseConnector:
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            print("Connected to the database.")
        except psycopg2.Error as e:
            print(f"Error: Unable to connect to the database. {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def execute_sql_file(self, sql_commands):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql_commands)
                self.connection.commit()
                cursor.close()
                print("SQL script executed successfully.")
        except psycopg2.Error as e:
            # Rollback changes if an error occurs
            self.connection.rollback()
            print(f"Error executing SQL script: {e}")
        finally:
            self.disconnect()
   
        
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        result = []
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.Error as e:
            print(f"Error executing query. {e}")
        finally:
            self.disconnect()
        return result
