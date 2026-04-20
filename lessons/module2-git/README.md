# 🌿 Модуль 2 — Git и GitHub (Уроки 9–11)

> **Цель:** научиться сохранять историю изменений и делиться кодом через GitHub.

---

> 💡 **Git vs GitHub? Что такое ветка? Зачем SSH-ключ?**  
> → [Ответы в Детском FAQ](../kids-faq/#модуль-2--git)


## Урок 9 — Что такое Git?

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module2-git-workflow.jpg" alt="Git workflow" width="900"/>
  <br/><em>📸 Git-workflow: ты пишешь код → кладёшь в Staging → делаешь коммит-снимок → отправляешь в облако GitHub</em>
</div>


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module2-git-analogy.jpg" alt="Git — система сохранений как в игре" width="85%"/>
<br/><em>Git — как точки сохранения в игре. Каждый commit = сохранение. Можно вернуться в любой момент!</em>
</div>

### 🧠 Теория: зачем нужен Git?

Представь, что ты пишешь большую программу неделями. В пятницу вечером добавляешь новую функцию, всё ломается, и ты не помнишь что изменил. Без Git приходится угадывать. С Git — одна команда, и код вернётся к пятничному утру.

Git хранит **всю историю изменений** как снимки (коммиты). Каждый коммит — это точка сохранения с описанием «что было сделано». Можно вернуться к любому моменту, сравнить версии, работать параллельно в нескольких ветках.

Главное: Git работает **локально** на твоём компьютере. GitHub — это облачное хранилище для Git-репозиториев, чтобы делиться кодом с другими.

```bash
# Настройка (один раз на компьютер)
git config --global user.name  "Твоё Имя"
git config --global user.email "твой@email.com"

# Создать репозиторий
mkdir my-project && cd my-project
git init                     # Инициализирует скрытую папку .git

# Три шага сохранения (add → commit — запомни!)
echo "print('Привет!')" > app.py
git add app.py               # 1. Staging: выбрать что сохранить
git commit -m "Первый коммит — hello world"  # 2. Сохранить снимок
git log --oneline            # Посмотреть историю
git status                   # Что изменилось с последнего коммита?
```

### ⚠️ Типичная ошибка: «nothing to commit»

```
On branch main
nothing to commit, working tree clean
```
**Это не ошибка!** Это значит, что все изменения уже сохранены. Измени файл и снова сделай `git add` + `git commit`.

---

## Урок 10 — Ветки и GitHub


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module2-git-branches.jpg" alt="Git ветки" width="90%"/>
<br/><em>Main всегда работает. Эксперименты — в отдельных ветках!</em>
</div>
### 🧠 Теория: зачем нужны ветки?

Представь: ты работаешь над сайтом и хочешь добавить форму входа. Но сайт уже работает у пользователей — нельзя сломать. Решение: создать **ветку** (branch) — параллельную копию кода. Добавляешь там форму, тестируешь. Когда готово — сливаешь (merge) в основную ветку.

По умолчанию основная ветка называется `main`. Все новые функции разрабатываются в отдельных ветках, потом сливаются в `main`.

```bash
# Ветки = параллельные версии кода
git branch                      # Список веток (* = текущая)
git checkout -b feature/login   # Создать ветку и перейти в неё

# Работаем в ветке
echo "# Login form" >> app.py
git add . && git commit -m "Добавить форму входа"

# Слить в main
git checkout main
git merge feature/login         # Объединить изменения
git branch -d feature/login     # Удалить ветку (она больше не нужна)

# Отправить на GitHub
git remote add origin https://github.com/ТЫ/проект.git
git push -u origin main         # Первый раз (-u запоминает origin main)
git push                        # Последующие разы
git pull                        # Получить чужие изменения
```

---

## Урок 11 — SSH: подключение без пароля и решение проблем

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module2-ssh-keys.jpg" alt="SSH ключи" width="900"/>
  <br/><em>🗝️ SSH-ключи как замок и ключ: публичный ключ отдаёшь серверу, приватный — хранишь только у себя</em>
</div>



### 🧠 Теория: что такое SSH и зачем он нужен?

SSH (Secure Shell) — протокол безопасного подключения к удалённым серверам. Вместо пароля используется пара ключей: **публичный** (можно раздавать всем) и **приватный** (только у тебя, никому не показывать).

GitHub рекомендует использовать SSH вместо HTTPS-пароля — это удобнее и безопаснее.

```bash
# Создать SSH ключ
ssh-keygen -t ed25519 -C "твой@email.com"
# Нажми Enter 3 раза (путь по умолчанию, без пароля)

# Посмотреть публичный ключ
cat ~/.ssh/id_ed25519.pub
# Скопируй всё (начинается с "ssh-ed25519 ...")

# Добавить ключ в GitHub:
# github.com → Settings → SSH and GPG keys → New SSH key → вставь

# Проверить подключение
ssh -T git@github.com
# Должно ответить: Hi username! You've successfully authenticated
```


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module2-ssh-troubleshoot.jpg" alt="SSH troubleshooting" width="90%"/>
<br/><em>Следуй блок-схеме — шаг за шагом найдёшь проблему</em>
</div>
### ⚠️ Что делать если SSH не пускает?

SSH-проблемы — одни из самых частых. Вот все типичные случаи:

**Проблема 1: Permission denied (publickey)**
```
git@github.com: Permission denied (publickey).
```
**Диагностика по шагам:**
```bash
# Шаг 1: есть ли ключи?
ls ~/.ssh/
# Должны быть: id_ed25519 и id_ed25519.pub

# Шаг 2: добавлен ли ключ в ssh-agent?
ssh-add -l
# Если "The agent has no identities" — добавь:
ssh-add ~/.ssh/id_ed25519

# Шаг 3: какой ключ видит GitHub?
ssh -vT git@github.com 2>&1 | grep "Offering"
# Должен показать твой ключ

# Шаг 4: совпадает ли публичный ключ с тем что в GitHub?
cat ~/.ssh/id_ed25519.pub
# Сравни с github.com → Settings → SSH keys
```

**Проблема 2: UNPROTECTED PRIVATE KEY FILE**
```
WARNING: UNPROTECTED PRIVATE KEY FILE!
Permissions 0644 for '/home/user/.ssh/id_ed25519' are too open.
```
**Причина:** приватный ключ доступен для чтения другим пользователям — это опасно, SSH отказывается его использовать.
```bash
chmod 600 ~/.ssh/id_ed25519       # Только владелец может читать
chmod 700 ~/.ssh/                 # Только владелец видит папку
```

**Проблема 3: Host key verification failed**
```
Host key verification failed.
```
**Причина:** сервер изменил свой ключ, или первое подключение к нему.
```bash
# Удалить старую запись (если сервер переустановлен)
ssh-keygen -R github.com
# Подключиться снова — он спросит "Are you sure?" → введи yes
ssh -T git@github.com
```

**Проблема 4: Connection refused / Network unreachable**
```
ssh: connect to host github.com port 22: Connection refused
```
**Причина:** корпоративный файрвол блокирует порт 22.
```bash
# Попробовать SSH через порт 443 (HTTPS порт — почти никогда не блокируется)
# Добавь в ~/.ssh/config:
cat >> ~/.ssh/config << 'EOF'
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
EOF
ssh -T git@github.com   # Проверить
```

**Проблема 5: всё правильно, но push не работает**
```
remote: Repository not found.
```
**Причина:** используешь HTTPS URL вместо SSH.
```bash
# Проверить текущий URL
git remote -v
# Если видишь https://github.com/... — переключи на SSH:
git remote set-url origin git@github.com:ТЫ/проект.git
```

---


---

## 🎯 Практические задания

### Задание 1 — Первый репозиторий
```bash
mkdir moy-proekt && cd moy-proekt
git init
echo "# Мой первый проект" > README.md
git add README.md
git commit -m "Первый коммит"
git log --oneline
```
> ✅ Видишь строку с хешем и «Первый коммит»? Отлично!

### Задание 2 — Ветки
```bash
git checkout -b feature/hello
echo "print('Привет, Git!')" > hello.py
git add hello.py && git commit -m "Добавил hello.py"
git checkout main
git merge feature/hello
git log --oneline --graph
```
> ✅ В логе видна развилка и слияние? Задание выполнено!

### Задание 3 — Публикация на GitHub
```bash
# 1. Создай репозиторий на github.com (кнопка «New»)
# 2. Привяжи локальный проект:
git remote add origin git@github.com:ТВО_ИМЯ/moy-proekt.git
git push -u origin main
# 3. Зайди на github.com — файлы там! ✅
```

## Шпаргалка Git + SSH

| Команда | Действие |
|---------|---------|
| `git init` | Создать репозиторий |
| `git add .` | Добавить все файлы в staging |
| `git commit -m "..."` | Сохранить снимок |
| `git push` | Отправить на GitHub |
| `git pull` | Получить изменения |
| `git log --oneline` | История коммитов |
| `git checkout -b ветка` | Создать и перейти в ветку |
| `ssh -T git@github.com` | Проверить SSH |
| `ssh-add ~/.ssh/id_ed25519` | Добавить ключ в агент |
| `chmod 600 ~/.ssh/id_ed25519` | Исправить права ключа |

➡️ [Следующий модуль: Docker →](../module3-docker/)

---

## ❓ Вопросы новичков — Git

<details>
<summary><strong>Git и GitHub — это одно и то же?</strong></summary>

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/kid_git_github.jpg" alt="Git vs GitHub" width="85%"/>
<br/><em>Git = программа на твоём компьютере. GitHub = сайт в интернете. Разные вещи!</em>
</div>

Нет, это **разные вещи**:

| | Git | GitHub |
|---|---|---|
| Что это | Программа на компьютере | Сайт в интернете |
| Где хранит | На твоём диске | В облаке (серверы Microsoft) |
| Без интернета | Работает | Не работает |

Существуют аналоги: **GitLab** (популярен в России), **Bitbucket**, **Gitea**.

</details>

<details>
<summary><strong>Что такое «ветка» в Git?</strong></summary>

Ветка — **параллельная копия** твоего кода для экспериментов, не ломающих основной код.

```bash
git checkout -b feature/новая-кнопка   # Создать ветку
# ... делаешь изменения ...
git add . && git commit -m "Добавил кнопку"
git checkout main                       # Вернуться
git merge feature/новая-кнопка         # Влить изменения
```

> 🎮 Аналогия: ветка — как «сохранить и попробовать другой путь» в RPG. Не удался — просто удаляешь ветку.

</details>

<details>
<summary><strong>SSH-ключ — это как замок с ключом?</strong></summary>

Точно! SSH работает **именно как замок с ключом**:
- **Публичный ключ** (`.pub`) = замок — даёшь серверу/GitHub
- **Приватный ключ** = ключ — только у тебя, никому не показываешь

```bash
ssh-keygen -t ed25519 -C "твой@email.com"
# Создаст два файла:
# ~/.ssh/id_ed25519      ← приватный (только у тебя!)
# ~/.ssh/id_ed25519.pub  ← публичный (вставляешь в GitHub Settings → SSH Keys)
```

> 🔐 Правило: приватный ключ — как паспорт. Никому не показывай.

</details>

<details>
<summary><strong>Зачем .gitignore?</strong></summary>

.gitignore — список того, что Git **не должен** отслеживать и не отправлять в GitHub:

```bash
# .gitignore — примеры:
.env            # пароли и секреты
node_modules/   # тысячи файлов библиотек
__pycache__/    # кэш Python
.DS_Store       # служебные файлы macOS
*.log           # лог-файлы
```

Главное правило: **никогда не коммить `.env`** — там пароли, которые увидит весь мир.

</details>

