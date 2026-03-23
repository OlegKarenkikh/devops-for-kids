# 🎼 Модуль 4 — Docker Compose + Мониторинг (Уроки 16–20)

> **Цель:** связать контейнеры, собрать полный стек, наблюдать за системой через Prometheus и Grafana.

---

## Урок 16 — Docker Compose: несколько сервисов

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-code-to-compose.jpg" alt="От кода до Compose" width="85%"/>
<br/><em>Последний шаг пути: docker-compose.yml объединяет все контейнеры как здания в городе</em>
</div>

### 🧠 Зачем Compose?

Настоящее приложение = несколько частей. Вместо трёх команд `docker run` — одна: `docker compose up`.

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    build: .            # Собрать из Dockerfile
    ports:
      - "8080:8080"
    environment:
      APP_NAME: "Мой составной сайт"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      retries: 5

  cache:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  pgdata:
```

```bash
# .env файл (НЕ добавлять в Git!)
echo "DB_PASSWORD=МойСекрет123" > .env
echo ".env" >> .gitignore

docker compose up -d        # Запустить всё
docker compose ps           # Статус
docker compose logs -f      # Логи всех
docker compose down         # Остановить
docker compose down -v      # + удалить тома
```

---

## Урок 17 — Полный проект: код → Dockerfile → Compose

### Структура проекта

```
мой-проект/
├── app.py              ← наш Python-сервер
├── Dockerfile          ← рецепт образа
├── docker-compose.yml  ← оркестрация
├── .env                ← секреты (не в Git!)
├── .gitignore
└── README.md
```

### app.py (с подключением к Redis)

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, datetime, os

VISITS = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global VISITS
        VISITS += 1
        data = {
            "сервис": os.environ.get("APP_NAME", "Сайт"),
            "визиты": VISITS,
            "версия": "2.0",
            "время": datetime.datetime.now().isoformat()
        }
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {fmt % args}")

HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), Handler).serve_forever()
```

### docker-compose.yml с мониторингом

```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      APP_NAME: "Мой сайт v2"
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      retries: 5

  cache:
    image: redis:7-alpine

  # Мониторинг контейнеров
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - "8081:8080"

volumes:
  pgdata:
```

```bash
docker compose up -d
curl http://localhost:8080         # Сайт
open http://localhost:8081         # cAdvisor — метрики контейнеров
```

---

## Урок 18 — Prometheus: собираем метрики

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-prometheus-grafana.jpg" alt="Prometheus + Grafana" width="85%"/>
<br/><em>Прометей — детектив: каждые 15 сек обходит все сервисы и записывает числа. Grafana рисует графики</em>
</div>

### 🧠 Что такое метрики?

> Представь спидометр в машине. Он показывает скорость в реальном времени. **Prometheus** — это спидометр для твоего сервера.

**Типы метрик:**
- `cpu_usage` — загрузка процессора
- `memory_usage` — использование памяти
- `http_requests_total` — сколько запросов пришло
- `container_up` — работает ли контейнер

### prometheus.yml

```yaml
global:
  scrape_interval: 15s    # Собирать каждые 15 секунд

scrape_configs:
  - job_name: 'docker-containers'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

### Добавить в docker-compose.yml

```yaml
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=7d'
```

```bash
docker compose up -d
open http://localhost:9090        # Prometheus UI
# Попробуй запросы (PromQL):
# container_memory_usage_bytes
# rate(container_cpu_usage_seconds_total[5m])
```

---

## Урок 19 — Grafana: красивые дашборды

```yaml
# Добавить в docker-compose.yml:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

volumes:
  pgdata:
  grafana_data:
```

```bash
docker compose up -d
open http://localhost:3000   # Grafana (admin/admin)
```

### Настройка Grafana

1. **Войти:** admin / admin
2. **Добавить источник данных:** Configuration → Data Sources → Add → Prometheus → URL: `http://prometheus:9090`
3. **Импортировать дашборд:** Dashboards → Import → ID `193` (Docker готовый дашборд)
4. **Готово!** Графики CPU, RAM, сети для всех контейнеров

### Алертинг

```yaml
# В Grafana: Alerting → Alert Rules → New Alert Rule
# Условие: container_memory_usage_bytes > 500MB
# Уведомление: Email / Telegram
```

---

## Урок 20 — Итоговый проект

Полный стек: **Python-сайт + PostgreSQL + Redis + Prometheus + Grafana**

```bash
# Финальный docker-compose up
mkdir итоговый-проект && cd итоговый-проект

# Скопировать все файлы:
# app.py, Dockerfile, docker-compose.yml, prometheus.yml, .env

docker compose up -d
docker compose ps          # Все сервисы запущены?
docker compose logs -f     # Смотрим логи

# Проверяем:
curl http://localhost:8080        # Сайт
open http://localhost:8081        # cAdvisor
open http://localhost:9090        # Prometheus
open http://localhost:3000        # Grafana

# Масштабируем:
docker compose up -d --scale web=3   # 3 экземпляра сайта!
docker compose logs -f web

# Уборка после урока:
docker compose down -v
docker system prune -f
```

---

## 📋 Полная шпаргалка Модуля 4

| Команда | Что делает |
|---------|-----------|
| `docker compose up -d` | Запустить всё |
| `docker compose ps` | Статус сервисов |
| `docker compose logs -f` | Логи всех сервисов |
| `docker compose exec web bash` | Войти в сервис |
| `docker compose down` | Остановить |
| `docker compose down -v` | Остановить + удалить данные |
| `docker compose up --scale web=3` | Масштабировать |

### 🔗 Порты нашего стека

| Сервис | Порт | URL |
|--------|------|-----|
| Наш сайт | 8080 | http://localhost:8080 |
| cAdvisor | 8081 | http://localhost:8081 |
| Prometheus | 9090 | http://localhost:9090 |
| Grafana | 3000 | http://localhost:3000 |

➡️ [Следующий модуль: Kubernetes →](../module5-kubernetes/)
