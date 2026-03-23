# 🔐 Модуль 6 — Секреты и REST API (Уроки 29–35)

> **Цель:** научиться безопасно хранить пароли и токены, создать REST API на Python и подключить базу данных SQLite.

---

## Урок 29 — Почему нельзя писать пароль в коде?

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

## Урок 31 — REST API: что это?

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

> SQLite — это база данных, которая живёт в **одном файле** на диске. Не нужно устанавливать никаких серверов!

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

➡️ [Итоговый проект →](../../projects/final-project/)