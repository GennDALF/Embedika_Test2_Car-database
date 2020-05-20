# Тестовое задание 2. Справочник автомобилей
### Задание
>Необходимо реализовать сервис справочника автомобилей с хранением данных в базе или файле.
><br/>Минимальная информация по объекту:<br/> – номер;<br/> – марка;<br/> – цвет;<br/> – год выпуска.
#
### Описание API
#

| Метод | Параметры | Возвращаемый результат |
| :--- | :---: | :---: |
| ```get_cars()``` <br/> Вывод списка автомобилей | ```**filters```<br/>Словарь для задания фильтров \*<br/>```_and=True```<br/>В значении ```True``` использует логическое И для фильтров<br/>В значении ```False``` использует логическое ИЛИ для фильтров | list <br/> |
| ```add_car()``` <br/> Добавление автомобиля(-ей) | ```entry="[]"```<br/>Строка с данными в формате JSON<br/>```**car_specs```<br/>Словарь для задания спецификаций автомобиля \* | str <br/> |
| ```del_car()``` <br/> Удаление автомобиля(-ей) | ```*plate_numbers```<br/>```set()``` из строк с номерами автомобилей для удаления | str |
| ```get_stats()``` <br/> Статистика по базе данных |   –   | JSON str \*\* |

\* all possible fields of the database entry: ```'r'``` is required
```
{
  'plate': 'r',
  'brand': 'r',
  'model': 'r',
  'year': 'r',
  'color': 'r',
  'VIN': '',
  'power': '',
  'body': ''
}
```
\*\* structure of ```get_stats()``` JSON output is:
```
[
  {
    'total_entries': <int>,   # number of all cars in the database
    'first_entry': <str>,     # time and date of the first entry adding: "HH:MM DD.mm.YYYY"
    'last_update': <str>,     # time and date of the last entry adding: "HH:MM DD.mm.YYYY"
    'total_queries': <int>,   # number of all queries made to the database
    'last_query': <str>       # time and date of the last querie made: "HH:MM DD.mm.YYYY"
  }
]
```
