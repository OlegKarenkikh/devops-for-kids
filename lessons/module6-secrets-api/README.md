# 🔐 Модуль 6 — Секреты и REST API (Уроки 29–35)

> **Цель:** научиться безопасно хранить пароли и токены, и создать первый REST API на Python.

---

## Урок 29 — Почему нельзя писать пароль в коде?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-secrets-env.jpg" alt="Секреты — не в код, а в .env" width="85%"/>
<br/><em>Код на GitHub видят все. Пароль в коде = пароль для всех. .env решает эту проблему</em>
</div>

> Представь: ты написал пароль прямо в коде и запушил на GitHub. Теперь его видит весь мир!

```bash
# Создаём .env файл
cat > .env << 'EOF'
DB_PASSWORD=МойСекрет123
API_KEY=abc123xyz
APP_PORT=8080
EOF

# ОБЯЗАТЕЛЬНО добавить в .gitignore
echo ".env" >> .gitignore
```

```python
# app.py — читаем секреты из окружения
import os
from dotenv import load_dotenv

load_dotenv()   # Загружает .env файл автоматически

db_password = os.environ["DB_PASSWORD"]
api_key     = os.environ.get("API_KEY", "default-key")

print("Ключ:", api_key[:3] + "***")  # Никогда не печатай целиком!
```

> **⚠️ Правило:** `.env` всегда в `.gitignore`. Без исключений.

---

## Урок 30 — .env в Docker и Compose

```bash
docker run --env-file .env моё-приложение
```

```yaml
# docker-compose.yml
services:
  web:
    build: .
    env_file: .env
```

---

## Урок 31 — REST API: что это?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-rest-api.jpg" alt="REST API — как меню в ресторане" width="85%"/>
<br/><em>API — официант между клиентом и сервером</em>
</div>

| HTTP метод | Действие | Аналогия |
|-----------|---------|---------|
| `GET` | Получить данные | «Покажи меню» |
| `POST` | Создать новое | «Хочу заказать пиццу» |
| `PUT` | Обновить | «Замени пиццу на суп» |
| `DELETE` | Удалить | «Отмени заказ» |

```bash
curl http://localhost:8080/items
curl -X POST http://localhost:8080/items -H "Content-Type: application/json" -d '{"name":"яблоко"}'
```

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

```bash
pip install flask
python app.py
curl http://localhost:8080/items
```

---

## Урок 33–34 — SQLite и Secrets в Kubernetes

```python
import sqlite3
db = sqlite3.connect("items.db")
db.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)")
db.commit()
```

```bash
kubectl create secret generic my-secret --from-literal=db-password=СекретныйПароль
kubectl get secrets
```

---

## Урок 35 — Шпаргалка

| Правило | Почему |
|---------|--------|
| Пароли в `.env` | Код открыт, .env закрыт |
| `.env` в `.gitignore` | Иначе GitHub увидит |
| `os.environ.get("KEY")` | Безопасное чтение |
| 200=OK, 201=Создано, 404=Не найдено, 500=Ошибка сервера | HTTP коды |

➡️ [Итоговый проект →](../../projects/final-project/)
