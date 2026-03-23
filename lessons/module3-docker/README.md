# 🐳 Модуль 3 — Docker (Уроки 12–18)

> **Цель:** упаковать приложение в контейнер, научиться управлять им и понять зачем это нужно.

---

## Урок 12 — Зачем нужен Docker?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-why-docker.jpg" alt="Зачем нужен Docker" width="85%"/>
<br/><em>«У меня работает, у тебя нет» — классическая проблема. Docker решает её раз и навсегда</em>
</div>

### 🧠 Главная идея

> Представь, что ты испёк торт дома, а потом принёс его на вечеринку — но он рассыпался по дороге. Docker — это коробка, в которой торт **всегда** доедет целым.

```bash
# Установка Docker (Ubuntu)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Первый контейнер
docker run hello-world
docker run -it ubuntu bash          # Интерактивный Ubuntu!
docker run -d -p 8080:80 nginx      # Nginx в фоне
```

---

## Урок 13 — Образ vs Контейнер

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-image-vs-container.jpg" alt="Образ — рецепт, контейнер — блюдо" width="85%"/>
<br/><em>Образ = рецепт (неизменный). Контейнер = приготовленное блюдо. Из одного рецепта — сколько угодно блюд</em>
</div>

```bash
docker images                       # Список образов
docker ps                           # Запущенные контейнеры
docker ps -a                        # Все контейнеры (включая остановленные)

docker pull python:3.11-slim        # Скачать образ
docker run python:3.11-slim python --version

# Управление контейнерами
docker stop ИМЯ_ИЛИ_ID
docker start ИМЯ
docker restart ИМЯ
docker rm ИМЯ                       # Удалить (должен быть остановлен)
docker rm -f ИМЯ                    # Принудительно удалить
```

---

## Урок 14 — Dockerfile

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-dockerfile-recipe.jpg" alt="Dockerfile — пошаговый рецепт" width="85%"/>
<br/><em>Dockerfile — пошаговый рецепт: каждая строка добавляет новый слой к образу</em>
</div>

```dockerfile
# Dockerfile
FROM python:3.11-slim          # Базовый образ

WORKDIR /app                   # Рабочая папка внутри контейнера

COPY requirements.txt .        # Сначала зависимости (кэш!)
RUN pip install -r requirements.txt --no-cache-dir

COPY . .                       # Потом весь код

EXPOSE 8080                    # Документируем порт

ENV APP_NAME="Мой сайт"        # Переменная окружения

CMD ["python", "app.py"]       # Команда запуска
```

```bash
docker build -t мой-сайт .          # Собрать образ
docker build -t мой-сайт:v2.0 .     # С тегом версии
docker run -d -p 8080:8080 мой-сайт # Запустить
curl http://localhost:8080          # Проверить
```

---

## Урок 15 — docker exec: войти внутрь

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-exec.jpg" alt="docker exec — шлюз в контейнер" width="85%"/>
<br/><em>exec -it — как воздушный шлюз: входишь внутрь работающего контейнера не останавливая его</em>
</div>

```bash
# Войти в запущенный контейнер
docker exec -it МОЙ_КОНТЕЙНЕР bash
docker exec -it МОЙ_КОНТЕЙНЕР sh      # Если bash недоступен

# Внутри контейнера можно:
ls /app                        # Посмотреть файлы
cat /etc/os-release            # Какая ОС?
env                            # Переменные окружения
ps aux                         # Процессы
pip list                       # Установленные пакеты

# Выполнить одну команду без входа
docker exec МОЙ_КОНТЕЙНЕР python --version
docker exec МОЙ_КОНТЕЙНЕР cat /app/config.py

# Скопировать файл из/в контейнер
docker cp контейнер:/app/log.txt ./log.txt
docker cp ./config.py контейнер:/app/config.py
```

---

## Урок 16 — docker logs: читаем дневник

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-logs.jpg" alt="docker logs — дневник контейнера" width="85%"/>
<br/><em>Каждый контейнер ведёт дневник. Логи — это хроника всего что происходило внутри</em>
</div>

```bash
# Просмотр логов
docker logs МОЙ_КОНТЕЙНЕР              # Все логи
docker logs -f МОЙ_КОНТЕЙНЕР           # Следить в реальном времени (Ctrl+C — выход)
docker logs --tail 50 МОЙ_КОНТЕЙНЕР    # Последние 50 строк
docker logs --since 10m МОЙ_КОНТЕЙНЕР  # За последние 10 минут

# Docker Compose логи
docker compose logs                     # Все сервисы
docker compose logs -f web              # Только сервис web
docker compose logs -f --tail 100       # Последние 100 строк всех

# Зачем читать логи?
# ✅ Найти ошибку ("Error connecting to database")
# ✅ Проверить что сервис запустился ("Server started on :8080")
# ✅ Отследить запросы ("GET /api/users 200 OK")
# ✅ Понять почему упал контейнер
```

---

## Урок 17 — docker system prune: уборка

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-prune.jpg" alt="docker system prune — генеральная уборка" width="85%"/>
<br/><em>Со временем Docker накапливает гигабайты мусора. prune — генеральная уборка одной командой</em>
</div>

```bash
# Посмотреть что занимает место
docker system df
# TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
# Images          15        3         8.5GB     6.2GB (72%)
# Containers      8         2         150MB     140MB (93%)
# Build Cache     -         -         2.1GB     2.1GB

# Уборка
docker system prune             # Удалить остановленные контейнеры,
                                # неиспользуемые образы, сети, кэш
docker system prune -a          # Всё, включая образы без контейнеров
docker system prune -a --volumes # + тома с данными (ОСТОРОЖНО!)

# Точечная уборка
docker image prune              # Только образы без тегов
docker container prune          # Только остановленные контейнеры
docker volume prune             # Только тома

# ⚠️ НЕ удаляются:
# - Запущенные контейнеры
# - Образы используемых контейнеров
# - Тома (без --volumes)
```

---

## Урок 18 — Шпаргалка Docker

| Команда | Действие |
|---------|---------|
| `docker build -t имя .` | Собрать образ |
| `docker run -d -p 8080:8080 имя` | Запустить в фоне |
| `docker ps` | Запущенные контейнеры |
| `docker exec -it имя bash` | Войти внутрь |
| `docker logs -f имя` | Следить за логами |
| `docker stop имя` | Остановить |
| `docker system df` | Использование диска |
| `docker system prune` | Убраться |

➡️ [Следующий модуль: Docker Compose + Мониторинг →](../module4-compose/)
