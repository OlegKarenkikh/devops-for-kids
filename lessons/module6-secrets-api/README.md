# 🔐 Модуль 6 — Секреты, REST API, JWT и API Gateway (Уроки 29–35)

> **Цель:** научиться безопасно хранить пароли, строить API-сервисы и защищать их токенами.

---

## Урок 29 — .env файл: конверт с настройками

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-dotenv.jpg" alt=".env файл — секреты не в коде" width="85%"/>
<br/><em>.env — конверт с паролями. Код читает его, но в Git он не попадает</em>
</div>

### 🧠 Зачем .env?

> Представь, что ты написал сайт и сохранил пароль от базы данных прямо в коде. Потом залил на GitHub. Теперь твой пароль видит весь мир. Это плохо! 😱

**.env** — отдельный файл с настройками, который **не добавляется в Git**.

```bash
# .env (создать в корне проекта)
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SECRET_KEY=мой-супер-секретный-ключ-12345
DEBUG=false
API_KEY=sk-abcdef1234567890
PORT=8080
REDIS_URL=redis://localhost:6379
```

### Python — читаем .env

```python
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # Читаем .env файл

db_url  = os.environ.get("DATABASE_URL")
secret  = os.environ.get("SECRET_KEY")
port    = int(os.environ.get("PORT", 8080))  # 8080 по умолчанию

print(f"Сервер на порту: {port}")
print(f"DB: {db_url}")
```

### Node.js — читаем .env

```javascript
// npm install dotenv
require('dotenv').config();

const port   = process.env.PORT || 8080;
const dbUrl  = process.env.DATABASE_URL;
const secret = process.env.SECRET_KEY;

console.log(`Сервер стартует на порту ${port}`);
```

### .gitignore — обязательно!

```bash
# .gitignore
.env
.env.local
.env.production
*.env

# Проверить что .env не в Git:
git status          # .env не должен появляться
git ls-files .env   # Если пусто — всё правильно
```

### .env.example — шаблон для команды

```bash
# .env.example (ДОБАВЛЯЕМ в Git — без реальных значений)
DATABASE_URL=postgresql://user:PASSWORD@localhost:5432/DB_NAME
SECRET_KEY=YOUR_SECRET_KEY_HERE
DEBUG=false
PORT=8080
```

> **📝 Задание:** создай `.env`, прочитай его в Python-скрипте, убедись что `.env` в `.gitignore`.

---

## Урок 30 — Секреты: где хранить пароли?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-secrets-vault.jpg" alt="Vault — банк для секретов" width="85%"/>
<br/><em>Vault — банковский сейф для паролей. Каждый получает только свой секрет</em>
</div>

### Уровни защиты секретов

| Уровень | Где хранить | Для чего |
|---------|------------|---------|
| 🟡 Базовый | `.env` файл | Локальная разработка |
| 🟠 CI/CD | GitHub Secrets | Деплой и пайплайны |
| 🔴 Прод | HashiCorp Vault / Azure Key Vault | Боевые приложения |

---

## Урок 31 — GitHub Secrets и Azure Key Vault

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-github-azure-secrets.jpg" alt="GitHub Secrets vs Azure Key Vault" width="85%"/>
<br/><em>GitHub — для пайплайнов, Azure — для приложений в облаке. Оба скрывают реальные пароли</em>
</div>

### GitHub Secrets — для CI/CD

```bash
# Настройка: GitHub → Репозиторий → Settings → Secrets and variables → Actions
# Добавить: DOCKER_PASSWORD = мой_пароль

# Использование в .github/workflows/deploy.yml:
```

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Docker Login
        run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build & Push
        run: |
          docker build -t myapp .
          docker push myapp
        env:
          APP_SECRET: ${{ secrets.APP_SECRET_KEY }}   # Доступен как переменная
```

### HashiCorp Vault — для production

```bash
# Установка (Ubuntu)
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt install vault

# Запуск в dev-режиме (для учёбы)
vault server -dev &
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Запись секрета
vault kv put secret/myapp     db_password="СуперСекрет123"     api_key="sk-abc123"

# Чтение секрета
vault kv get secret/myapp
vault kv get -field=db_password secret/myapp

# Из Python:
# pip install hvac
import hvac, os
client = hvac.Client(url='http://vault:8200', token=os.environ['VAULT_TOKEN'])
secret = client.secrets.kv.read_secret_version(path='myapp')
db_pass = secret['data']['data']['db_password']
```

---

## Урок 32 — REST API: официант между сервером и клиентом

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-rest-api.jpg" alt="REST API как ресторан" width="85%"/>
<br/><em>API — как официант: клиент делает заказ (запрос), официант несёт его на кухню (сервер) и возвращает блюдо (ответ)</em>
</div>

### 🧠 Что такое REST API?

> **REST** (Representational State Transfer) — это правила, по которым программы общаются через интернет. Как язык жестов для программ.

### Основные правила REST

| HTTP-метод | Действие | Аналогия |
|-----------|---------|---------|
| `GET` | Получить данные | Посмотреть меню |
| `POST` | Создать что-то новое | Сделать заказ |
| `PUT` | Заменить целиком | Изменить весь заказ |
| `PATCH` | Изменить частично | Убрать лук из блюда |
| `DELETE` | Удалить | Отменить заказ |

### Простой Python REST API

```python
# pip install flask
from flask import Flask, jsonify, request

app = Flask(__name__)

# Простая "база данных"
пользователи = [
    {"id": 1, "имя": "Алиса", "роль": "admin"},
    {"id": 2, "имя": "Боб",   "роль": "user"},
]

