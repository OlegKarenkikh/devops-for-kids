# 🐳 Модуль 3 — Docker (Уроки 12–18)

> **Цель:** упаковать приложение в контейнер, научиться управлять им и понять зачем это нужно.

---

> 💡 **Image vs Container? Порт 8080:8080? Зачем Volume?**  
> → [Ответы в Детском FAQ](../kids-faq/#модуль-3--docker)


## Урок 12 — Зачем нужен Docker?

![module3-docker-architecture](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-architecture.png)


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-why-docker.jpg" alt="Зачем нужен Docker" width="85%"/>
<br/><em>«У меня работает, у тебя нет» — классическая проблема. Docker решает её раз и навсегда</em>
</div>

### 🧠 Теория: что такое Docker и зачем он нужен?

Представь: ты написал игру на своём компьютере, она работает. Ты отправил её другу — у него ничего не запускается. Он говорит: «Нет нужной библиотеки». Ты добавляешь библиотеку, он снова запускает — теперь «не та версия Python». Это продолжается часами.

**Docker решает эту проблему раз и навсегда.** Он упаковывает приложение вместе со всем, что ему нужно: кодом, библиотеками, настройками — в один «контейнер». Этот контейнер запустится одинаково на любом компьютере, сервере или в облаке.

> 🍱 Аналогия: Docker — это ланч-бокс. Ты кладёшь в него еду дома, и она приезжает в офис точно такой же. Никакого «ой, я забыл соль» — всё уже внутри.

### Разница: контейнер vs виртуальная машина

| | Виртуальная машина | Docker контейнер |
|---|---|---|
| Размер | 10–50 GB | 50–500 MB |
| Запуск | 1–3 минуты | 1–3 секунды |
| ОС внутри | Полная (своё ядро) | Общее ядро хоста |
| Изоляция | Полная | Почти полная |
| Использование | Когда нужна другая ОС | Для приложений |

### Практика

```bash
# Шаг 1: Установка Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker                       # Применить группу без перезагрузки

# Шаг 2: Проверка установки
docker --version                    # Должно показать версию
docker run hello-world              # Тест: скачает и запустит тестовый образ
```


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-errors.jpg" alt="Частые ошибки Docker" width="90%"/>
<br/><em>Три самые частые ошибки и как их исправить</em>
</div>

### ⚠️ Частая ошибка: permission denied

```
docker: Got permission denied while trying to connect to the Docker daemon socket
```

**Причина:** пользователь не в группе `docker`.
**Решение:**
```bash
sudo usermod -aG docker $USER
newgrp docker
# Если не помогло — полностью выйди и войди заново (logout/login)
```

---

## Урок 13 — Образ vs Контейнер

![module3-image-vs-container](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-image-vs-container.png)


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-image-vs-container.jpg" alt="Образ — рецепт, контейнер — блюдо" width="85%"/>
<br/><em>Образ = рецепт (неизменный). Контейнер = приготовленное блюдо. Из одного рецепта — сколько угодно блюд</em>
</div>

### 🧠 Теория: в чём разница?

**Образ (Image)** — это шаблон, «снимок» системы: файлы, библиотеки, настройки. Он неизменный. Как рецепт: сколько раз ни читай — рецепт не меняется.

**Контейнер (Container)** — это запущенный образ. Живой процесс. Он может изменяться во время работы, но эти изменения не сохраняются в образе. Как готовое блюдо: его едят и оно исчезает.

Один и тот же образ можно запустить 100 раз — получишь 100 независимых контейнеров. Они не знают друг о друге.

```bash
# Работа с образами
docker images                       # Список образов на твоём компьютере
docker pull python:3.11-slim        # Скачать образ из Docker Hub
docker rmi python:3.11-slim         # Удалить образ

# Работа с контейнерами
docker ps                           # Только запущенные контейнеры
docker ps -a                        # Все: запущенные + остановленные

# Запуск и управление
docker run -d -p 8080:80 nginx      # -d: в фоне, -p: пробрасываем порт хост:контейнер
docker stop НАЗВАНИЕ_ИЛИ_ID         # Мягкая остановка (SIGTERM, даёт 10 сек)
docker kill НАЗВАНИЕ                # Принудительная остановка (SIGKILL)
docker start НАЗВАНИЕ               # Запустить остановленный
docker rm НАЗВАНИЕ                  # Удалить (контейнер должен быть остановлен)
docker rm -f НАЗВАНИЕ               # Остановить и удалить сразу
```

### ⚠️ Почему данные исчезают при удалении контейнера?

Контейнер — как блокнот из блокнота. Пока он работает — ты пишешь. Удалил контейнер — блокнот выброшен вместе с записями. Для сохранения данных нужны **тома (volumes)** — об этом в уроке 17.

---

## Урок 14 — Dockerfile: пишем свой рецепт

![module3-dockerfile-layers](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-dockerfile-layers.png)


<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-layers.jpg" alt="Слои Docker образа" width="90%"/>
  <br/><em>🐳 Рис. 5 — Dockerfile → слои образа → кеширование: что меняется — то пересобирается</em>
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-dockerfile-recipe.jpg" alt="Dockerfile — пошаговый рецепт" width="85%"/>
<br/><em>Dockerfile — пошаговый рецепт: каждая строка добавляет новый слой к образу</em>
</div>

### 🧠 Теория: как читать Dockerfile?

Dockerfile — это текстовый файл с инструкциями. Docker читает его сверху вниз и строит образ слоями. Каждая инструкция = новый слой. Слои кэшируются — если строка не изменилась, Docker не перезапускает её.

**Поэтому важен порядок:** сначала то, что меняется редко (зависимости), потом то, что меняется часто (код).

```dockerfile
# Dockerfile

# FROM — с чего начинаем. python:3.11-slim = Python 3.11 на минимальном Linux
FROM python:3.11-slim

# WORKDIR — создаёт папку и делает её текущей. Все следующие команды выполняются тут
WORKDIR /app

# COPY — сначала копируем только зависимости (список библиотек)
# Зачем отдельно? Если код изменился, а requirements.txt — нет,
# Docker возьмёт слой с pip install из кэша и не будет устанавливать заново
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Теперь копируем весь остальной код
> ### ⚠️ Обязательно создай файл `.dockerignore`!
>
> `COPY . .` копирует **всё** из папки — включая `.env` с паролями и секретами!
> Создай файл `.dockerignore` рядом с `Dockerfile`:
>
> ```
> .env
> .git
> .gitignore
> __pycache__
> *.pyc
> node_modules
> *.log
> ```
>
> **Без этого файла твои пароли окажутся внутри образа** — и если кто-то скачает образ с Docker Hub, он получит все твои секреты!

COPY . .

# EXPOSE — документирует, какой порт слушает приложение
# Это НЕ открывает порт автоматически — нужен ещё -p при docker run
EXPOSE 8080

# ENV — задаём переменную окружения
ENV APP_NAME="Мой сайт"

# CMD — команда запуска контейнера. Выполняется, когда контейнер стартует
CMD ["python", "app.py"]
```

```bash
docker build -t my-site .           # Собрать образ (. = текущая папка)
docker build -t my-site:v2.0 .      # С тегом версии
docker run -d -p 8080:8080 my-site  # Запустить
curl http://localhost:8080          # Проверить
```

### CMD vs ENTRYPOINT — в чём разница?

| | CMD | ENTRYPOINT |
|---|---|---|
| Что делает | Команда по умолчанию | Основная команда, не заменяется |
| Можно переопределить? | Да (`docker run my-app python other.py`) | Нет (только аргументы) |
| Когда использовать | Для гибких команд | Для строгих исполняемых файлов |

```dockerfile
# Рекомендуется комбинировать:
ENTRYPOINT ["python"]   # основное — всегда python
CMD ["app.py"]          # аргумент по умолчанию
# docker run my-app              → python app.py
# docker run my-app other.py     → python other.py
```


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-dockerfile-layers.jpg" alt="Dockerfile порядок слоёв" width="90%"/>
<br/><em>Меняется редко — наверх. Меняется часто — вниз. Кэш экономит минуты сборки!</em>
</div>

### ⚠️ Частые ошибки при сборке

**Ошибка: COPY failed — file not found**
```
COPY failed: file not found in build context: requirements.txt
```
**Причина:** файл `requirements.txt` не существует или ты запускаешь `docker build` из другой папки.
**Решение:** убедись что ты в папке с Dockerfile и файл существует:
```bash
ls requirements.txt   # Должен показать файл
docker build -t my-site .
```

**Ошибка: permission denied в контейнере**
```
PermissionError: [Errno 13] Permission denied: '/app/data'
```
**Причина:** в Dockerfile создана папка, но у пользователя нет прав на запись.
**Решение:**
```dockerfile
RUN mkdir -p /app/data && chmod 755 /app/data
# Или создай непривилегированного пользователя:
RUN useradd -m appuser && chown -R appuser /app
USER appuser
```

---

## Урок 15 — docker exec: войти внутрь контейнера

![module3-docker-exec](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-exec.png)


### 🧠 Теория: зачем заходить внутрь?

Иногда приложение ведёт себя странно: логи не помогают, нужно посмотреть своими глазами — что внутри контейнера, какие файлы есть, какие переменные окружения установлены. `docker exec` даёт тебе терминал прямо внутри работающего контейнера.

```bash
# Зайти в интерактивный bash внутри контейнера
docker exec -it НАЗВАНИЕ bash

# Если bash недоступен (slim/alpine образы) — используй sh
docker exec -it НАЗВАНИЕ sh

# Выполнить одну команду без входа
docker exec НАЗВАНИЕ ls /app        # Посмотреть файлы
docker exec НАЗВАНИЕ env            # Все переменные окружения
docker exec НАЗВАНИЕ python --version

# Выйти из контейнера: введи exit или Ctrl+D
```

### ⚠️ Частая ошибка: OCI runtime exec failed

```
OCI runtime exec failed: exec: "bash": executable file not found in $PATH
```
**Причина:** в минимальных образах (`-slim`, `-alpine`) нет `bash`.
**Решение:** используй `sh` вместо `bash`:
```bash
docker exec -it НАЗВАНИЕ sh
```

---

## Урок 16 — Логи и мониторинг

![module3-docker-logs](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-logs.png)


### 🧠 Теория: как узнать что происходит внутри?

Контейнер изолирован — ты не видишь его «экран». Но всё, что приложение пишет в stdout/stderr, Docker перехватывает и хранит как логи. Это основной инструмент отладки.

```bash
docker logs НАЗВАНИЕ                # Все логи
docker logs -f НАЗВАНИЕ             # Следить в реальном времени (Ctrl+C — выход)
docker logs --tail 50 НАЗВАНИЕ      # Последние 50 строк
docker logs --since 10m НАЗВАНИЕ    # За последние 10 минут

docker stats                        # CPU, RAM, сеть — всех контейнеров
docker stats НАЗВАНИЕ               # Только одного
docker top НАЗВАНИЕ                 # Процессы внутри контейнера
```

---

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-volume.jpg" alt="Docker Volume" width="90%"/>
<br/><em>Volume — мост между контейнером и диском. Данные живут снаружи контейнера!</em>
</div>

## Урок 17 — Тома (Volumes): сохраняем данные

![module3-docker-volume](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-volume.png)


### 🧠 Теория: почему данные исчезают?

По умолчанию все изменения внутри контейнера живут только пока контейнер работает. Удалил контейнер — данные пропали. Для баз данных, загруженных файлов, конфигов это проблема.

**Том (Volume)** — это папка на твоём компьютере, которая «прокидывается» внутрь контейнера. Данные хранятся на хосте — контейнер просто читает и пишет туда.

```bash
# Тип 1: именованный том (Docker управляет путём)
docker run -v mydata:/app/data nginx

# Тип 2: bind mount (ты указываешь путь на хосте)
docker run -v /home/user/files:/app/uploads nginx
docker run -v $(pwd):/app my-site    # $(pwd) = текущая папка

# Управление томами
docker volume ls                     # Список
docker volume inspect mydata         # Детали (где хранится на хосте)
docker volume rm mydata              # Удалить
```

---

## 🎯 Практические задания

### Задание 1 — Первый контейнер
```bash
docker run -d -p 8080:80 --name moy-nginx nginx:1.25
# Открой http://localhost:8080 — приветственная страница nginx
docker logs moy-nginx
docker stop moy-nginx && docker rm moy-nginx
```
> ✅ Видишь страницу nginx? Контейнер работает!

> 💡 Мы используем `nginx:1.25` а не просто `nginx`. Тег без версии (`latest`) — антипаттерн: сегодня скачал одну версию, завтра другую — и всё сломалось. Всегда указывай конкретную версию!

### Задание 2 — Свой Dockerfile
```bash
mkdir moy-sayt && cd moy-sayt
echo "<h1>Привет из Docker!</h1>" > index.html

# Сначала создаём .dockerignore — защита секретов!
cat > .dockerignore << 'EOF'
.env
.git
__pycache__
*.pyc
*.log
EOF

cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EOF

docker build -t moy-sayt:1.0 .
docker run -d -p 8080:80 moy-sayt:1.0
# Открой http://localhost:8080
```
> ✅ Видишь «Привет из Docker!»? Ты запустил свой сайт! 🚀

### Задание 3 — Зайди внутрь контейнера
```bash
docker exec -it moy-sayt /bin/sh
ls /usr/share/nginx/html/
cat /usr/share/nginx/html/index.html
exit
```
> ✅ Видишь index.html внутри контейнера? Отлично!

## Урок 18 — Шпаргалка Docker

![module3-docker-prune](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module3-docker-prune.png)


| Команда | Что делает |
|---------|-----------|
| `docker run -d -p 8080:80 nginx` | Запустить nginx в фоне |
| `docker ps` | Запущенные контейнеры |
| `docker ps -a` | Все контейнеры |
| `docker logs -f ИМЯ` | Логи в реальном времени |
| `docker exec -it ИМЯ sh` | Войти внутрь |
| `docker stop ИМЯ` | Остановить |
| `docker rm ИМЯ` | Удалить |
| `docker build -t ИМЯ .` | Собрать образ |
| `docker images` | Список образов |
| `docker rmi ИМЯ` | Удалить образ |

### 🔑 Ключевые понятия

| Понятие | Простыми словами |
|---------|-----------------|
| Образ | Рецепт (неизменный шаблон) |
| Контейнер | Готовое блюдо (запущенный образ) |
| Dockerfile | Инструкция как приготовить образ |
| Volume | Внешний диск для контейнера |
| Port mapping | Дверь снаружи → дверь внутри (-p 8080:80) |
| .dockerignore | Список файлов которые НЕ копируются в образ |


---

## 🧠 Чекпойнт понимания — обязательный

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/checkpoint.jpg" alt="Чекпойнт понимания" width="90%"/>
<br/><em>Три вопроса после каждого урока. Понимание важнее скорости.</em>
</div>

Прежде чем перейти к Модулю 4 — ответь себе вслух или письменно:

**1. Чем Docker-образ отличается от контейнера? Объясни как аналогию с рецептом и блюдом.**

**2. Зачем нужен `.dockerignore`? Что будет если его не создать?**

**3. В чём разница между `CMD` и `ENTRYPOINT` в Dockerfile?**

**4. Почему не стоит использовать тег `latest` в production? Какой тег лучше?**

> 💡 Если не можешь ответить на вопрос — вернись к соответствующему уроку. Понимание важнее скорости!

➡️ [Следующий модуль: Docker Compose →](../module4-compose/)
