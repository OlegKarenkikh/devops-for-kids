# 🎼 Модуль 4 — Docker Compose + Мониторинг (Уроки 19–23)

> **Цель:** запускать несколько сервисов одной командой и наблюдать за ними через Prometheus + Grafana.

> 💡 **Вопросы по Compose?** Зачем несколько сетей? Что такое том? Как работает depends_on?  
> → [Ответы в Детском FAQ](../kids-faq/#модуль-4--compose)

---

## Урок 19 — Docker Compose: город сервисов


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-compose-overview.jpg" alt="Docker Compose" width="90%"/>
<br/><em>Docker Compose: запускаем несколько сервисов одним файлом одной командой</em>
</div>


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-code-to-compose-ru.jpg" alt="Перевод docker run команд в docker-compose.yml" width="90%"/>
<br/><em>Перевод docker run команд в docker-compose.yml — наглядное сравнение</em>
</div>


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-compose-network.jpg" alt="Docker Compose — город сервисов" width="85%"/>
<br/><em>Compose = целый город из сервисов. Один файл — один запуск. Все сервисы видят друг друга по имени</em>
</div>

### 🧠 Теория: зачем нужен Compose?


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-code-to-compose.jpg" alt="От разрозненных docker run" width="90%"/>
<br/><em>От разрозненных docker run — к единому docker-compose.yml</em>
</div>


Представь, что ты делаешь интернет-магазин. Ему нужны три части:
- **Сайт** — показывает страницы пользователю
- **База данных** — хранит товары и заказы
- **Кэш** — запоминает часто запрашиваемые данные, чтобы не лезть в базу каждый раз

Запускать каждый контейнер отдельно вручную — это как каждый раз перед поездкой вручную накачивать все 4 колеса по одному. Compose запускает все три одной командой `docker compose up`.

Главный файл Compose — `docker-compose.yml`. В нём описаны все сервисы, их настройки, связи между ними.

```yaml
# docker-compose.yml
# version: не нужна в Compose v2+ (Docker Desktop 4.x и новее)
services:
  web:
    build: .                        # Собрать из Dockerfile в текущей папке
    ports:
      - "8080:8080"                 # Открыть порт: хост:контейнер
    depends_on:
      db:
        condition: service_healthy  # Ждать, пока db не станет healthy
    restart: unless-stopped         # Автоперезапуск при падении

  db:
    image: postgres:15-alpine       # Готовый образ из Docker Hub
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}   # Берём из .env
    volumes:
      - pgdata:/var/lib/postgresql/data   # Сохраняем данные БД
    healthcheck:                    # Проверка готовности
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      retries: 5

  cache:
    image: redis:7-alpine

volumes:
  pgdata:                           # Именованный том для БД
bash
echo "DB_PASSWORD=Секрет123" > .env
docker compose up -d        # Запустить всё (-d = в фоне)
docker compose ps           # Статус всех сервисов
docker compose logs -f      # Логи всех (Ctrl+C — выход)
docker compose down         # Остановить и удалить контейнеры
docker compose down -v      # + удалить тома (данные БД пропадут!)

---

## Урок 20 — Networks: как сервисы общаются


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-compose-networks-ru.jpg" alt="Сети в Compose" width="85%"/>
<br/><em>Сети в Compose: фронтенд видит только бэкенд, бэкенд — только базу</em>
</div>



<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-compose-networks-segmentation.jpg" alt="Сегментация сети Compose" width="90%"/>
<br/><em>Сегментация сети Compose: изоляция сервисов для безопасности</em>
</div>


### 🧠 Теория: зачем изолировать сервисы?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/kid_ports.jpg" alt="Порты: как номера квартир в доме" width="80%"/>
<br/><em>Порт — как номер квартиры: один дом (IP), разные квартиры (порты) для разных жильцов (сервисов)</em>
</div>



По умолчанию все сервисы в одном Compose-файле видят друг друга — это удобно, но небезопасно. Если взломают frontend — злоумышленник через него может добраться до базы данных напрямую. Сетевая сегментация решает это: **каждый сервис видит только тех соседей, с кем должен общаться**.

Правило: **база данных никогда не должна быть доступна напрямую из интернета** — только через backend.


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-compose-networks.jpg" alt="Docker Networks" width="90%"/>
<br/><em>База данных защищена — Frontend не видит её напрямую!</em>
</div>
### 🧠 Теория: почему сервис может «не видеть» другой?


По умолчанию Compose создаёт одну сеть для всех сервисов в файле. Внутри этой сети сервисы обращаются друг к другу **по именам** (не по IP). Например, сайт обращается к базе данных просто как `db:5432` — не надо знать никакой IP-адрес.

Но иногда нужно **разделить** сервисы: например, база данных не должна быть доступна снаружи, только для бэкенда. Для этого используют несколько сетей.

yaml
# docker-compose.yml с явными сетями
# version: не нужна в Compose v2+ (Docker Desktop 4.x и новее)
services:
  frontend:
    image: nginx:latest
    networks:
      - public-net           # Видна снаружи
    ports:
      - "80:80"

  backend:
    build: .
    networks:
      - public-net           # Принимает запросы от frontend
      - private-net          # Ходит в БД

  db:
    image: postgres:15-alpine
    networks:
      - private-net          # Только для backend — снаружи недоступна!
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}

networks:
  public-net:                # Публичная сеть (frontend + backend)
  private-net:               # Приватная сеть (backend + db)

**Что это даёт:**
- Frontend не может напрямую обратиться к базе — только через backend
- База защищена от случайного доступа
- Это называется «сетевая сегментация» — важная практика безопасности

bash
# Посмотреть сети
docker network ls
docker network inspect my-project_private-net

# Проверить, что backend видит db (зайди в backend и пропингуй)
docker compose exec backend ping db

### ⚠️ Типичная ошибка: сервис не может подключиться к базе

text
sqlalchemy.exc.OperationalError: could not connect to server: Connection refused
    Is the server running on host "localhost"?

**Причина:** в коде написано `localhost` вместо имени сервиса из Compose.
**Решение:** внутри Docker Compose обращайся по имени сервиса:
python
# ❌ Неправильно:
DATABASE_URL = "postgresql://user:pass@localhost:5432/mydb"

# ✅ Правильно (имя сервиса из docker-compose.yml):
DATABASE_URL = "postgresql://user:pass@db:5432/mydb"

---

## Урок 21 — Полный проект: код → контейнер → Compose

python
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
bash
docker compose up -d
curl http://localhost:8080
docker compose logs -f web

---

## Урок 22 — Prometheus: собираем метрики


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-monitoring.jpg" alt="Мониторинг стека" width="90%"/>
<br/><em>Мониторинг стека: Prometheus собирает метрики, Grafana строит дашборды</em>
</div>


<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-prometheus.jpg" alt="Prometheus и Grafana" width="90%"/>
  <br/><em>📊 Рис. 6 — Поток метрик: контейнеры → Prometheus → Grafana</em>
</div>


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-prometheus-grafana.jpg" alt="Prometheus + Grafana мониторинг" width="85%"/>
<br/><em>Prometheus — детектив: каждые 15 сек обходит сервисы и записывает числа. Grafana рисует красивые графики</em>
</div>

### 🧠 Теория: что такое метрика?


**Метрика** — это число, которое что-то измеряет в реальном времени. Например:
- `cpu_usage = 87%` — процессор загружен на 87%
- `http_requests_total = 12430` — за всё время пришло 12430 запросов
- `memory_bytes = 256000000` — используется 256 МБ памяти

Метрики собираются автоматически каждые несколько секунд и записываются в базу данных временных рядов. Потом их можно визуализировать как график: ось X — время, ось Y — значение.

### 🧠 Теория: зачем нужен мониторинг?

Представь: сайт стал работать медленно. Пользователи жалуются, но ты не знаешь — в чём причина. Закончилась память? Перегружен CPU? Слишком много запросов к базе?

**Prometheus** каждые несколько секунд опрашивает твои сервисы и записывает числа: сколько памяти используется, сколько запросов в секунду, сколько ошибок. **Grafana** превращает эти числа в красивые графики — ты видишь картину в реальном времени.

yaml
# prometheus.yml
global:
  scrape_interval: 15s            # Опрашивать каждые 15 секунд
scrape_configs:
  - job_name: 'cadvisor'          # cAdvisor собирает метрики Docker
    static_configs:
      - targets: ['cadvisor:8080']
yaml
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
bash
docker compose up -d
# Открыть Prometheus:
curl http://localhost:9090
# Открыть Grafana (admin/admin):
curl http://localhost:3000
# В Grafana: Add Data Source → Prometheus → http://prometheus:9090
# Import Dashboard ID: 193 (Docker metrics)

---


---

## 🎯 Практические задания

### Задание 1 — Стек одной командой
bash
mkdir compose-test && cd compose-test

cat > docker-compose.yml << 'EOF'
# version: не нужна в Compose v2+ (Docker Desktop 4.x и новее)
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: testdb
EOF

docker compose up -d
docker compose ps      # оба Running?
docker compose down
> ✅ Два сервиса запустились одной командой!

### Задание 2 — Переменные окружения
bash
cat > .env << 'EOF'
DB_PASSWORD=supersecret
WEB_PORT=9090
EOF
# Используй ${DB_PASSWORD} и ${WEB_PORT} в docker-compose.yml
docker compose up -d

## Урок 23 — Шпаргалка Compose

### 🧠 Теория: почему важно знать эти команды наизусть?

В реальной работе DevOps-инженер десятки раз в день смотрит статус сервисов, читает логи, перезапускает контейнеры. Эти команды — как велосипед: сначала учишь, потом работают автоматически. Шпаргалка ниже — не для зазубривания, а для того чтобы видеть всю картину сразу.

| Команда | Действие |
|---------|---------|
| `docker compose up -d` | Запустить всё |
| `docker compose ps` | Статус сервисов |
| `docker compose logs -f` | Логи всех |
| `docker compose exec web bash` | Войти в сервис |
| `docker compose down` | Остановить |
| `docker compose up --scale web=3` | Масштабировать |
| `docker compose restart web` | Перезапустить один сервис |

### Порты нашего стека

| Сервис | Порт |
|--------|------|
| Наш сайт | :8080 |
| cAdvisor | :8081 |
| Prometheus | :9090 |
| Grafana | :3000 |

### Концепции Networks

| Концепция | Смысл |
|-----------|-------|
| Сеть по умолчанию | Все сервисы Compose видят друг друга |
| Обращение по имени | `db:5432`, не `localhost:5432` |
| Несколько сетей | Разделение: frontend/backend/db |
| `docker network ls` | Список всех сетей |


---

### Задание 3 — Мониторинг в действии
bash
# Запусти стек с Prometheus:
docker compose up -d
# Открой в браузере: http://localhost:9090
# Найди метрику: container_cpu_usage_seconds_total
# Запрос PromQL: rate(container_cpu_usage_seconds_total[5m])
```
> ✅ Grafana показала график CPU? Мониторинг работает!

---

## 🧩 Быстрый тест — проверь себя

| Вопрос | Ответ |
|--------|-------|
| Как обратиться к сервису `db` из `backend` внутри Compose? | `db:5432` (не localhost!) |
| Что делает `depends_on: db: condition: service_healthy`? | Ждёт, пока db не пройдёт healthcheck |
| Чем том (`volume`) отличается от `tmpfs`? | Том сохраняется на диск, tmpfs — в RAM (исчезает) |
| Что такое cAdvisor? | Агент, который собирает метрики Docker в Prometheus |
| Что делает `docker compose down -v`? | Удаляет контейнеры И тома (данные пропадают!) |

## 🧠 Чекпойнт понимания — обязательный

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/checkpoint.jpg" alt="Чекпойнт понимания" width="90%"/>
<br/><em>Три вопроса после каждого урока. Понимание важнее скорости.</em>
</div>

Прежде чем перейти к Модулю 5 — ответь себе вслух или письменно:

**1. Зачем нужен Docker Compose если можно запускать контейнеры по одному через `docker run`?**

**2. Как контейнеры общаются друг с другом внутри одной Compose-сети? Что является адресом?**

**3. Что такое Prometheus и Grafana? Объясни разницу: один собирает, другой...**

**4. В чём разница между `depends_on` и реальной готовностью сервиса?**

> 💡 Если не можешь ответить на вопрос — вернись к соответствующему уроку. Понимание важнее скорости!

➡️ [Следующий модуль: Kubernetes →](../module5-kubernetes/)
