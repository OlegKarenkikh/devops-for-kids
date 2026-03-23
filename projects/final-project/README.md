# 🏆 Итоговый проект — «Моя Коллекция»

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/final-project-pyramid.jpg" alt="Итоговый проект — пирамида знаний" width="85%"/>
<br/><em>Один проект — все знания курса. От терминала до Kubernetes!</em>
</div>

---

## 🤔 Что мы строим и зачем?

### Задача

Представь: ты хочешь вести список своей коллекции — книг, игр, фильмов, чего угодно. Можно завести таблицу в Excel. Но что если ты хочешь, чтобы к твоей коллекции мог обращаться телефон, другой компьютер, или даже другой программист?

Для этого создают **REST API** — программу, которая отвечает на запросы по сети и умеет хранить данные. Это именно то, что мы и построим.

### Что будет в итоге?

После выполнения проекта у тебя будет полноценный сервис:

| Что | Зачем |
|-----|-------|
| Flask REST API | Принимает запросы, работает с данными |
| SQLite база | Хранит коллекцию (не теряется при перезапуске) |
| Docker контейнер | Запускается одинаково везде |
| Docker Compose | Запускает всё одной командой с правильными настройками |
| Kubernetes Deployment | Управляет 3 копиями сервиса, автоперезапуск |
| GitHub репозиторий | История всех изменений, публичный код |

### Как всё работает вместе?

```
Пользователь (curl / браузер)
        │
        │ HTTP запрос: GET /items
        ▼
   Flask API (app.py)           ← Python код, обрабатывает запрос
        │
        │ SQL запрос: SELECT * FROM items
        ▼
   SQLite (collection.db)       ← Файл на диске, хранит данные
        │
        │ Возвращает строки
        ▼
   Flask API → JSON ответ       ← [{"id":1,"name":"Гитара"}, ...]
        │
        ▼
Пользователь получает данные
```

Всё это работает **внутри Docker контейнера**. Контейнер запускается в **Kubernetes** — системе, которая следит чтобы сервис всегда работал.


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/project_architecture.png" alt="Архитектура проекта" width="90%"/>
<br/><em>Запрос от пользователя → Flask API → SQLite → ответ JSON. Всё внутри Docker!</em>
</div>
### Маршрут API

| Маршрут | Метод | Что делает |
|---------|-------|-----------|
| `/` | GET | Информация о сервисе |
| `/items` | GET | Получить все предметы коллекции |
| `/items` | POST | Добавить новый предмет |
| `/items/<id>` | DELETE | Удалить предмет по ID |
| `/health` | GET | Проверка что сервис жив (для Kubernetes) |

---


> **Когда делать:** после прохождения всех 35 уроков
> **Время:** 3–4 часа
> **Что создаём:** REST API «Моя Коллекция» — список любимых вещей

---

## 🗂️ Структура проекта

```
final-project/
├── app.py                ← Flask API (главный код)
├── requirements.txt      ← Зависимости
├── Dockerfile            ← Рецепт контейнера
├── docker-compose.yml    ← Запуск локально
├── .env.example          ← Пример переменных
├── .gitignore
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

---

## Шаг 1 — Создать проект (Модули 1–2)

```bash
mkdir my-collection && cd my-collection
git init
echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore

cat > .env << 'ENVEOF'
APP_PORT=8080
APP_NAME=МояКоллекция
DB_PATH=collection.db
ENVEOF

git add .gitignore && git commit -m "Старт проекта"
```

---

## Шаг 2 — Код на Python (Модуль 6)

Смотри файл `app.py` рядом с этим README.

```bash
pip install -r requirements.txt
python app.py

# Тестируем
curl http://localhost:8080/
curl http://localhost:8080/items

curl -X POST http://localhost:8080/items \
     -H "Content-Type: application/json" \
     -d '{"name":"Гитара","emoji":"🎸","comment":"Yamaha F310"}'

curl http://localhost:8080/items
curl -X DELETE http://localhost:8080/items/1
```

---

## Шаг 3 — Docker (Модуль 3)

```bash
docker build -t my-collection .
docker run -d -p 8080:8080 --env-file .env my-collection
curl http://localhost:8080/items
docker stop $(docker ps -q --filter ancestor=my-collection)
```

---

## Шаг 4 — Docker Compose (Модуль 4)

```bash
docker compose up -d
docker compose logs -f
# Добавляем данные, затем перезапускаем:
docker compose down && docker compose up -d
curl http://localhost:8080/items   # Данные сохранились!
```

---

## Шаг 5 — Kubernetes (Модуль 5)

```bash
minikube start
eval $(minikube docker-env)
docker build -t my-collection .
kubectl apply -f k8s/
kubectl get pods
minikube service collection-service --url
```

---

## ✅ Чеклист

- [ ] `python app.py` — работает локально
- [ ] `docker build` — образ собирается
- [ ] `docker compose up -d` — сервис запускается
- [ ] Данные сохраняются после перезапуска
- [ ] `kubectl apply -f k8s/` — деплой прошёл
- [ ] Удалил Pod — K8s запустил новый автоматически
- [ ] Код в GitHub с понятными коммитами

---

## 🎓 Поздравляем!

Ты только что применил ВСЁ что изучил:
Linux + Git + Python + Docker + Compose + Kubernetes = **Junior DevOps!** 🚀

