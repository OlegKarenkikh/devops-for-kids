# 🌿 Модуль 2 — Git и GitHub (Уроки 6–8)

> **Цель:** сохранять историю изменений, работать с ветками и делиться кодом на GitHub.

---

## 📖 Урок 6 — Git: сохраняем работу

### 🧠 Объяснение

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module2-git-analogy.png" alt="Git как сохранение в игре" width="80%"/>
<br/><em>Git — как «сохранить игру»: каждый коммит = точка возврата</em>
</div>

Помнишь сохранения в видеоиграх? **Git** — это точно такая же система для кода. Каждое сохранение называется **коммит** (commit).

### 💻 Установка и настройка

```bash
sudo apt install git
git config --global user.name "Твоё Имя"
git config --global user.email "твой@email.com"
```

### 💻 Основные команды

```bash
git init                  # Начать Git-проект
git status                # Что изменилось?
git add .                 # Добавить всё к сохранению
git commit -m "Текст"    # Сохранить
git log --oneline         # История сохранений
git diff                  # Что изменилось?
```

### 📊 Схема работы

```
Рабочая папка  →  git add  →  Staging  →  git commit  →  История
(изменяешь)                  (готово)                   (сохранено!)
```

### 🧪 Задание 6

```bash
mkdir мой-сайт && cd мой-сайт
git init
echo "# Мой первый сайт" > README.md
git add .
git commit -m "🎉 Первый коммит"
git log --oneline
```

---

## 📖 Урок 7 — Ветки

```bash
git branch                 # Список веток
git checkout -b моя-идея   # Создать и переключиться
git merge моя-идея         # Слить ветку в текущую
git branch -d моя-идея     # Удалить ветку
```

### 🧪 Задание 7

```bash
git checkout -b добавляю-контент
echo "- пункт 1" >> README.md
git add . && git commit -m "Добавил контент"
git checkout main
git merge добавляю-контент
git log --oneline
```

---

## 📖 Урок 8 — GitHub

```bash
git remote add origin https://github.com/ИМЯ/РЕПО.git
git branch -M main
git push -u origin main   # Отправить первый раз
git push                  # Следующие разы
git pull                  # Получить изменения
git clone URL             # Скачать проект
```

### 🧪 Задание 8

1. Зарегистрируйся на [github.com](https://github.com)
2. Создай новый репозиторий
3. Выполни команды выше

---

## 📋 Шпаргалка Модуля 2

| Команда | Что делает |
|---------|-----------|
| `git init` | Начать репозиторий |
| `git add .` | Добавить всё |
| `git commit -m "текст"` | Сохранить |
| `git log --oneline` | История |
| `git checkout -b имя` | Новая ветка |
| `git merge имя` | Слить |
| `git push / pull` | Облако |
| `git clone URL` | Скачать |

➡️ [Следующий модуль: Docker →](../module3-docker/)
