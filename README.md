# Тестовое задание 2. Справочник автомобилей
### Задание
>Необходимо реализовать сервис справочника автомобилей с хранением данных в базе или файле.
><br/>Минимальная информация по объекту:
>- номер;
>- марка;
>- цвет;
>- год выпуска.
#
### Описание API



| Метод | Параметры | Возвращаемый результат |
| :--- | :---: | :---: |
| ```get_cars()``` <br/> Вывод списка автомобилей | ```_and=True```<br/><br/>```**filters```<br/>"DD MM YYYY" | float <br/> |
| ```add_car()``` <br/> Добавление автомобиля(-ей) | date_range_string <br/> "DD MM YYYY - <br/>DD MM YYYY" | float <br/> |
| ```del_car()``` <br/> Удаление автомобиля(-ей) |date_range_string <br/> "DD MM YYYY - <br/>DD MM YYYY" | JSON str |
| ```get_stats()``` <br/> Статистика по базе данных |   –   | JSON str * |

\* structure of ```get_stats()``` JSON output is:
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
