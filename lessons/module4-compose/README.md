# 🎼 Модуль 4 — Docker Compose (Уроки 12–13)

> **Цель:** запускать несколько взаимосвязанных сервисов одной командой.

---

## 📖 Урок 12 — Docker Compose

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-compose-diagram.png" alt="Docker Compose — квартиры в доме" width="85%"/>
<br/><em>Compose — как многоквартирный дом: каждый сервис живёт отдельно, но рядом</em>
</div>

### 🧠 Объяснение

Настоящие приложения состоят из нескольких частей: сайт, база данных, кеш. Docker Compose запускает все **одной командой** `docker compose up`.

### 💻 Структура docker-compose.yml

```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine

volumes:
  pgdata:
```

### 💻 Команды

```bash
docker compose up -d          # Запустить все
docker compose ps             # Статус
docker compose logs -f        # Следить за логами
docker compose stop           # Остановить
docker compose down           # Удалить контейнеры
docker compose down -v        # + удалить тома
docker compose exec db bash   # Войти в сервис
```

### 💻 Практика: сайт + PostgreSQL

```bash
mkdir compose-проект && cd compose-проект
mkdir html
echo "<h1>🐳 Мой Compose-сайт!</h1>" > html/index.html
```

**docker-compose.yml:**
```yaml
version: "3.9"
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: секрет
      POSTGRES_DB: моя_база
    volumes:
      - pgdata:/var/lib/postgresql/data
  adminer:
    image: adminer
    ports:
      - "8081:8080"
volumes:
  pgdata:
```

```bash
docker compose up -d
# Браузер: http://localhost:8080 — сайт
# Браузер: http://localhost:8081 — база данных
```

### 🧪 Задание 12

```bash
docker compose exec db psql -U postgres -d моя_база
# Внутри psql:
CREATE TABLE фрукты (название TEXT, цена INT);
INSERT INTO фрукты VALUES ('яблоко', 50), ('банан', 30);
SELECT * FROM фрукты;
\q
docker compose down
```

---

## 📖 Урок 13 — Переменные окружения и безопасность

```bash
# .env файл — НИКОГДА не добавляй в Git!
echo "DB_PASSWORD=МойСекрет" > .env
echo ".env" >> .gitignore
```

В `docker-compose.yml`:
```yaml
environment:
  POSTGRES_PASSWORD: ${DB_PASSWORD}   # из .env
```

### 💻 healthcheck

```yaml
db:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 10s
    retries: 5
web:
  depends_on:
    db:
      condition: service_healthy   # Ждать готовности БД
```

---

## 📋 Шпаргалка Модуля 4

| Команда | Что делает |
|---------|-----------|
| `docker compose up -d` | Запустить |
| `docker compose ps` | Статус |
| `docker compose logs -f` | Логи |
| `docker compose down -v` | Удалить с данными |
| `docker compose exec сервис bash` | Войти |

➡️ [Следующий модуль: Kubernetes →](../module5-kubernetes/)
