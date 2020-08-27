import psycopg2
import os


def _get_db_credentials():
    db_creds = {
        'dbname': os.getenv('PGDATABASE', 'postgres'),
        'username': os.getenv('PGUSER', 'postgres'),
        'password': os.getenv('PGPASSWORD', 'postgres'),
        'host': os.getenv('PGHOST', 'localhost'),
        'port': os.getenv('PGPORT', 5432)
    }
    return db_creds


def connect_to_db():
    db_creds = _get_db_credentials()
    cnx = psycopg2.connect(dbname=db_creds['dbname'],
                           user=db_creds['username'],
                           password=db_creds['password'],
                           host=db_creds['host'],
                           port=db_creds['port'])
    return cnx
