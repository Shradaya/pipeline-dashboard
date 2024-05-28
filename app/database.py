import os
import psycopg2
from psycopg2 import pool
from flask import g, current_app
from dotenv import load_dotenv

load_dotenv()

# Initialize the connection pool
def init_connection_pool():
    return psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,  # Adjust maxconn according to your application's requirement
        host=os.getenv('DB_HOST'),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5
    )

# Get a connection from the pool
def get_conn():
    if 'conn_pool' not in g:
        g.conn_pool = init_connection_pool()
    if not g.conn_pool:
        raise Exception("Connection pool not available")
    return g.conn_pool.getconn()

# Release a connection back to the pool
def put_conn(conn):
    g.conn_pool.putconn(conn)

def close_db(e=None):
    conn = g.pop('conn', None)
    if conn is not None:
        put_conn(conn)  # Release the connection back to the pool instead of closing it

def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        g.conn_pool = init_connection_pool()  # Initialize the connection pool when app starts