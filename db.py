import psycopg2
from pgvector.psycopg2 import register_vector
from app.config import Setting

def get_connection():
    connections = psycopg2.connect(Setting.database_url)
    register_vector(connections)
    return connections