import psycopg2
from ..config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT


class PostgreSQLConnection:
    def __init__(self):
        self.conn = None
        self.host = DB_HOST
        self.user = DB_USER
        self.port = DB_PORT
        self.database = DB_NAME
        self.password = DB_PASSWORD
        self.conn_not_established = "Conenction to database not established"

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def __del__(self):
        self.close()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connected to PostgreSQL successfully!")
            return self
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("Connection to PostgreSQL closed.")

    def execute_get_query(self, query, data = None):
        if self.conn:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, data)
                    result = cursor.fetchall()
                    return result
            except psycopg2.Error as e:
                print(f"Error executing query: {e}")
                return None
        else:
            print(self.conn_not_established)
            return None
   
    def execute_query(self, query, data = None):
        if self.conn:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, data)
                    self.conn.commit()
            except psycopg2.Error as e:
                print(f"Error executing query: {e}")
                return None
        else:
            print(self.conn_not_established)
            return None
    
    def batch_execute_queries(self, query, data = None):
        if self.conn:
            try:
                with self.conn.cursor() as cursor:
                    cursor.executemany(query, data)
                    self.conn.commit()
            except psycopg2.Error as e:
                print(f"Error executing query: {e}")
                return None
        else:
            print(self.conn_not_established)
            return None
