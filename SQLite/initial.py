
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


def execute_query(query, values=None):
    global connection
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
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
                     "  body TEXT);")

create_history_table = ("CREATE TABLE IF NOT EXISTS history (\n"
                        "  id INTEGER PRIMARY KEY,\n"
                        "  track_car INTEGER NOT NULL,\n"
                        "  entry_updated TEXT,\n"
                        "  previous_state TEXT,\n"
                        "  FOREIGN KEY(track_car) REFERENCES cars(id));")

create_cars_insert_trigger = ("CREATE TRIGGER IF NOT EXISTS first_history_entry\n"
                              "    AFTER INSERT ON cars\n"
                              "    BEGIN \n"
                              "        INSERT INTO history (track_car, entry_updated)\n"
                              "        VALUES (new.id, datetime('now','localtime'));\n"
                              "    END;")

create_cars_update_trigger = ("CREATE TRIGGER IF NOT EXISTS update_history \n"
                              "    AFTER UPDATE ON cars WHEN old.id == new.id \n"
                              "    BEGIN\n"
                              "        INSERT INTO history (track_car, entry_updated, previous_state) \n"
                              "        VALUES (new.id, \n"
                              "                datetime('now','localtime'), \n"
                              "                old.plate || ';' || \n"
                              "                old.brand || ';' || \n"
                              "                old.model || ';' || \n"
                              "                old.year || ';' || \n"
                              "                old.color || ';' || \n"
                              "                coalesce(old.VIN, '<null>') || ';' || \n"
                              "                coalesce(old.power, '<null>')  || ';' || \n"
                              "                coalesce(old.body, '<null>')); \n"
                              "    END;")

create_cars_delete_trigger = ("CREATE TRIGGER IF NOT EXISTS delete_history\n"
                              "    AFTER DELETE ON cars\n"
                              "    BEGIN\n"
                              "        DELETE FROM history WHERE old.id == track_car;\n"
                              "    END;")

if connection:
    execute_query(create_cars_table)
    execute_query(create_history_table)
    execute_query(create_cars_insert_trigger)
    execute_query(create_cars_update_trigger)
    execute_query(create_cars_delete_trigger)
else:
    raise Error('no access to database')

insert_cars_table = "INSERT INTO cars ({0}) VALUES ({1})"
select_cars_table = "SELECT * FROM cars WHERE {0}"
delete_cars_table = "DELETE FROM cars WHERE {0}"

aggregate_all_cars = "SELECT count(1) FROM cars"
first_last_update = ("SELECT min(entry_updated) FROM history\n"
                     "UNION\n"
                     "SELECT max(entry_updated) FROM history")
cars_bodies = ("SELECT body, count(1) as amount FROM cars\n"
               "GROUP BY body\n"
               "ORDER BY amount DESC")
