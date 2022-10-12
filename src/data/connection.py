#!/usr/bin/python
from dotenv import load_dotenv
import os
load_dotenv()
from configparser import ConfigParser
import psycopg2

import sqlalchemy as db


DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PASSW = os.getenv("DB_PASSW")
DB_PORT = os.getenv("DB_PORT")



SQLALCHEMY_DATABASE_URI =  f'postgresql://{DB_USER}:{DB_PASSW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
connection = engine.connect()


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db



def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        SQLALCHEMY_DATABASE_URI =  f'postgresql://{DB_USER}:{DB_PASSW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        print(connection)




    #     # read connection parameters
    #     params = config()

    #     # connect to the PostgreSQL server
    #     print('Connecting to the PostgreSQL database...')
    #     conn = psycopg2.connect(**params)
		
    #     # create a cursor
    #     cur = conn.cursor()
        
	# # execute a statement
    #     print('PostgreSQL database version:')
    #     cur.execute('SELECT version()')

    #     # display the PostgreSQL database server version
    #     db_version = cur.fetchone()
    #     print(db_version)
       
	# # close the communication with the PostgreSQL
    #     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')


if __name__ == '__main__':
    connect()