# GET /api/users — получить всех
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(пользователи)

# GET /api/users/1 — получить одного
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in пользователи if u['id'] == user_id), None)
    if not user:
        return jsonify({"ошибка": "Не найден"}), 404
    return jsonify(user)

# POST /api/users — создать нового
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = {"id": len(пользователи) + 1, "имя": data['имя'], "роль": "user"}
    пользователи.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

```bash
# Тестирование API
curl http://localhost:8080/api/users
curl http://localhost:8080/api/users/1
curl -X POST http://localhost:8080/api/users \
     -H "Content-Type: application/json" \
     -d '{"имя": "Коля"}'
```

---

## Урок 33 — JWT токен: поезд из трёх вагонов

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-jwt-token.jpg" alt="JWT токен из трёх частей" width="85%"/>
<br/><em>JWT — поезд: header (тип подписи) + payload (кто ты) + signature (печать сервера). Нельзя подделать!</em>
</div>

### Как работает JWT

```
1. Пользователь входит → сервер выдаёт JWT токен
2. Клиент сохраняет токен (localStorage / cookie)
3. С каждым запросом клиент отправляет: Authorization: Bearer <token>
4. Сервер проверяет подпись → разрешает или отказывает
```

### JWT в Python

```python
# pip install pyjwt
import jwt, datetime, os

SECRET = os.environ.get("JWT_SECRET", "супер-секрет")

# Создать токен (при логине)
def create_token(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

# Проверить токен (при каждом запросе)
def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise Exception("Токен истёк!")
    except jwt.InvalidTokenError:
        raise Exception("Неверный токен!")

# Пример использования
token = create_token(user_id=42, role="admin")
print(f"Токен: {token[:50]}...")

data = verify_token(token)
print(f"Пользователь: {data['user_id']}, роль: {data['role']}")
```

### API Key vs JWT

| | API Key | JWT |
|-|---------|-----|
| **Что это** | Случайная строка | Подписанный JSON |
| **Хранит данные** | Нет (только ID) | Да (роль, имя...) |
| **Отозвать** | Удалить из БД | Подождать истечения |
| **Используется** | Сервис-к-сервису | Пользователь-к-API |
| **Пример** | `sk-abc123...` | `eyJhbGci...` |

---

## Урок 34 — API Gateway: Gravitee

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module6-api-gateway-jwt.jpg" alt="API Gateway — охранник у входа" width="85%"/>
<br/><em>API Gateway — как охранник в клубе: проверяет кто ты, ведёт журнал, перенаправляет в нужный зал (сервис)</em>
</div>

### 🧠 Зачем API Gateway?

> Представь большой торговый центр. Один вход — охранник. Внутри много магазинов (микросервисов). Охранник проверяет всех на входе — чтобы каждый магазин не ставил собственного охранника.

**API Gateway решает:**
- Аутентификация (JWT, API Key) — один раз для всех
- Rate limiting (не больше 100 запросов/минуту)
- Логирование всех запросов
- Балансировка нагрузки
- SSL-терминация

### Gravitee — запуск через Docker Compose

```yaml
# docker-compose-gravitee.yml
version: "3.9"

services:
  mongodb:
    image: mongo:5.0
    volumes:
      - mongo_data:/data/db

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - es_data:/usr/share/elasticsearch/data

  gateway:
    image: graviteeio/apim-gateway:3.20
    ports:
      - "8082:8082"
    environment:
      - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee
    depends_on:
      - mongodb
      - elasticsearch

  management-api:
    image: graviteeio/apim-management-api:3.20
    ports:
      - "8083:8083"
    environment:
      - gravitee_management_mongodb_uri=mongodb://mongodb:27017/gravitee

  management-ui:
    image: graviteeio/apim-management-ui:3.20
    ports:
      - "80:8080"

volumes:
  mongo_data:
  es_data:
```

```bash
docker compose -f docker-compose-gravitee.yml up -d
open http://localhost        # Gravitee UI (admin/admin)
# Gateway слушает: http://localhost:8082
```

### Политики Gravitee

```json
{
  "policies": [
    {
      "name": "jwt",
      "configuration": {
        "signature": "HS256",
        "secretKey": "мой-секрет"
      }
    },
    {
      "name": "rate-limit",
      "configuration": {
        "rate": {"limit": 100, "periodTime": 1, "periodTimeUnit": "MINUTES"}
      }
    }
  ]
}
```

---

## Урок 35 — Итоговый проект: защищённый API

```
📁 secure-api/
├── .env                  ← секреты
├── .env.example          ← шаблон для команды
├── .gitignore            ← скрываем .env
├── app.py                ← Flask REST API с JWT
├── Dockerfile
├── docker-compose.yml    ← app + postgres + redis
└── README.md
```

```bash
# Запуск
docker compose up -d
curl http://localhost:8080/api/users          # 401 — нет токена!

# Получить токен
curl -X POST http://localhost:8080/auth/login \
  -d '{"username":"admin","password":"secret"}'
# Ответ: {"token": "eyJhbG..."}

# Использовать с токеном
curl http://localhost:8080/api/users \
  -H "Authorization: Bearer eyJhbG..."      # 200 OK ✅
```

---

## 📋 Шпаргалка: Безопасность

| Что | Где хранить | Никогда |
|-----|------------|---------|
| DB пароль | `.env` / Vault | В коде |
| API ключ | GitHub Secrets | В репозитории |
| SSH ключ | `~/.ssh/` (chmod 600) | В Git/чате |
| JWT secret | Vault / env var | Hardcode в коде |

➡️ [Следующий модуль: Финальный проект →](../projects/)
