# 🌿 Модуль 2 — Git и GitHub (Уроки 9–11)

> **Цель:** научиться сохранять историю изменений и делиться кодом через GitHub.

---

## Урок 9 — Что такое Git?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module2-git-analogy.jpg" alt="Git — система сохранений как в игре" width="85%"/>
<br/><em>Git — как точки сохранения в игре. Каждый commit = сохранение. Можно вернуться в любой момент!</em>
</div>

### 🧠 Зачем Git?

> Представь, что ты пишешь сочинение и хочешь сохранять черновики: «черновик 1», «черновик 2», «финальная версия». Git делает это автоматически для кода.

```bash
# Настройка (один раз)
git config --global user.name  "Твоё Имя"
git config --global user.email "твой@email.com"

# Создать репозиторий
mkdir мой-проект && cd мой-проект
git init                     # Создать .git папку
git status                   # Что изменилось?

# Три шага сохранения
echo "print('Привет!')" > app.py
git add app.py               # 1. Выбрать файлы
git commit -m "Первый коммит — hello world"  # 2. Сохранить
git log --oneline            # Посмотреть историю
```

---

## Урок 10 — Ветки и GitHub

```bash
# Ветки = параллельные версии
git branch                   # Список веток
git branch feature/кнопка    # Создать ветку
git checkout feature/кнопка  # Переключиться
# или сразу:
git checkout -b feature/форма

# Изменяем код в ветке
echo "# Форма" >> app.py
git add . && git commit -m "Добавил форму"

# Сливаем в main
git checkout main
git merge feature/кнопка     # Объединить изменения
git branch -d feature/кнопка # Удалить ветку

# GitHub
git remote add origin https://github.com/ТЫ/проект.git
git push -u origin main      # Первый раз
git push                     # Последующие разы
git pull                     # Получить чужие изменения
```

---

## Урок 11 — Шпаргалка Git

| Команда | Действие |
|---------|---------|
| `git init` | Создать репозиторий |
| `git add .` | Добавить все файлы |
| `git commit -m "..."` | Сохранить с сообщением |
| `git push` | Отправить на GitHub |
| `git pull` | Получить изменения |
| `git log --oneline` | История коммитов |
| `git checkout -b ветка` | Создать и перейти в ветку |

➡️ [Следующий модуль: Docker →](../module3-docker/)
