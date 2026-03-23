# 🐳 Модуль 3 — Docker (Уроки 12–18)

> **Цель:** научиться создавать контейнеры, собирать образы и управлять ими.

---

## Урок 12 — Зачем нужен Docker?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-why-docker.jpg" alt="Зачем нужен Docker" width="85%"/>
<br/><em>Без Docker: «У меня работает!» — «У меня нет!». С Docker — работает везде одинаково.</em>
</div>

### 🧠 Простое объяснение

> Docker решает вечную проблему разработчиков: код работает на одном компьютере и ломается на другом. Docker упаковывает программу **вместе со всем нужным** в коробку-контейнер.

```bash
# Установить Docker (Ubuntu)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Проверить установку
docker --version
docker run hello-world
```

---

## Урок 13 — Образ и контейнер

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-image-vs-container.jpg" alt="Образ и контейнер" width="85%"/>
<br/><em>Образ = рецепт пирога (шаблон). Контейнер = готовый пирог (запущенная программа).</em>
</div>

### 🧠 Простое объяснение

> **Образ** (Image) — это рецепт. Нельзя изменить.  
> **Контейнер** (Container) — это пирог, испечённый по рецепту. Из одного рецепта — много пирогов.

```bash
docker pull nginx               # Скачать образ
docker images                   # Список образов
docker run -p 8080:80 nginx     # Запустить контейнер
docker ps                       # Запущенные контейнеры
docker ps -a                    # Все контейнеры
docker stop nginx               # Остановить
docker start nginx              # Запустить снова
docker rm nginx                 # Удалить контейнер
docker rmi nginx                # Удалить образ
```

### 🧪 Задание 13
```bash
# Запускаем реальный веб-сервер!
docker run -d --name мой-nginx -p 8080:80 nginx
docker ps

# Открываем в браузере: http://localhost:8080
curl http://localhost:8080

# Смотрим что внутри
docker exec -it мой-nginx bash
ls /usr/share/nginx/html/
exit

docker stop мой-nginx
docker rm мой-nginx
```

---

## Урок 14 — Dockerfile: рецепт образа

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-dockerfile-recipe.jpg" alt="Dockerfile — пошаговый рецепт" width="70%"/>
<br/><em>Dockerfile — пошаговый рецепт: берёшь основу, добавляешь ингредиенты, готово!</em>
</div>

### 🧠 Простое объяснение

> Dockerfile — это текстовый файл с инструкциями: «возьми такую-то основу, скопируй мой код, установи библиотеки, запусти».

### Создаём первый Dockerfile

```bash
mkdir ~/мой-сайт && cd ~/мой-сайт
```

**app.py** — наш сайт:
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, datetime, os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {
            "сообщение": "Привет из контейнера! 🐳",
            "время": datetime.datetime.now().isoformat(),
            "хост": os.environ.get("HOSTNAME", "неизвестно"),
            "версия": "1.0"
        }
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {fmt % args}")

print("Сервер запущен на порту 8080...")
HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
```

**Dockerfile**:
```dockerfile
# Шаг 1: Берём основу (Alpine = лёгкий Linux)
FROM python:3.11-slim

# Шаг 2: Переходим в рабочую папку
WORKDIR /app

# Шаг 3: Копируем наш код
COPY app.py .

# Шаг 4: Открываем порт
EXPOSE 8080

# Шаг 5: Команда запуска
CMD ["python", "app.py"]
```

```bash
# Собираем образ
docker build -t мой-сайт:v1.0 .

# Проверяем
docker images | grep мой-сайт

# Запускаем!
docker run -d --name мой-сайт -p 8080:8080 мой-сайт:v1.0
curl http://localhost:8080
```

**Ожидаемый результат:**
```json
{
  "сообщение": "Привет из контейнера! 🐳",
  "время": "2026-03-23T12:00:00",
  "хост": "a1b2c3d4e5f6",
  "версия": "1.0"
}
```

---

## Урок 15 — docker exec: войти внутрь

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-exec.jpg" alt="docker exec -it" width="85%"/>
<br/><em>docker exec -it — как шлюз подводной лодки: входишь внутрь работающего контейнера</em>
</div>

### 🧠 Простое объяснение

> Контейнер — как подводная лодка. Снаружи не видно что внутри. `docker exec -it` — это шлюз: входишь внутрь и смотришь.

```bash
# Войти в контейнер (интерактивный bash)
docker exec -it мой-сайт bash

# Внутри контейнера (командная строка изменится):
root@a1b2c3:/app# ls -la
root@a1b2c3:/app# cat app.py
root@a1b2c3:/app# ps aux
root@a1b2c3:/app# env
root@a1b2c3:/app# exit

