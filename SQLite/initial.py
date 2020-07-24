
import os
import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection_object = None
    try:
        connection_object = sqlite3.connect('\\'.join([os.getcwd(), path]))
        connection_object.row_factory = sqlite3.Row
        print(f"Connection to SQLite DB {path} successful")
    except Error as e:
        print(f"The error \'{e}\' occurred")
    return connection_object


connection = create_connection('database.sqlite')


def execute_query(query):
    global connection
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"the error \'{e}\' occurred")
    cursor.close()


def execute_read_query(query):
    global connection
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print(f"The error \'{e}\' occurred")
    cursor.close()
    return result


create_cars_table = ("CREATE TABLE IF NOT EXISTS cars (\n"
                     "  id INTEGER PRIMARY KEY,\n"
                     "  plate TEXT NOT NULL,\n"
                     "  brand TEXT NOT NULL,\n"
                     "  model TEXT NOT NULL,\n"
                     "  year INTEGER NOT NULL,\n"
                     "  color TEXT NOT NULL,\n"
                     "  VIN TEXT,\n"
                     "  power REAL,\n"
                     "  body TEXT NOT NULL);")

create_stats_table = ("CREATE TABLE IF NOT EXISTS history (\n"
                      "  id INTEGER PRIMARY KEY,\n"
                      "  track_car INTEGER NOT NULL,\n"
                      "  entry_updated TEXT,\n"
                      "  previous_state TEXT,\n"
                      "  FOREIGN KEY(track_car) REFERENCES cars(id));")

if connection:
    execute_query(create_cars_table)
    execute_query(create_stats_table)
else:
    raise Error('no access to database')

insert_cars_table = "INSERT INTO cars ({0}) VALUES (?{1})"
insert_stats_table = "INSERT INTO stats ({0}) VALUES (?{1})"

select_cars_table = "SELECT * FROM cars WHERE {0}"
select_stats_table = "SELECT * FROM stats WHERE {0}"
