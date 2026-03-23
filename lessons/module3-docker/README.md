# 🐳 Модуль 3 — Docker (Уроки 9–11)

> **Цель:** упаковывать приложения в контейнеры, писать Dockerfile, управлять образами.

---

## 📖 Урок 9 — Что такое Docker?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-why-docker.png" alt="Зачем нужен Docker" width="85%"/>
<br/><em>Docker решает вечную проблему: «у меня работает, у тебя нет!»</em>
</div>

### 🧠 Объяснение

> **Аналогия:** Docker — как отправить другу не рецепт торта, а уже **готовый торт в коробке**. Вскрыл — он уже готов, не надо ничего готовить!

### 🏗️ Архитектура Docker

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-architecture.png" alt="Архитектура Docker" width="80%"/>
<br/><em>Три слоя: ОС → Docker Engine → контейнеры (изолированы друг от друга)</em>
</div>

### 💻 Установка

```bash
sudo apt update && sudo apt install docker.io
sudo usermod -aG docker $USER
# Перезайди в систему, затем:
docker --version
docker run hello-world
```

---

## 📖 Урок 10 — Образы и контейнеры

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-image-vs-container.png" alt="Образ vs Контейнер" width="80%"/>
<br/><em>Образ = рецепт (статичный), Контейнер = работающее блюдо (живёт и дышит)</em>
</div>

### 💻 Управление контейнерами

```bash
docker images                       # Список образов
docker pull nginx                   # Скачать образ
docker run -d -p 8080:80 nginx      # Запустить в фоне
docker run -it ubuntu bash          # Войти внутрь

docker ps                           # Запущенные
docker ps -a                        # Все

docker stop мой-сервер
docker start мой-сервер
docker rm мой-сервер
docker logs -f мой-сервер          # Следить за логами
docker exec -it мой-сервер bash    # Терминал внутри
docker stats                        # Нагрузка
```

### 🧪 Задание 10

```bash
docker run -d -p 8080:80 --name тест nginx
docker ps
curl http://localhost:8080
docker logs тест
docker stop тест && docker rm тест
```

---

## 📖 Урок 11 — Пишем Dockerfile

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-dockerfile-recipe.png" alt="Dockerfile как рецепт" width="80%"/>
<br/><em>Dockerfile — пошаговый рецепт: FROM (основа) → RUN (готовим) → COPY → CMD (подаём)</em>
</div>

### 💻 Структура Dockerfile

```dockerfile
FROM python:3.11-slim    # Базовый образ
WORKDIR /app             # Рабочая папка
COPY app.py .            # Скопировать файл
RUN pip install flask    # Установить зависимости
EXPOSE 5000              # Документировать порт
CMD ["python3", "app.py"] # Запустить при старте
```

### 💻 Практика: Python-сайт в Docker

```python
# app.py
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<h1>Привет из Docker! 🐳</h1>")
    def log_message(self, *args): pass

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
```

```bash
docker build -t мой-сайт:v1 .
docker run -d -p 8080:8080 --name сервер мой-сайт:v1
curl http://localhost:8080
```

### 💻 Публикация на Docker Hub

```bash
docker login
docker build -t ТВОЁ_ИМЯ/мой-сайт:v1 .
docker push ТВОЁ_ИМЯ/мой-сайт:v1
```

### 🚀 Путь от кода до сервера

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-deployment-path.png" alt="Путь от кода до сервера" width="85%"/>
<br/><em>5 шагов: написал → Dockerfile → образ → Docker Hub → сервер запустил</em>
</div>

### 🧪 Задание 11

```bash
mkdir урок11 && cd урок11
cat > Dockerfile << 'EOF'
FROM alpine
CMD echo "🐳 Контейнер запущен!"
EOF
docker build -t мой-первый .
docker run --rm мой-первый
```

---

## 📋 Шпаргалка Модуля 3

| Команда | Что делает |
|---------|-----------|
| `docker images` | Образы |
| `docker pull имя` | Скачать |
| `docker build -t имя .` | Собрать |
| `docker push имя` | Отправить |
| `docker run -d -p 8080:80 имя` | Запустить |
| `docker ps / ps -a` | Контейнеры |
| `docker logs -f имя` | Логи |
| `docker exec -it имя bash` | Войти |
| `docker stop/rm имя` | Остановить/Удалить |
| `docker system prune` | Очистить |

➡️ [Следующий модуль: Docker Compose →](../module4-compose/)
