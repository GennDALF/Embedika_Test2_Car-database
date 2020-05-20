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
| ```del_car()``` <br/> Максимальная и минимальная цены за промежуток времени |date_range_string <br/> "DD MM YYYY - <br/>DD MM YYYY" | JSON str |
| ```get_stats()``` <br/> Статистика по базе данных |   –   | JSON str * |

\* structure of ```get_stats()``` JSON output is:
```
[
  {
    "all entries": <int>,  # number of all entries 
    "start of monitoring": <str>,  # date of first monitoring period start: "DD mmmm YYYY"
    "end of monitoring": <str>,  # date of last monitoring period end: "DD mmmm YYYY"
    "global min price": [<float>, <str>],  # list of minimal price and corresponding date
    "global max price": [<float>, <str>]  # list of maximal price and corresponding date
  }
]
```
