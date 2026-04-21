# 🎨 Иллюстрация: module6-flask-routes

## Назначение
Визуализировать как Flask @app.route связывает URL с Python-функцией.

## Схема
```
HTTP Запрос                 Flask Router              Python функция
GET /items        ────►    @app.route("/items")  ───► def get_all():
                           methods=["GET"]              return jsonify(...)

POST /items       ────►    @app.route("/items")  ───► def create():
                           methods=["POST"]             return jsonify(...), 201
```

### Блоки:
- Левый столбец: HTTP запросы (GET, POST, DELETE) с URL
- Центр: Flask маршрутизатор (стрелки)
- Правый столбец: Python функции с результатами
- Внизу: HTTP статус коды 200/201/404

## Стиль
Три колонки с соединяющими стрелками. Цветовое кодирование методов (GET=зелёный, POST=синий, DELETE=красный).
