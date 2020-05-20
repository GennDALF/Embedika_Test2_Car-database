
import datetime as dt
import locale as lc
import json

lc.setlocale(lc.LC_ALL, 'ru_RU.UTF-8')

# loading database
with open("database.json", encoding='utf8') as db:
    cars = json.load(db)

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

# global database statistics
stats = {
    'total_entries': len(cars),
    'first_entry': dt.datetime(2020, 5, 20, 12).strftime("%H:%M %x"),
    'last_update': dt.datetime(2020, 5, 20, 17, 20).strftime("%H:%M %x"),
    'total_queries': 28,
    'last_query': ""
}


# first method to get list of cars from the database
def get_cars(_and=True, **filters):
    # any database field could be used as a filter,
    # set _and=False if want to use OR for filtering
    global cars, specs, stats
    # check if we have wrong fields
    if all([i in specs.keys() for i in filters.keys()]):
        if _and:
            # that means logical AND for filters
            cars_filtered = cars
            # start from full database and cut it according to filter results
            for field in filters.keys():
                cars_filtered = [car for car in cars_filtered
                                 if filters[field] in car.values()]
        else:
            # that means logical OR for filters
            cars_filtered = []
            # start from empty database and extend it with filter results
            for field in filters.keys():
                for elem in [car for car in cars if filters[field] in car.values()]:
                    # without duplicates
                    if elem not in cars_filtered:
                        cars_filtered.append(elem)
        stats['total_queries'] += 1
        stats['last_query'] = dt.datetime.today().strftime("%H:%M %x")
        return cars_filtered
    else:
        return "Error: wrong input"


# second method to add one or few entries to the database
def add_car(entry="[]", **car_specs):
    # can use JSON to add one or more entries to the database directly,
    # or can use raw car specification to form and add one entry
    global cars, specs
    # convert from JSON str to dict
    data = json.loads(entry)
    # processing raw car specifications
    if car_specs:
        # check if all required fields are attributed
        if all(i in car_specs.keys() for
               i in [k for k, v in specs.items() if v == 'r']):
            # update and write database to file
            cars.append(car_specs)
            with open('database.json', 'w', encoding='utf8') as db:
                json.dump(cars, db, indent=2, sort_keys=False)
            stats['total_entries'] += 1
            stats['last_update'] = dt.datetime.today().strftime("%H:%M %x")
            return "Successful"
        else:
            return "Error. The required fields are missing"
    # processing JSON entry
    elif all(d for d in data):
        # case of any amount of entries
        if type(data) is list:
            for elem in data:
                # check if all required fields are in entry
                if all(i in elem.keys() for
                       i in [k for k, v in specs.items() if v == 'r']):
                    # check with unique plate number if entry already exists
                    if not elem['plate'] in [car['plate'] for car in cars]:
                        # update database
                        cars.append(elem)
                    else:
                        return "Error: entry already exists"
                else:
                    return "Error: the required fields are missing"
            # write database to file
            with open('database.json', 'w', encoding='utf8') as db:
                json.dump(cars, db, indent=2, sort_keys=False)
            stats['total_entries'] += len(data)
            stats['last_update'] = dt.datetime.today().strftime("%H:%M %x")
            return "Successful"
        # case of one entry
        elif type(data) is dict:
            # probably not good for frequent database updates, but work well here
            return add_car(json.dumps([data]))
        else:
            return "Error: wrong input"
    else:
        raise AttributeError("Attribute error")


# third method to delete one or few entries from the database
def del_car(*plate_numbers):
    # can list one or more plate numbers to delete from the database
    global cars
    flag = False
    wrong_numbers = []
    for number in plate_numbers:
        # check with unique plate number if entry already exists
        if number in [car['plate'] for car in cars]:
            # update database
            cars = [car for car in cars if not(car['plate'] == number)]
            flag = True
        else:
            wrong_numbers.append(number)
    with open('database.json', 'w', encoding='utf8') as db:
        json.dump(cars, db, indent=2, sort_keys=True)
    if flag and not wrong_numbers:
        # if got here than all numbers are deleted
        return "Successful"
    elif flag and wrong_numbers:
        # here some numbers were deleted and some were not found
        return "Warning: {} plate number(-s) have not been found".format(wrong_numbers)
    elif not(flag) and wrong_numbers:
        # here none of the numbers were found
        return "Error: {} plate number(-s) have not been found".format(wrong_numbers)
    else:
        # how did you get here?
        return "Error"


# fourth method to get statistics on the database
def get_stats():
    global stats
    return stats
