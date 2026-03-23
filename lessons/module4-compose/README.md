# 🎼 Модуль 4 — Docker Compose + Мониторинг (Уроки 19–23)

> **Цель:** связать контейнеры вместе, собрать полный стек, наблюдать через Prometheus + Grafana.

---

## Урок 19 — Docker Compose: один файл — всё приложение

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-compose-network.jpg" alt="Docker Compose сеть сервисов" width="85%"/>
<br/><em>Compose — как многоквартирный дом: каждый сервис живёт отдельно, но соединён общей сетью</em>
</div>

### 🧠 Простое объяснение

> Настоящее приложение = несколько частей. Вместо трёх команд `docker run` — одна: `docker compose up`.

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
echo "DB_PASSWORD=МойСекрет123" > .env
echo ".env" >> .gitignore

docker compose up -d        # Запустить всё
docker compose ps           # Статус
docker compose logs -f      # Логи всех сервисов
docker compose exec web bash # Войти в сервис
docker compose down         # Остановить
docker compose down -v      # + удалить тома
```

---

## Урок 20 — Полный проект: код → контейнер → Compose

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

### Финальный docker-compose.yml с мониторингом

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
curl http://localhost:8080       # Наш сайт
# http://localhost:8081          # cAdvisor — метрики
```

---

## Урок 21 — Prometheus: собираем метрики

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-prometheus-grafana.jpg" alt="Prometheus и Grafana" width="85%"/>
<br/><em>Прометей — детектив: каждые 15 секунд обходит сервисы и записывает числа. Grafana рисует графики.</em>
</div>

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
```

```bash
docker compose up -d
# http://localhost:9090   → Prometheus
# http://localhost:3000   → Grafana (admin/admin)
```

### Настройка Grafana

1. Войти: admin / admin
2. Configuration → Data Sources → Add → Prometheus → URL: `http://prometheus:9090`
3. Dashboards → Import → ID `193` (готовый Docker-дашборд)
4. Готово! Графики CPU, RAM, сети для всех контейнеров

---

## Урок 22 — Масштабирование

```bash
# 3 экземпляра сайта!
docker compose up -d --scale web=3
docker compose ps
docker compose logs -f web
```

---

## 📋 Шпаргалка Модуля 4

| Команда | Что делает |
|---------|------------|
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
