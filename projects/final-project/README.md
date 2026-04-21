# 🏆 Итоговый проект — «Моя Коллекция»

<div align="center">

![final-project-pyramid](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/final-project-pyramid.png)

**Ты прошёл весь курс — и теперь строишь настоящий DevOps-проект!**

</div>

---

## 🤔 Что мы строим и зачем?

«Моя Коллекция» — это REST API-сервис, который хранит список твоих любимых вещей  
(книги, игры, фильмы — что угодно!) в базе данных.

### Что будет в итоге?

```
Браузер / curl
      │
      ▼
Flask REST API (:8080)
      │
      ▼
SQLite (файл collection.db)
```

### Маршруты API

| Метод  | Маршрут          | Что делает               |
|--------|-----------------|--------------------------|
| GET    | `/`              | Информация о сервисе     |
| GET    | `/items`         | Список всех предметов    |
| GET    | `/items/<id>`    | Один предмет по ID       |
| POST   | `/items`         | Добавить предмет         |
| PUT    | `/items/<id>`    | Изменить предмет         |
| DELETE | `/items/<id>`    | Удалить предмет          |

---

## 🗂️ Структура проекта

```
final-project/
├── app.py                 ← Flask REST API (Модуль 6)
├── requirements.txt       ← зависимости Python
├── .env.example           ← пример переменных окружения (Модуль 6)
├── .gitignore             ← что не коммитим в Git (Модуль 2)
├── Dockerfile             ← рецепт образа (Модуль 3)
├── docker-compose.yml     ← оркестрация (Модуль 4)
├── Makefile               ← удобные команды (make run / make k8s-deploy)
└── k8s/
    ├── deployment.yaml    ← Deployment с livenessProbe (Модуль 5)
    ├── service.yaml       ← NodePort :30080 (Модуль 5)
    ├── hpa.yaml           ← авто-масштабирование CPU 70% (Модуль 5)
    ├── configmap.yaml     ← конфиг (Модуль 5)
    └── secret.yaml        ← пример Secret (Модуль 6)
```

---

## 🛠️ Быстрый старт

```bash
# Клонировать репо
git clone https://github.com/OlegKarenkikh/devops-for-kids.git
cd devops-for-kids/projects/final-project

# Создать .env из примера
cp .env.example .env
```

---

## Шаг 1 — Запуск локально (Модули 1–2)

```bash
pip install -r requirements.txt
python app.py
# Открой http://localhost:8080
```

---

## Шаг 2 — Код на Python (Модуль 6)

Изучи `app.py` — обрати внимание:
- **`os.environ.get()`** — читаем настройки из переменных окружения
- **`load_dotenv()`** — загружаем `.env` файл
- **SQLite** — лёгкая база данных в одном файле

```bash
# Тест вручную
curl http://localhost:8080/

# Добавить предмет
curl -X POST http://localhost:8080/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Моя книга", "emoji": "📚", "comment": "очень интересная"}'

# Посмотреть список
curl http://localhost:8080/items
```

---

## Шаг 3 — Docker (Модуль 3)

```bash
# Собрать образ
docker build -t my-collection:latest .

# Запустить контейнер
docker run -p 8080:8080 my-collection:latest

# Или используй Makefile:
make build
```

---

## Шаг 4 — Docker Compose (Модуль 4)

```bash
docker compose up -d

# Проверить статус
docker compose ps
docker compose logs -f

# Или через Makefile:
make compose-up
make logs
```

> Данные сохраняются в volume `collection-data` — даже после перезапуска!

---

## Шаг 5 — Kubernetes (Модуль 5)

```bash
# Запустить minikube
minikube start

# Задеплоить всё одной командой
make k8s-deploy

# Или вручную:
kubectl apply -f k8s/
kubectl get pods
kubectl get services

# Открыть сервис
minikube service collection-service --url
```

### Проверь самовосстановление!

```bash
# Удали под вручную
kubectl delete pod -l app=collection

# Kubernetes сразу создаст новый! Проверь:
kubectl get pods -w
```

### Авто-масштабирование HPA

```bash
kubectl get hpa
# При нагрузке CPU > 70% — добавит поды автоматически (до 5)
```

---

## Шаг 6 — Опубликуй на GitHub (Модуль 2)

```bash
# Все изменения закоммить
git add .
git commit -m "feat: мой первый DevOps-проект"
git push origin main
```

---

## make — все команды

```
make run          — запустить локально (Python)
make build        — собрать Docker-образ
make compose-up   — запустить через Docker Compose
make compose-down — остановить Docker Compose
make k8s-deploy   — задеплоить в Kubernetes
make k8s-delete   — удалить из Kubernetes
make test         — тест API (curl)
make clean        — очистить всё
make help         — эта помощь
```

---

## ✅ Чеклист

- [ ] Запустил локально (`python app.py`)
- [ ] Добавил 3+ предмета через curl
- [ ] Собрал Docker-образ (`docker build`)
- [ ] Запустил через `docker compose up -d`
- [ ] Задеплоил в Kubernetes (`make k8s-deploy`)
- [ ] Проверил самовосстановление pod'а
- [ ] Посмотрел на HPA (`kubectl get hpa`)
- [ ] Запушил на GitHub (`git push`)

---

## 🎓 Поздравляем!

Ты прошёл весь курс **DevOps для детей** и запустил настоящий сервис:

| Модуль | Что использовал |
|--------|----------------|
| M0-1   | Терминал, команды, файловая система |
| M2     | Git, ветки, GitHub, SSH |
| M3     | Docker, образ, контейнер, Dockerfile |
| M4     | Docker Compose, сети, volumes |
| M5     | Kubernetes, Pod, Deployment, HPA |
| M6     | Flask REST API, .env, SQLite, Secrets |

**Ты — настоящий DevOps-инженер! 🚀**

---

*← [Модуль 6](../../lessons/module6-secrets-api/) | [FAQ](../../lessons/kids-faq/)*
