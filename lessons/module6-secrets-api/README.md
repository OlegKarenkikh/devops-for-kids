# 🔐 Модуль 6 — Секреты и REST API (Уроки 29–35)

> **Цель:** научиться безопасно хранить пароли и токены, создать REST API на Python и подключить базу данных SQLite.

---

> 💡 **Что такое .env? REST = отдых? Что такое JSON?**  
> → [Ответы в Детском FAQ](../kids-faq/#модуль-6--секреты-и-api)


## Урок 29 — Почему нельзя писать пароль в коде?

![module6-env-dotenv](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-env-dotenv.jpg)

![module6-env-secrets](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-env-secrets.jpg)


### 🧠 Теория: почему пароль в коде = катастрофа

Представь: ты написал в коде `password = "мойСуперПароль"` и запушил на GitHub. GitHub индексирует **весь публичный код**. Существуют боты, которые сканируют GitHub в поисках паролей и токенов — и находят их за минуты. Реальные случаи: слитые AWS-ключи → счёт на $50 000 за одну ночь майнинга криптовалюты.

**Решение — переменные окружения:** код читает пароль из окружения (`os.environ`), а само значение хранится в `.env` файле, который **никогда не коммитится**.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-secrets-env.jpg" alt="Секреты — не в код, а в .env" width="85%"/>
<br/><em>Код на GitHub видят все. Пароль в коде = пароль для всех. .env решает эту проблему</em>
</div>

```bash
cat > .env << 'EOF'
DB_PASSWORD=МойСекрет123
API_KEY=abc123xyz
APP_PORT=8080
EOF
echo ".env" >> .gitignore
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

db_password = os.environ["DB_PASSWORD"]
api_key = os.environ.get("API_KEY", "default-key")
print("Ключ:", api_key[:3] + "***")
```

> **⚠️ Правило:** `.env` всегда в `.gitignore`. Без исключений.

---

## Урок 30 — .env в Docker и Compose



### 🧠 Теория: как .env попадает в контейнер?

Контейнер изолирован — он не видит файлы твоей машины. Как передать ему переменные окружения? Два способа:

| Способ | Команда | Когда использовать |
|--------|---------|-------------------|
| Один файл | `--env-file .env` | Docker run, для разработки |
| Compose-файл | `env_file: .env` | Docker Compose, основной способ |
| По одному | `-e KEY=value` | Одна переменная, скрипты |

Compose автоматически ищет `.env` в папке с `docker-compose.yml` — можно не указывать `env_file` явно, просто используй `${KEY}` в yaml и создай `.env` рядом.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-env-docker.jpg" alt=".env в Docker и Compose" width="85%"/>
<br/><em>Docker run с --env-file и Compose с env_file: переменные попадают внутрь контейнера</em>
</div>

```bash
docker run --env-file .env моё-приложение
```

```yaml
services:
  web:
    build: .
    env_file: .env
```

---

## Урок 31 — REST API

![module6-rest-api-flask](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-rest-api-flask.jpg)
: что это?

![module6-rest-api](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-rest-api.jpg)


### 🧠 Теория: HTTP запрос и ответ

Каждый раз когда ты открываешь сайт — твой браузер отправляет **HTTP запрос** серверу, а сервер присылает **HTTP ответ**.

```
Запрос:                          Ответ:
GET /items HTTP/1.1              HTTP/1.1 200 OK
Host: api.example.com     →      Content-Type: application/json
Authorization: Bearer xxx        
                                 {"items": [...]}
```

**REST** — это соглашение о том, как строить API: один URL = один ресурс, HTTP-метод = действие над ним. REST = **Re**presentational **S**tate **T**ransfer — «передача представления состояния». В быту: стандартный способ для сервисов общаться по HTTP.

**JSON** (JavaScript Object Notation) — формат данных для передачи по API:
```json
{"name": "яблоко", "count": 5, "fresh": true}
```

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-rest-api.jpg" alt="REST API" width="85%"/>
<br/><em>API — официант между клиентом и сервером</em>
</div>

| HTTP метод | Действие | Аналогия |
|-----------|---------|---------|
| `GET` | Получить данные | «Покажи меню» |
| `POST` | Создать новое | «Хочу заказать пиццу» |
| `PUT` | Обновить | «Замени пиццу на суп» |
| `DELETE` | Удалить | «Отмени заказ» |

---

## Урок 32 — Первый API на Flask



### 🧠 Теория: что такое декоратор @app.route?

**Декоратор** `@app.route("/items")` говорит Flask: «когда придёт запрос на URL `/items` — вызови функцию прямо под мной». Это связывает URL с Python-функцией.

```python
# Как это работает:
@app.route("/items", methods=["GET"])  # ← этот URL + этот метод
def get_all():                          # ← вызывает эту функцию
    return jsonify({"items": []})       # ← которая возвращает JSON
```

**Flask** — минимальный веб-фреймворк для Python. Делает одно: принимает HTTP запросы и вызывает твои функции. Весь код API — это просто обычные Python-функции с декораторами.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-flask-routes.jpg" alt="Flask декораторы и маршруты" width="85%"/>
<br/><em>@app.route связывает URL с Python-функцией. GET /items → get_all(), POST /items → create()</em>
</div>

```python
from flask import Flask, jsonify, request
app = Flask(__name__)
items = [{"id": 1, "name": "яблоко", "emoji": "🍎"}]

@app.route("/items", methods=["GET"])
def get_all():
    return jsonify({"items": items, "count": len(items)})

@app.route("/items", methods=["POST"])
def create():
    data = request.get_json()
    new = {"id": len(items)+1, "name": data["name"], "emoji": data.get("emoji","📦")}
    items.append(new)
    return jsonify(new), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
```

---

## Урок 33 — SQLite: база данных в одном файле

![module6-sqlite-db](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-sqlite-db.jpg)

![module6-sqlite](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-sqlite.jpg)




### 🧠 Теория: что такое реляционная база данных?

**База данных** — это организованное хранилище данных. **Реляционная** — значит данные хранятся в **таблицах** (как Excel), а таблицы могут быть связаны между собой.

```
Таблица items:
┌────┬─────────┬───────┐
│ id │ name    │ emoji │
├────┼─────────┼───────┤
│  1 │ Гитара  │  🎸   │
│  2 │ Кот     │  🐱   │
│  3 │ Книга   │  📚   │
└────┴─────────┴───────┘
```

**SQL** (Structured Query Language) — язык запросов к таблицам:
- `SELECT * FROM items` — дай все строки
- `INSERT INTO items VALUES (...)` — добавь строку
- `UPDATE items SET name='...' WHERE id=1` — измени строку
- `DELETE FROM items WHERE id=2` — удали строку

**SQLite** — база данных в одном `.db` файле. Не нужен отдельный сервер. Идеально для обучения и маленьких проектов.

> SQLite — это база данных, которая живёт в **одном файле** на диске. Не нужно устанавливать никаких серверов!

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-sqlite-table.jpg" alt="SQLite таблица и SQL запросы" width="85%"/>
<br/><em>SQLite = один файл .db. SELECT читает строки, INSERT добавляет, DELETE удаляет</em>
</div>

```python
import sqlite3

db = sqlite3.connect("items.db")

db.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT NOT NULL,
        emoji TEXT DEFAULT '📦'
    )
""")
db.commit()

db.execute("INSERT INTO items (name, emoji) VALUES (?, ?)", ("Гитара", "🎸"))
db.commit()

rows = db.execute("SELECT * FROM items").fetchall()
for row in rows:
    print(row)

db.close()
```

```bash
# Попробуй прямо в терминале (база в памяти):
python3 -c "
import sqlite3
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE t (id INTEGER PRIMARY KEY, val TEXT)')
db.execute(\"INSERT INTO t (val) VALUES ('Привет!')\")
db.execute(\"INSERT INTO t (val) VALUES ('Мир!')\")
db.commit()
print(db.execute('SELECT * FROM t').fetchall())
db.close()
"
```

### SQLite + Flask API

```python
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = "collection.db"

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            emoji TEXT DEFAULT '📦'
        )
    """)
    db.commit()
    db.close()

@app.route("/items", methods=["GET"])
def get_all():
    db = get_db()
    rows = db.execute("SELECT * FROM items").fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])

@app.route("/items", methods=["POST"])
def create():
    data = request.get_json()
    db = get_db()
    cur = db.execute(
        "INSERT INTO items (name, emoji) VALUES (?, ?)",
        (data["name"], data.get("emoji", "📦"))
    )
    db.commit()
    new_id = cur.lastrowid
    db.close()
    return jsonify({"id": new_id, "name": data["name"]}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
```

> **📝 Задание:** запусти API, добавь через curl 3 своих любимых вещи и получи список обратно.

---

## Урок 34 — Kubernetes Secrets: хранение паролей в кластере

![module6-k8s-secrets](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-k8s-secrets.jpg)


![module6-jwt-token](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-jwt-token.jpg)


### 🧠 Теория: почему Secret хранится в base64?

Kubernetes Secret хранит данные в **base64** — это НЕ шифрование! Base64 — просто способ закодировать любые байты в текст (чтобы JSON/YAML не ломался от спецсимволов). Декодировать может кто угодно:

```bash
echo "МойПароль123" | base64          # → 0J3QvtC5UGFyb2xsMTIz
echo "0J3QvtC5UGFyb2xsMTIz" | base64 -d  # → МойПароль123
```

**Реальная защита** Secrets — это RBAC (права доступа): не все пользователи кластера могут читать Secrets, только авторизованные сервисы. Для продакшна используют также `etcd` encryption at rest.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-secrets-vault.jpg" alt="Kubernetes Secrets — сейф в кластере" width="85%"/>
<br/><em>Secret в Kubernetes — как сейф внутри кластера. Пароль хранится отдельно от кода</em>
</div>

> Разница `.env` vs K8s Secret:
> - `.env` — для локальной разработки и Docker Compose
> - `K8s Secret` — для продакшн-кластера Kubernetes

```bash
kubectl create secret generic db-secret \
  --from-literal=db-password=МойПароль123 \
  --from-literal=api-key=abc123xyz

kubectl get secrets
kubectl describe secret db-secret

kubectl get secret db-secret -o jsonpath='{.data.db-password}' | base64 -d
```

```yaml
# pod-with-secret.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: app
    image: my-collection:latest
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: db-password
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: api-key
```

```bash
kubectl apply -f pod-with-secret.yaml
kubectl exec -it my-app -- env | grep DB_PASSWORD
```

---

## Урок 35 — Шпаргалка

| Правило | Почему |
|---------|--------|
| Пароли в `.env` | Код открыт, .env закрыт |
| `.env` в `.gitignore` | Иначе GitHub увидит |
| `os.environ.get("KEY")` | Безопасное чтение |
| `app.run()` в `if __name__` | Не запускать при импорте |
| 200 = OK | Всё хорошо |
| 201 = Создано | POST успешен |
| 404 = Не найдено | Ресурс отсутствует |
| 500 = Ошибка сервера | Что-то сломалось |

### Команды K8s Secrets

| Команда | Действие |
|---------|---------|
| `kubectl create secret generic имя --from-literal=ключ=значение` | Создать |
| `kubectl get secrets` | Список |
| `kubectl describe secret имя` | Детали |
| `kubectl delete secret имя` | Удалить |


---

## 🎯 Практические задания

### Задание 1 — Flask API с нуля
```bash
mkdir flask-api && cd flask-api
python3 -m venv venv && source venv/bin/activate
pip install flask

cat > app.py << 'EOF'
from flask import Flask, jsonify, request
app = Flask(__name__)

items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    items.append(data)
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
EOF

python app.py
```
```bash
# В другом терминале — тестируем API:
curl http://localhost:5000/items
curl -X POST http://localhost:5000/items \
     -H "Content-Type: application/json" \
     -d '{"name": "учебник", "topic": "DevOps"}'
curl http://localhost:5000/items
```
> ✅ Видишь JSON с твоим объектом? REST API работает!

### Задание 2 — .env файл
```bash
cat > .env << 'EOF'
SECRET_KEY=mysuperpassword123
APP_PORT=5001
EOF

pip install python-dotenv

# Добавь в app.py:
# from dotenv import load_dotenv; import os
# load_dotenv()
# secret = os.environ.get("SECRET_KEY")
# print(f"Секрет загружен: {secret[:4]}****")
```
> ✅ Никогда не добавляй .env в git!

### Задание 3 — Kubernetes Secret
```bash
# Создай секрет
kubectl create secret generic my-secret \
  --from-literal=db-password=supersecret123

# Проверь (значение закодировано в base64)
kubectl get secret my-secret -o yaml

# Декодируй:
kubectl get secret my-secret -o jsonpath='{.data.db-password}' | base64 -d
```


---

## 🧩 Быстрый тест — проверь себя

| Вопрос | Ответ |
|--------|-------|
| Почему нельзя хранить пароли в коде? | Они попадут в git и будут видны всем |
| Что делает `os.getenv("DB_PASSWORD")`? | Читает переменную окружения из .env |
| Что такое REST API? | Сервер отвечает на HTTP-запросы данными в формате JSON |
| Из чего состоит JWT-токен? | Header.Payload.Signature (три части через точку) |
| Чем K8s Secret отличается от .env? | Secret живёт в кластере, зашифрован, управляется kubectl |
| Что такое SQLAlchemy? | ORM: работа с базой через Python-объекты, без SQL |

## 🧠 Чекпойнт понимания — обязательный

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/checkpoint.jpg" alt="Чекпойнт понимания" width="90%"/>
<br/><em>Три вопроса после каждого урока. Понимание важнее скорости.</em>
</div>

Ты прошёл весь основной курс! Финальная проверка — ответь себе вслух или письменно:

**1. Почему нельзя хранить пароли в коде или в git-репозитории? Что случится если утечёт?**

**2. Чем `.env` файл отличается от Kubernetes Secret? Когда что использовать?**

**3. Что такое JWT-токен? Из каких трёх частей он состоит?**

**4. Объясни полный путь запроса: пользователь нажал кнопку → Flask получил запрос → данные сохранились в SQLite. Что происходит на каждом шаге?**

> 🏆 Если ответил на все 4 вопроса — ты готов к итоговому проекту! Переходи в `projects/`

➡️ [Итоговый проект →](../../projects/final-project/)