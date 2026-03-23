# 🐳 Модуль 3 — Docker (Уроки 9–15)

> **Цель:** написать код → упаковать в контейнер → запустить → отлаживать → подключить к другим сервисам.

---

## Урок 9 — Зачем Docker?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-why-docker.jpg" alt="Зачем Docker" width="85%"/>
<br/><em>«У меня работает, у тебя нет!» — Docker решает эту проблему навсегда</em>
</div>

```bash
sudo apt update && sudo apt install docker.io
sudo usermod -aG docker $USER
# Перезайди, затем:
docker --version
docker run hello-world
```

---

## Урок 10 — Образы и контейнеры

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-image-vs-container.jpg" alt="Образ vs Контейнер" width="80%"/>
<br/><em>Образ = замороженный рецепт. Контейнер = живое работающее блюдо</em>
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-architecture.jpg" alt="Архитектура Docker" width="80%"/>
<br/><em>Docker Engine изолирует каждый контейнер, но все используют одно ядро Linux</em>
</div>

```bash
docker images              # Список образов
docker pull nginx          # Скачать образ
docker run -d -p 8080:80 --name веб nginx
docker ps                  # Запущенные
docker ps -a               # Все
docker stop веб && docker rm веб
docker rmi nginx           # Удалить образ
```

---

## Урок 11 — Пишем первый Dockerfile

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-dockerfile-recipe.jpg" alt="Dockerfile — рецепт" width="80%"/>
<br/><em>FROM = основа, RUN = готовим, COPY = кладём, CMD = запускаем</em>
</div>

```dockerfile
FROM python:3.11-slim
WORKDIR /app
# Сначала зависимости — кешируются
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Потом код
COPY . .
EXPOSE 8080
CMD ["python3", "app.py"]
```

---

## Урок 12 — Пишем код и запускаем в контейнере

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module4-code-to-compose.jpg" alt="От кода до Compose" width="85%"/>
<br/><em>5 шагов: написал → Dockerfile → build → run → compose up</em>
</div>

### Шаг 1: Код приложения

```python
# app.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, datetime, os

VISITS = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global VISITS
        VISITS += 1
        name = os.environ.get("APP_NAME", "Мой сайт")
        data = {
            "сайт": name,
            "визиты": VISITS,
            "время": datetime.datetime.now().isoformat()
        }
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {fmt % args}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Сервер запущен на порту {port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
```

### Шаг 2: Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
EXPOSE 8080
ENV APP_NAME="Мой первый Docker-сайт"
CMD ["python3", "app.py"]
```

### Шаг 3: Собрать и запустить

```bash
docker build -t мой-сайт:v1 .
docker run -d -p 8080:8080 --name сайт мой-сайт:v1
curl http://localhost:8080
# {"сайт": "Мой первый Docker-сайт", "визиты": 1}
```

---

## Урок 13 — docker exec: работаем внутри контейнера

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-exec.jpg" alt="docker exec — войти в контейнер" width="80%"/>
<br/><em>Контейнер — подводная лодка. docker exec — воздушный шлюз: входишь не останавливая</em>
</div>

```bash
# Открыть терминал внутри контейнера
docker exec -it сайт bash       # bash (Ubuntu/Debian)
docker exec -it сайт sh         # sh (Alpine)

# Выполнить команду без входа
docker exec сайт ls /app
docker exec сайт env            # Переменные окружения
docker exec сайт ps aux         # Процессы

# Войти в базу данных
docker exec -it postgres-db psql -U postgres
docker exec -it redis-cache redis-cli

# Диагностика
docker exec сайт df -h          # Диск
docker exec сайт free -h        # Память
```

| Флаг | Смысл | Когда |
|------|-------|-------|
| `-i` | Интерактивный ввод | Когда надо вводить текст |
| `-t` | Эмуляция терминала | Для красивого вывода |
| `-it` | Оба | Интерактивная работа |
| _(без флагов)_ | Одна команда | Скрипты, проверки |

---

## Урок 14 — Логи контейнера

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-logs.jpg" alt="docker logs — дневник контейнера" width="80%"/>
<br/><em>Логи — корабельный журнал: каждое событие записывается с меткой времени</em>
</div>

```bash
# Читать логи
docker logs сайт                  # Все логи
docker logs -f сайт               # Следить в реальном времени
docker logs --tail 50 сайт        # Последние 50 строк
docker logs --since 1h сайт       # За последний час

# Docker Compose — все сервисы сразу
docker compose logs -f            # Следить за всеми
docker compose logs -f web        # Только один сервис
docker compose logs --tail 100    # Последние 100 строк
```

> 📌 **Зачем?** Логи — главный инструмент диагностики. Когда что-то сломалось — смотри логи!

---

## Урок 15 — Уборка: docker system prune

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-prune.jpg" alt="docker system prune — уборка" width="80%"/>
<br/><em>Старые контейнеры и образы занимают гигабайты. Prune — генеральная уборка</em>
</div>

```bash
docker system df               # Сколько места занято

docker container prune         # Удалить остановленные контейнеры
docker image prune -a          # Удалить неиспользуемые образы
docker volume prune            # Удалить пустые тома
docker builder prune           # Очистить кеш сборки

docker system prune            # Всё сразу (безопасно)
docker system prune -a         # Агрессивно (все неиспользуемые образы)
docker system prune -af        # Без вопросов
```

| Команда | Что удаляет | Влияние |
|---------|------------|---------|
| `prune` | Остановленные контейнеры | Освобождает место |
| `prune -a` | + все неиспользуемые образы | Намного больше места |
| `prune -af --volumes` | + тома с данными | ⚠️ Удаляет данные! |

---

## 📋 Шпаргалка Модуля 3

| Команда | Что делает |
|---------|-----------|
| `docker build -t имя:тег .` | Собрать образ |
| `docker run -d -p 8080:80 имя` | Запустить в фоне |
| `docker exec -it имя bash` | Войти внутрь |
| `docker logs -f имя` | Следить за логами |
| `docker system df` | Место на диске |
| `docker system prune` | Очистить неиспользуемое |
| `docker stats` | Нагрузка в реальном времени |

➡️ [Следующий модуль: Docker Compose →](../module4-compose/)
