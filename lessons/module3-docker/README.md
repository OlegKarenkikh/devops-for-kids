# 🐳 Модуль 3 — Docker (Уроки 9–11)

> **Цель:** научиться упаковывать приложения в контейнеры, писать Dockerfile и управлять образами.

---

## 📖 Урок 9 — Что такое Docker?

### 🧠 Объяснение

Docker решает главную проблему: «У меня работает, а у тебя нет». Ты упаковываешь программу со ВСЕМ нужным в один контейнер — и она работает везде одинаково.

> **Аналогия:** Docker — это как отправить другу не рецепт торта, а уже готовый торт в коробке. Вскрыл — и он уже готов!

### 💻 Установка

```bash
sudo apt update && sudo apt install docker.io
sudo usermod -aG docker $USER
# Перезайди в систему, затем:
docker --version
docker run hello-world
```

### 💻 Первые команды

```bash
docker images            # Список скачанных образов
docker ps                # Запущенные контейнеры
docker ps -a             # Все контейнеры
docker pull ubuntu       # Скачать образ Ubuntu
docker run -it ubuntu bash  # Войти внутрь контейнера
```

### 🧪 Задание

```bash
docker pull nginx
docker images
docker run -d -p 8080:80 --name тест nginx
docker ps
curl http://localhost:8080
docker stop тест && docker rm тест
```

---

## 📖 Урок 10 — Управление контейнерами

### 💻 Жизненный цикл контейнера

```bash
docker run -d --name мой-сервер nginx   # Запустить в фоне
docker stop мой-сервер                  # Остановить
docker start мой-сервер                 # Запустить снова
docker restart мой-сервер              # Перезапустить
docker rm мой-сервер                   # Удалить

docker logs мой-сервер                 # Логи контейнера
docker logs -f мой-сервер              # Следить за логами
docker exec -it мой-сервер bash        # Войти внутрь
docker stats                           # Потребление ресурсов
docker inspect мой-сервер             # Полная информация
```

### 💻 Тома (Volumes) — сохраняем данные

```bash
# Данные внутри контейнера исчезают при его удалении!
# Volume сохраняет данные на хосте:
docker run -d -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html \
  --name мой-сайт nginx
```

### 🧪 Задание

```bash
mkdir html
echo "<h1>Привет из Docker!</h1>" > html/index.html
docker run -d -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html \
  --name мой-сайт nginx
curl http://localhost:8080
# Открой браузер: http://localhost:8080
```

---

## 📖 Урок 11 — Пишем Dockerfile

### 🧠 Объяснение

Dockerfile — пошаговый рецепт сборки образа. Каждая строка — один шаг.

### 💻 Структура Dockerfile

```dockerfile
FROM python:3.11-slim      # Базовый образ (основа)
LABEL maintainer="Ваня"   # Метаданные
WORKDIR /app               # Рабочая папка
COPY app.py .              # Скопировать файл
RUN pip install flask      # Выполнить команду при сборке
EXPOSE 5000                # Документировать порт
ENV APP_NAME=МойСайт       # Переменная окружения
CMD ["python3", "app.py"]  # Команда при запуске
```

### 💻 Практика: Python-сервер в Docker

**app.py:**
```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<h1>Привет из Docker! 🐳</h1>")
    def log_message(self, *args):
        pass

print("Сервер: http://localhost:8080")
HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
EXPOSE 8080
CMD ["python3", "app.py"]
```

```bash
docker build -t мой-сайт:v1 .
docker run -d -p 8080:8080 --name мой-сервер мой-сайт:v1
curl http://localhost:8080
docker images
docker history мой-сайт:v1
```

### 🧪 Задание

```bash
mkdir урок11 && cd урок11
cat > Dockerfile << 'EOF'
FROM alpine
RUN echo "Привет при сборке!"
CMD echo "Контейнер запущен! 🎉"
EOF
docker build -t мой-alpine .
docker run --rm мой-alpine
```

---

## 📋 Шпаргалка Модуля 3

| Команда | Что делает |
|---------|-----------|
| `docker images` | Список образов |
| `docker pull имя` | Скачать образ |
| `docker run -d -p 8080:80 имя` | Запустить с портом |
| `docker ps` | Запущенные контейнеры |
| `docker stop имя` | Остановить |
| `docker rm имя` | Удалить контейнер |
| `docker logs имя` | Логи |
| `docker exec -it имя bash` | Войти внутрь |
| `docker build -t имя .` | Собрать образ |
| `docker push имя` | Отправить в реестр |
| `docker system prune` | Очистить всё лишнее |
