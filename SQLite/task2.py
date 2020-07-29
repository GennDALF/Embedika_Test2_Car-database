
import locale as lc
from io import IOBase
import json
from SQLite import initial as db
from datetime import datetime as dt

lc.setlocale(lc.LC_ALL, 'ru_RU.UTF-8')

# list of all fields for database entry, 'r' fields are required
specs = {
    'plate': 'r',
    'brand': 'r',
    'model': 'r',
    'year': 'r',
    'color': 'r',
    'VIN': '',
    'power': '',
    'body': ''
}
# list of possible responses
results = {'s': "Success",
           'e': "Error occurred",
           'o': "Overlap occurred",
           'ow': "Overlap warning",
           'aw': "Attribute warning",
           'nf': "Not found"}


# first method to get list of cars from the database
def get_cars(_and=True, **filters):
    # any database field could be used as a filter,
    # set _and=False if want to use OR for filtering
    global specs, results
    if _and:
        operator = ' and '
    else:
        operator = ' or '
    # check if there are wrong columns
    if all([i in specs.keys() for i in filters.keys()]):
        params = ""
        # generate query
        for k, v in filters.items():
            params += '='.join([str(k), "'"+str(v)+"'"]) + operator
        query = db.select_cars_table.format(params[:-4])
        response, result = db.execute_read_query(query), []
        # process response
        for elem in response:
            result.append(tuple(elem))
        return result
    else:
        return results['e']


# second method to add one or few entries to the database
def add_cars(entry):
    # can use JSON string to add one or more entries to the database,
    # or .read()-supporting text or binary file containing
    # JSON dictionary or list of dictionaries
    global specs, results
    warning = None
    # convert from JSON to dict
    if isinstance(entry, IOBase):
        data = json.load(entry)
    elif isinstance(entry, str):
        data = json.loads(entry)
    else:
        return results['e']
    # if we have few non-empty elements
    if isinstance(data, list) and len(data) > 0:
        if all(type(d) is dict for d in data) and \
           all(d for d in data):
            # iterate the list of entries
            for elem in data:
                # check if there are wrong columns
                if all([i in specs.keys() for i in elem.keys()]):
                    # check if all required fields are given
                    if all(i in elem.keys() for
                           i in [k for k, v in specs.items() if v == 'r']):
                        # check if there is the same element in database
                        check_query = db.select_cars_table.format("plate='" + elem['plate'] + "'")
                        overlap = db.execute_read_query(check_query)
                        if not overlap:
                            # generate query
                            columns_cars = [*elem.keys()]
                            query_cars = db.insert_cars_table.format(','.join(columns_cars),
                                                                     ('?,' * len(columns_cars))[:-1])
                            values_cars = [*elem.values()]
                            db.execute_query(query_cars, values_cars)
                        else:
                            warning = results['ow']
                            continue
                    else:
                        warning = results['aw']
                        continue
                else:
                    warning = results['aw']
                    continue
        else:
            return results['e']
    # if we have one non-empty element
    elif isinstance(data, dict) and len(data) > 0:
        return add_cars(json.dumps([data]))
    else:
        return results['e']
    # check if there was warning
    if warning:
        return warning
    else:
        return results['s']


# third method to delete entry from the database
def del_cars(id_number=None, plate_number=None):
    # can use plate_number (explicit key) or id field as reference
    # (if none will be entered, 'Not found' error will return)
    # the history table will be updated symmetrically
    global results
    if not id_number and not plate_number:
        return results['nf']
    # generate query for checking if we have such entry in database
    if not id_number:
        check_query = db.select_cars_table.format("plate='" + plate_number + "'")
    else:
        check_query = db.select_cars_table.format("id=" + str(id_number))
    found = db.execute_read_query(check_query)
    if found:
        if not id_number:
            query = db.delete_cars_table.format("plate='" + plate_number + "'")
        else:
            query = db.delete_cars_table.format("id=" + str(id_number))
        db.execute_query(query)
        return results['s']
    else:
        return results['nf']


# fourth method to get statistics about database
def get_stats():
    # number of all cars
    total_entries = db.execute_read_query(db.aggregate_all_cars)[0][0]
    # date and time of database creation
    first_update = db.execute_read_query(db.first_last_update)[0][0]
    # date and time of last update
    last_update = db.execute_read_query(db.first_last_update)[1][0]
    # days between creation and last update
    days_uptime = (dt.fromisoformat(last_update) - dt.fromisoformat(first_update)).days
    # number of cars with certain body type
    bodies = dict(db.execute_read_query(db.cars_bodies))
    # changing None key to str type
    if None in bodies.keys():
        bodies['no category'] = bodies[None]
        del bodies[None]
    result = {
        'Total entries': str(total_entries),
        'Days of uptime': str(days_uptime) + " days",
        'Last update': str(last_update),
        'Number of cars of different bodies': bodies
    }
    return json.dumps([result])
