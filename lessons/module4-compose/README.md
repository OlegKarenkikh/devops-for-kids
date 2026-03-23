# 🎼 Модуль 4 — Docker Compose (Уроки 12–13)

> **Цель:** научиться запускать несколько взаимосвязанных сервисов одной командой.

---

## 📖 Урок 12 — Docker Compose: несколько сервисов

### 🧠 Объяснение

Настоящие приложения состоят из нескольких частей: веб-сервер, база данных, кеш. Запускать каждую по отдельности неудобно. **Docker Compose** запускает все сразу одной командой!

> **Аналогия:** Это как многоквартирный дом. Каждый контейнер — отдельная квартира. Все живут рядом и могут общаться, но не мешают друг другу.

### 💻 Структура docker-compose.yml

```yaml
version: "3.9"

services:
  web:
    build: .                   # Собрать из Dockerfile
    ports:
      - "8080:8080"            # Проброс порта
    depends_on:
      - db                     # Стартует после db
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    restart: unless-stopped    # Перезапустить при сбое

  db:
    image: postgres:15-alpine  # Готовый образ
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data  # Сохранение данных

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  db_data:                     # Именованный том
```

### 💻 Команды

```bash
docker compose up -d           # Запустить все сервисы
docker compose ps              # Статус сервисов
docker compose logs            # Логи всех
docker compose logs -f web     # Логи конкретного
docker compose stop            # Остановить (данные сохр.)
docker compose down            # Остановить + удалить
docker compose down -v         # Удалить вместе с томами
docker compose exec db psql -U postgres  # Войти в сервис
docker compose build           # Пересобрать образы
docker compose pull            # Обновить образы
```

### 💻 Практика: сайт + база данных

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
      POSTGRES_PASSWORD: секрет123
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
docker compose ps
# Браузер: http://localhost:8080 — сайт
# Браузер: http://localhost:8081 — база данных
```

### 🧪 Задание

```bash
# Войди в PostgreSQL:
docker compose exec db psql -U postgres -d моя_база

# Внутри psql:
CREATE TABLE фрукты (название TEXT, цена INT);
INSERT INTO фрукты VALUES ('яблоко', 50), ('банан', 30);
SELECT * FROM фрукты;
\q

# Останови всё:
docker compose down
```

---

## 📖 Урок 13 — Переменные окружения и безопасность

### 💻 Файл .env — безопасное хранение секретов

```bash
# Создай .env:
cat > .env << 'EOF'
DB_PASSWORD=МойСекрет123
DB_NAME=моя_база
APP_PORT=5000
EOF

# ОБЯЗАТЕЛЬНО добавь в .gitignore:
echo ".env" >> .gitignore
```

Используй в `docker-compose.yml`:
```yaml
services:
  db:
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}    # из .env
      POSTGRES_DB: ${DB_NAME}
  web:
    ports:
      - "${APP_PORT}:5000"
```

### 💻 healthcheck — проверка здоровья сервиса

```yaml
services:
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    depends_on:
      db:
        condition: service_healthy   # Ждать пока db готова
```

---

## 📋 Шпаргалка Модуля 4

| Команда | Что делает |
|---------|-----------|
| `docker compose up -d` | Запустить все сервисы |
| `docker compose ps` | Статус |
| `docker compose logs -f` | Следить за логами |
| `docker compose stop` | Остановить |
| `docker compose down` | Удалить контейнеры |
| `docker compose down -v` | Удалить с данными |
| `docker compose exec сервис bash` | Войти в сервис |
| `docker compose build` | Пересобрать |