# Выполнить команду не заходя внутрь
docker exec мой-сайт ls /app
docker exec мой-сайт cat /etc/os-release
docker exec мой-сайт ps aux

# Войти через sh (если bash нет)
docker exec -it мой-сайт sh
```

### 🧪 Задание 15
```bash
# Изучаем контейнер изнутри
docker exec -it мой-сайт bash

# Внутри выполнить:
pwd                    # Где мы?
ls -la                 # Что здесь?
cat app.py             # Наш код
python --version       # Версия Python
env | grep -i path     # Переменные окружения
exit                   # Выходим
```

---

## Урок 16 — docker logs: журнал событий

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-logs.jpg" alt="docker logs — журнал событий" width="85%"/>
<br/><em>Логи — это бортовой журнал контейнера: записывает всё что происходит внутри</em>
</div>

### 🧠 Простое объяснение

> Логи — это история всего, что произошло в контейнере. Как бортовой журнал корабля. Когда что-то сломалось — ты смотришь логи и понимаешь почему.

```bash
# Основные команды
docker logs мой-сайт            # Все логи
docker logs -f мой-сайт         # Следить в реальном времени (Ctrl+C — выход)
docker logs --tail 50 мой-сайт  # Последние 50 строк
docker logs --since 5m мой-сайт # Логи за последние 5 минут
docker logs -t мой-сайт         # С временными метками

# Для docker compose
docker compose logs              # Логи всех сервисов
docker compose logs -f           # Следить за всеми
docker compose logs -f web       # Следить за конкретным сервисом
docker compose logs --tail 100   # Последние 100 строк
```

### 🧪 Задание 16
```bash
# Создаём трафик и смотрим логи
for i in 1 2 3 4 5; do curl -s http://localhost:8080 > /dev/null; done

docker logs мой-сайт
docker logs --tail 3 мой-сайт
docker logs -t мой-сайт
```

**Ожидаемый результат логов:**
```
[12:00:01] "GET / HTTP/1.1" 200 -
[12:00:02] "GET / HTTP/1.1" 200 -
[12:00:03] "GET / HTTP/1.1" 200 -
```

---

## Урок 17 — docker system prune: уборка

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-prune.jpg" alt="docker system prune — уборка" width="85%"/>
<br/><em>prune — как уборка гаража: выбрасываем всё ненужное. Важно знать что именно удаляется!</em>
</div>

### 🧠 Простое объяснение

> Со временем Docker накапливает мусор: старые образы, остановленные контейнеры, неиспользуемые сети. `docker system prune` — это уборка.

```bash
# Смотрим сколько занимает Docker
docker system df

# Удалить всё неиспользуемое
docker system prune          # Контейнеры, сети, висячие образы
docker system prune -a       # + все неиспользуемые образы
docker system prune -f       # Без вопроса "Вы уверены?"

# Точечная очистка
docker container prune       # Только остановленные контейнеры
docker image prune           # Только висячие образы
docker image prune -a        # Все неиспользуемые образы
docker volume prune          # Тома (⚠️ УДАЛЯЕТ ДАННЫЕ!)
docker network prune         # Неиспользуемые сети
```

> ⚠️ **Важно:** `docker volume prune` удаляет тома с данными (базы данных и т.д.)! Будь осторожен.

### 🧪 Задание 17
```bash
# Проверяем объём
docker system df

# Создаём мусор для теста
docker pull alpine
docker run alpine echo "тест"    # Контейнер остановится
docker ps -a                     # Видим остановленный контейнер

# Убираем
docker system prune -f

# Проверяем результат
docker system df
```

---

## Урок 18 — Публикация образа на Docker Hub

```bash
# Логин в Docker Hub
docker login

# Тегируем образ (ваш-логин/имя-образа:версия)
docker tag мой-сайт:v1.0 ваш-логин/мой-сайт:v1.0

# Публикуем
docker push ваш-логин/мой-сайт:v1.0

# Теперь кто угодно может запустить:
docker run -p 8080:8080 ваш-логин/мой-сайт:v1.0
```

---

## 📋 Шпаргалка Модуля 3

| Команда | Что делает |
|---------|------------|
| `docker build -t имя .` | Собрать образ из Dockerfile |
| `docker run -d -p 8080:80 образ` | Запустить контейнер |
| `docker ps` | Запущенные контейнеры |
| `docker ps -a` | Все контейнеры |
| `docker logs -f имя` | Логи в реальном времени |
| `docker exec -it имя bash` | Войти в контейнер |
| `docker stop имя` | Остановить |
| `docker rm имя` | Удалить контейнер |
| `docker system prune -f` | Уборка без вопросов |
| `docker system df` | Сколько занимает Docker |

➡️ [Следующий модуль: Compose + Мониторинг →](../module4-compose/)
