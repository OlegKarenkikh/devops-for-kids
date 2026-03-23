# 🎼 Модуль 4 — Docker Compose + Мониторинг (Уроки 19–23)

> **Цель:** запускать несколько сервисов одной командой и наблюдать за ними через Prometheus + Grafana.

---

## Урок 19 — Docker Compose: город сервисов

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-compose-network.jpg" alt="Docker Compose — город сервисов" width="85%"/>
<br/><em>Compose = целый город из сервисов. Один файл — один запуск. Все сервисы видят друг друга по имени</em>
</div>

### 🧠 Зачем Compose?

> Настоящее приложение — несколько частей: сайт, база данных, кэш. Compose запускает их все вместе одной командой.

```yaml
# docker-compose.yml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      retries: 5

  cache:
    image: redis:7-alpine

volumes:
  pgdata:
```

```bash
echo "DB_PASSWORD=Секрет123" > .env
docker compose up -d        # Запустить всё
docker compose ps           # Статус
docker compose logs -f      # Логи всех
docker compose down         # Остановить
docker compose down -v      # + удалить тома
```

---

## Урок 20–21 — Полный проект: код → контейнер → Compose

```python
# app.py
from flask import Flask, jsonify
import os, datetime

app = Flask(__name__)
visits = 0

@app.route('/')
def index():
    global visits
    visits += 1
    return jsonify({
        "сервис": os.environ.get("APP_NAME", "Сайт"),
        "визитов": visits,
        "время": datetime.datetime.now().isoformat()
    })

# ✅ Правило: app.run() ВСЕГДА внутри if __name__ == "__main__"
# Иначе Flask запустится повторно при импорте модуля другим кодом
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
```

```bash
docker compose up -d
curl http://localhost:8080
docker compose logs -f web
```

---

## Урок 22 — Prometheus: собираем метрики

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-prometheus-grafana.jpg" alt="Prometheus + Grafana мониторинг" width="85%"/>
<br/><em>Prometheus — детектив: каждые 15 сек обходит сервисы и записывает числа. Grafana рисует красивые графики</em>
</div>

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

```yaml
# Добавить в docker-compose.yml:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - "8081:8080"

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    depends_on:
      - prometheus
```

```bash
docker compose up -d
open http://localhost:9090   # Prometheus
open http://localhost:3000   # Grafana (admin/admin)
# В Grafana: Add Data Source → Prometheus → http://prometheus:9090
# Import Dashboard ID: 193 (Docker metrics)
```

---

## Урок 23 — Шпаргалка Compose

| Команда | Действие |
|---------|---------|
| `docker compose up -d` | Запустить всё |
| `docker compose ps` | Статус сервисов |
| `docker compose logs -f` | Логи всех |
| `docker compose exec web bash` | Войти в сервис |
| `docker compose down` | Остановить |
| `docker compose up --scale web=3` | Масштабировать |

### Порты нашего стека

| Сервис | Порт |
|--------|------|
| Наш сайт | :8080 |
| cAdvisor | :8081 |
| Prometheus | :9090 |
| Grafana | :3000 |

➡️ [Следующий модуль: Kubernetes →](../module5-kubernetes/)
