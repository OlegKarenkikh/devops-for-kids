# 🏆 Итоговые проекты

Выполни эти проекты, чтобы закрепить все знания курса.

---

## 📦 Проект 1 — Мой первый сайт (Модуль 1–2)

**Уровень:** Начинающий | **Время:** 1 час

Создай статический HTML-сайт с информацией о себе и опубликуй его на GitHub Pages.

```bash
mkdir мой-сайт && cd мой-сайт
git init
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="ru">
<head><meta charset="utf-8"><title>Мой сайт</title></head>
<body>
  <h1>Привет! Я [твоё имя]</h1>
  <p>Я учусь программировать 🚀</p>
</body>
</html>
EOF
git add . && git commit -m "Первый сайт"
```

**Публикуй на GitHub Pages:**
1. Создай репозиторий на GitHub
2. Запушь код
3. Settings → Pages → Deploy from branch → main

---

## 🐳 Проект 2 — Flask API в Docker (Модуль 3)

**Уровень:** Средний | **Время:** 1.5 часа

Создай REST API на Flask, упакуй в Docker и опубликуй на Docker Hub.

```python
# app.py
from flask import Flask, jsonify
app = Flask(__name__)
items = ["яблоко", "банан", "апельсин"]

@app.route("/")
def home():
    return jsonify({"message": "Мой API работает!", "version": "1.0"})

@app.route("/items")
def get_items():
    return jsonify({"items": items, "count": len(items)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "app.py"]
```

---

## 🎼 Проект 3 — Full-stack с Compose (Модуль 4)

**Уровень:** Средний | **Время:** 2 часа

Flask API + PostgreSQL + Redis кеш — всё через Docker Compose.

**Структура:**
```
проект/
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── .env
```

---

## ⚙️ Проект 4 — Приложение на Kubernetes (Модуль 5)

**Уровень:** Продвинутый | **Время:** 3 часа

Задеплой Проект 3 в minikube:
- Deployment с 3 репликами
- Service (NodePort)
- ConfigMap для настроек
- Secret для паролей
- HorizontalPodAutoscaler

---

## 🚀 Проект 5 — Полный CI/CD пайплайн (Все модули)

**Уровень:** Эксперт | **Время:** 4 часа

Git push → GitHub Actions → docker build → docker push → kubectl apply

Создай `.github/workflows/deploy.yml` который автоматически:
1. Тестирует код
2. Собирает Docker образ
3. Публикует на Docker Hub
4. Деплоит в Kubernetes
