# 🐧 Модуль 1 — Терминал и Linux (Уроки 1–8)

> **Цель:** уверенно работать в командной строке Linux, управлять файлами, пользователями и безопасным доступом.

---

> 💡 **Вопросы по терминалу?** Что значит `$`? Почему команды такие короткие? Что такое root?  
> → [Ответы в Детском FAQ](../kids-faq/#модуль-1--терминал)


## Урок 1 — Что такое терминал?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/terminal-intro.png" alt="Терминал — это разговор с компьютером" width="85%"/>
<br/><em>Терминал — это как разговор с компьютером на его языке. Ты пишешь команду — компьютер выполняет</em>
</div>

```bash
whoami          # Кто я? (имя текущего пользователя)
pwd             # Где я? (текущая папка)
ls              # Что здесь есть? (список файлов)
ls -la          # Подробный список с правами и размерами
clear           # Очистить экран (или Ctrl+L)
```

---

## Урок 2 — Файловая система

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module1-filesystem.png" alt="Файловая система Linux" width="900"/>
  <br/><em>📁 Рис. 1 — Дерево каталогов Linux: от корня / до твоей домашней папки</em>
</div>


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module1-permissions.png" alt="Права доступа через замки" width="85%"/>
<br/><em>Права — три замка: для владельца, группы, всех остальных. r=читать, w=писать, x=запускать</em>
</div>

```bash
ls -la script.sh          # Смотрим права: -rwxr-xr-x
chmod +x script.sh        # Добавить право на запуск всем
chmod 755 script.sh       # rwxr-xr-x (стандарт для скриптов)
chmod 644 config.txt      # rw-r--r-- (стандарт для конфигов)
chmod 600 ~/.ssh/id_rsa   # rw------- (только владелец — ключи!)

# Что значат цифры:
# 4 = r (читать)    2 = w (писать)    1 = x (выполнять)
# 7 = 4+2+1 = rwx   6 = 4+2 = rw-    5 = 4+1 = r-x
```

---

## Урок 4 — chown: смена владельца

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module1-chown.png" alt="chown — именной ярлык на файле" width="85%"/>
<br/><em>chown — как именной ярлык на вещи. Меняешь ярлык — меняется хозяин</em>
</div>

```bash
ls -la app.py
# -rw-r--r-- 1 root root 1234 Mar 23 app.py
#              ^^^^  ^^^^
#           владелец группа

sudo chown alice app.py             # Передать файл пользователю alice
sudo chown alice:developers app.py  # alice + группа developers
sudo chown -R alice:www-data /var/www/  # Рекурсивно для папки
sudo chown $(whoami) файл.txt       # Себе

# Пример — типичная ошибка и её исправление:
sudo systemctl start nginx          # Ошибка: /var/log/nginx: Permission denied
sudo chown -R www-data:www-data /var/log/nginx/
sudo systemctl start nginx          # Теперь работает!
```

---

## Урок 5 — Пользователи и группы

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module1-users-groups.png" alt="Пользователи и группы" width="85%"/>
<br/><em>Пользователи — это люди, группы — это команды. Один человек может быть в нескольких командах</em>
</div>

```bash
# Просмотр
id                         # Мой UID, GID и группы
who                        # Кто сейчас в системе
cat /etc/passwd            # Все пользователи (имя:x:UID:GID:...)
cat /etc/group             # Все группы

# Создание пользователя
sudo adduser alice                      # Создать (с home-папкой)
sudo useradd -m -s /bin/bash bob        # Вручную
sudo passwd alice                       # Установить пароль

# Управление группами
sudo groupadd developers                # Создать группу
sudo usermod -aG docker alice           # Добавить alice в группу docker
sudo usermod -aG sudo alice             # Сделать alice администратором
groups alice                            # Проверить группы alice
sudo deluser alice developers           # Убрать из группы

# Полезно при работе с Docker:
sudo usermod -aG docker $USER           # Чтобы запускать docker без sudo
newgrp docker                           # Применить без перезахода
```

> **📝 Задание:** создай пользователя `devuser`, добавь в группу `docker`, убедись командой `groups devuser`.

---

## Урок 6 — SSH: безопасный вход на сервер

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module1-ssh-keys.png" alt="SSH ключи — цифровой замок" width="85%"/>
<br/><em>SSH-ключи — это как замок и ключ. Публичный ключ (замок) — на сервере. Приватный ключ — только у тебя</em>
</div>

```bash
# Генерация ключевой пары (один раз на своей машине)
ssh-keygen -t ed25519 -C "твой@email.com"
# Создаётся:
#   ~/.ssh/id_ed25519      ← приватный ключ (НИКОМУ не давать!)
#   ~/.ssh/id_ed25519.pub  ← публичный ключ (можно копировать)

# Копировать публичный ключ на сервер
ssh-copy-id user@сервер_ip          # Автоматически
# Или вручную:
cat ~/.ssh/id_ed25519.pub           # Скопировать текст
ssh user@сервер "mkdir -p ~/.ssh && echo 'ВСТАВИТЬ_КЛЮЧ' >> ~/.ssh/authorized_keys"

# Подключение
ssh user@192.168.1.100              # По IP
ssh user@myserver.com               # По домену
ssh -i ~/.ssh/mykey user@server     # Конкретный ключ

# ~/.ssh/config — умные псевдонимы
cat >> ~/.ssh/config << 'EOF'
Host prod
    HostName 192.168.1.100
    User alice
    IdentityFile ~/.ssh/id_ed25519
    Port 22

Host dev
    HostName 10.0.0.5
    User developer
    IdentityFile ~/.ssh/dev_key
EOF

ssh prod                            # Теперь просто! (вместо ssh alice@192.168.1.100)
ssh dev

# Права SSH-файлов (обязательно!)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/config

# Отладка подключения
ssh -v user@server                  # Verbose — видим процесс
ssh -vvv user@server                # Максимальная детализация
```

> **🔐 Правило:** приватный ключ `id_ed25519` — как паспорт. Никому не отправляй, не коммить в Git!

---

## Урок 7 — Bash-скрипты

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module1-bash-script.png" alt="Структура Bash-скрипта" width="900"/>
  <br/><em>🖥️ Рис. 2 — Анатомия bash-скрипта: шебанг, переменные, условия, цикл</em>
</div>


```bash
#!/bin/bash
# Мой первый скрипт (hello.sh)

NAME=$(whoami)
DATE=$(date +"%d.%m.%Y %H:%M")
echo "Привет, $NAME! Сейчас $DATE"
echo "Ты находишься в: $(pwd)"
echo "Диск: $(df -h / | tail -1 | awk '{print $5}')"
```

```bash
chmod +x hello.sh
./hello.sh
```

---


---

## 🎯 Практические задания

### Задание 1 — Навигация и файлы
```bash
# Выполни все команды по порядку
pwd                          # где ты?
ls -la ~                     # что в домашней папке?
mkdir ~/my-course && cd ~/my-course
echo "Привет, Linux!" > hello.txt
cat hello.txt
cp hello.txt hello-copy.txt
ls -la
```
> ✅ Видишь два файла? Отлично!

### Задание 2 — Права доступа
```bash
touch secret.txt
chmod 600 secret.txt          # только владелец читает/пишет
ls -la secret.txt             # -rw------- ?

touch script.sh
echo '#!/bin/bash
echo "Скрипт работает!"' > script.sh
chmod +x script.sh
./script.sh
```
> ✅ Скрипт выполнился? Права работают!

### Задание 3 — SSH ключ
```bash
ssh-keygen -t ed25519 -C "moy-kurs" -f ~/.ssh/id_kurs
ls -la ~/.ssh/
cat ~/.ssh/id_kurs.pub        # это твой публичный ключ
```
> ✅ Два файла в ~/.ssh/: id_kurs и id_kurs.pub — готово!

## Урок 8 — Шпаргалка

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module1-commands-cheatsheet.png" alt="Шпаргалка по командам Linux" width="85%"/>
</div>

| Команда | Действие |
|---------|---------|
| `ls -la` | Список файлов с правами |
| `chmod 755 file` | Установить права |
| `chown user:group file` | Сменить владельца |
| `adduser alice` | Создать пользователя |
| `usermod -aG group user` | Добавить в группу |
| `ssh-keygen -t ed25519` | Создать ключи |
| `ssh-copy-id user@host` | Скопировать ключ на сервер |

➡️ [Следующий модуль: Git →](../module2-git/)

---

## ❓ Частые вопросы новичков по этому уроку

<details>
<summary><b>Почему команды такие короткие — ls, cd, pwd?</b></summary>

Их придумали в **1970-х годах**, когда клавиатуры были медленными и дорогими, а сети — крайне медленными. Чем короче команда, тем быстрее набрать и передать.

| Команда | Расшифровка | Что делает |
|---------|------------|------------|
| `ls` | list | Показать список файлов |
| `cd` | change directory | Сменить папку |
| `pwd` | print working directory | Показать текущую папку |
| `rm` | remove | Удалить |
| `cp` | copy | Копировать |
| `mv` | move | Переместить / переименовать |
| `mkdir` | make directory | Создать папку |

Со временем запомнишь их автоматически — как буквы на клавиатуре.

</details>

<details>
<summary><b>Знак $ в начале строки — это часть команды?</b></summary>

**Нет!** Знак `$` — это приглашение терминала (prompt). Он показывает, что терминал ждёт твою команду.

```bash
$ ls        ← знак $ НЕ набираешь — это обозначение в документации
$ cd /home  ← вводишь только: cd /home
```

Когда видишь в инструкции `$ команда` — набирай только то, что **после** `$`.

> Если в начале строки стоит `#` — это команда для **root** (администратора). Будь осторожен!

</details>

<details>
<summary><b>Что такое root и зачем он нужен?</b></summary>

Root — это **главный администратор** Linux. Он может всё: установить любую программу, удалить любой файл, сломать систему.

```bash
whoami        # Узнать, кто ты
sudo whoami   # Выполнить как root (покажет: root)
```

> ⚠️ Правило: не работай под root постоянно. Одна опечатка — и можно удалить всю систему. Используй `sudo` только когда это действительно необходимо.

</details>

<details>
<summary><b>Зачем нужен bash-скрипт?</b></summary>

Скрипт — это **список команд** в файле, чтобы запускать их все сразу одной командой.

```bash
# Без скрипта — каждый раз вручную (5 команд):
git pull && npm install && npm run build && docker build -t app . && docker push app

# Со скриптом — одна команда:
./deploy.sh
```

Скрипт — как макрос в Excel: один раз написал, дальше запускаешь в одно касание.

</details>

> 💬 Остались вопросы? Смотри [полный FAQ (48 вопросов)](../kids-faq/) или открой [issue на GitHub](https://github.com/OlegKarenkikh/devops-for-kids/issues).

