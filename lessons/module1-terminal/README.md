# 🐧 Модуль 1 — Терминал и Linux (Уроки 1–8)

> **Цель:** уверенно работать в командной строке Linux, управлять файлами, пользователями и безопасным доступом.

---

> 💡 **Вопросы по терминалу?** Что значит `$`? Почему команды такие короткие? Что такое root?  
> → [Ответы в Детском FAQ](../kids-faq/#модуль-1--терминал)


## Урок 1 — Что такое терминал?


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-terminal-analogy.jpg" alt="Терминал — это разговор с компьютером" width="85%"/>
<br/><em>Терминал — это как разговор с компьютером на его языке. Ты пишешь команду — компьютер выполняет</em>
</div>

### 🧠 Теория: что такое терминал?

Представь: компьютер — это очень послушный помощник. Обычно ты говоришь с ним мышкой: кнопки, иконки, меню. **Терминал — это говорить текстом.** Напрямую, без посредников.

Зачем? Потому что у серверов в интернете нет экрана, мышки и кнопок. Единственный способ управлять ими — терминал. Всё, что DevOps-инженер делает на сервере, он делает командами.

```bash
whoami          # Кто я? (имя текущего пользователя)
pwd             # Где я? (текущая папка)
ls              # Что здесь есть? (список файлов)
ls -la          # Подробный список с правами и размерами
clear           # Очистить экран (или Ctrl+L)

---

## Урок 2 — Файловая система


<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-filesystem.jpg" alt="Файловая система Linux" width="90%"/>
  <br/><em>📁 Рис. 1 — Дерево каталогов Linux: от корня / до твоей домашней папки</em>
</div>

### 🧠 Теория: файловая система

Linux организован как дерево. Корень — это `/` (слэш). Как папки на рабочем столе, но вложенные. `/home` — твои файлы, `/etc` — настройки системы, `/var` — логи и переменные данные. Всё начинается от одного корня.

bash
cd /home        # Перейти в папку /home
cd ~            # Перейти домой (твоя папка)
cd ..           # Подняться на уровень выше
mkdir мой-проект          # Создать папку
touch hello.txt           # Создать пустой файл
echo "Привет!" > hello.txt  # Записать текст в файл
cat hello.txt             # Прочитать файл
cp hello.txt копия.txt    # Скопировать
mv hello.txt bye.txt      # Переименовать / переместить
rm bye.txt                # Удалить файл
rm -rf папка/             # Удалить папку целиком (ОСТОРОЖНО!)

> ## ☠️ СТОП — прочитай перед тем как продолжить
> `rm -rf папка/` — **необратимо**. Корзины нет. Backup не создаётся автоматически.
> **Всегда** делай `ls папка/` перед удалением — убедись что удаляешь нужное.
> В продакшне эта команда без должной осторожности уничтожала целые проекты. Без шуток.

---

## Урок 3 — Права доступа (chmod)


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/kid_chmod.jpg" alt="chmod — как замки на дверях" width="80%"/>
<br/><em>chmod — как замки на дверях: r=читать, w=писать, x=запускать</em>
</div>



<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-permissions.jpg" alt="Права доступа через замки" width="85%"/>
<br/><em>Права — три замка: для владельца, группы, всех остальных. r=читать, w=писать, x=запускать</em>
</div>

### 🧠 Теория: права доступа

Каждый файл в Linux имеет три «замка»: для **владельца**, его **группы**, и **всех остальных**. Три вида прав: читать (`r`=4), писать (`w`=2), запускать (`x`=1). Число = сумма прав. 7=всё, 6=читать+писать, 5=читать+запускать.

bash
ls -la script.sh          # Смотрим права: -rwxr-xr-x
chmod +x script.sh        # Добавить право на запуск всем
chmod 755 script.sh       # rwxr-xr-x (стандарт для скриптов)
chmod 644 config.txt      # rw-r--r-- (стандарт для конфигов)
chmod 600 ~/.ssh/id_rsa   # rw------- (только владелец — ключи!)

# Что значат цифры:
# 4 = r (читать)    2 = w (писать)    1 = x (выполнять)
# 7 = 4+2+1 = rwx   6 = 4+2 = rw-    5 = 4+1 = r-x

---

## Урок 4 — chown: смена владельца


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-chown.jpg" alt="chown — именной ярлык на файле" width="85%"/>
<br/><em>chown — как именной ярлык на вещи. Меняешь ярлык — меняется хозяин</em>
</div>

### 🧠 Теория: зачем менять владельца?

Когда `nginx` запускается — он работает от имени пользователя `www-data`. Если файл принадлежит `root` — nginx не может его прочитать. `chown` передаёт «ключ» от файла другому пользователю. Это типичная ситуация в продакшне: сервис не может прочитать файл не потому что нет прав chmod, а потому что неправильный владелец.

bash
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

---

## Урок 5 — Пользователи и группы


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-users-groups.jpg" alt="Пользователи и группы" width="85%"/>
<br/><em>Пользователи — это люди, группы — это команды. Один человек может быть в нескольких командах</em>
</div>

### 🧠 Теория: пользователи и группы

Linux — **многопользовательская** система. Каждый процесс запускается от имени какого-то пользователя. Группы — как отделы в компании: один человек может быть в нескольких. Права управляются через них. Например, добавить себя в группу `docker` — и можно запускать контейнеры без `sudo`.

bash
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

> **📝 Задание:** создай пользователя `devuser`, добавь в группу `docker`, убедись командой `groups devuser`.

---

## Урок 6 — SSH: безопасный вход на сервер


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/kid_server.jpg" alt="Сервер" width="80%"/>
<br/><em>Сервер — это компьютер без экрана, которым управляют через терминал</em>
</div>



### 🧠 Теория: SSH и два сценария его применения

SSH (Secure Shell) — протокол для **безопасного подключения к удалённым серверам**. В этом уроке ты настроишь SSH для подключения к серверам. В Модуле 2 (Урок 11) будет **другой сценарий** — SSH для GitHub.

> 💡 **Два разных применения одного инструмента:**
>
> | | SSH → сервер (этот урок) | SSH → GitHub (Модуль 2, Урок 11) |
> |---|---|---|
> | Куда копируем ключ | `/home/user/.ssh/authorized_keys` на сервере | github.com → Settings → SSH keys |
> | Проверка | `ssh user@server-ip` | `ssh -T git@github.com` |
> | Зачем | Управлять сервером без пароля | Делать `git push` без пароля |
>
> Если пока непонятно зачем это нужно — вернись сюда после Модуля 2. Тогда всё встанет на место.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-ssh-keys.jpg" alt="SSH ключи — цифровой замок" width="85%"/>
<br/><em>SSH-ключи — это как замок и ключ. Публичный ключ (замок) — на сервере. Приватный ключ — только у тебя</em>
</div>

bash
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

> **🔐 Правило:** приватный ключ `id_ed25519` — как паспорт. Никому не отправляй, не коммить в Git!

---

## Урок 7 — Bash-скрипты


### 🧠 Теория: зачем писать скрипты?

Скрипт — это **список команд**, записанный в файл. Вместо того чтобы каждый раз вводить 10 команд вручную — запускаешь один файл. Строка `#!/bin/bash` в начале — это «шебанг»: подсказка системе **каким интерпретатором** запускать файл. Без неё Linux не знает это bash, Python или что-то ещё.

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-bash-script.jpg" alt="Структура Bash-скрипта" width="90%"/>
  <br/><em>🖥️ Рис. 2 — Анатомия bash-скрипта: шебанг, переменные, условия, цикл</em>
</div>


bash
#!/bin/bash
# Мой первый скрипт (hello.sh)

NAME=$(whoami)
DATE=$(date +"%d.%m.%Y %H:%M")
echo "Привет, $NAME! Сейчас $DATE"
echo "Ты находишься в: $(pwd)"
echo "Диск: $(df -h / | tail -1 | awk '{print $5}')"
bash
chmod +x hello.sh
./hello.sh

---


---

## 🎯 Практические задания

### Задание 1 — Навигация и файлы
bash
# Выполни все команды по порядку
pwd                          # где ты?
ls -la ~                     # что в домашней папке?
mkdir ~/my-course && cd ~/my-course
echo "Привет, Linux!" > hello.txt
cat hello.txt
cp hello.txt hello-copy.txt
ls -la
> ✅ Видишь два файла? Отлично!

### Задание 2 — Права доступа
bash
touch secret.txt
chmod 600 secret.txt          # только владелец читает/пишет
ls -la secret.txt             # -rw------- ?

touch script.sh
echo '#!/bin/bash
echo "Скрипт работает!"' > script.sh
chmod +x script.sh
./script.sh
> ✅ Скрипт выполнился? Права работают!

### Задание 3 — SSH ключ
bash
ssh-keygen -t ed25519 -C "moy-kurs" -f ~/.ssh/id_kurs
ls -la ~/.ssh/
cat ~/.ssh/id_kurs.pub        # это твой публичный ключ
```
> ✅ Два файла в ~/.ssh/: id_kurs и id_kurs.pub — готово!

## Урок 8 — Шпаргалка


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-commands-cheatsheet.jpg" alt="Шпаргалка по командам Linux" width="85%"/>
<br/><em>Шпаргалка по командам Linux: chmod, chown, пользователи и группы</em>
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


---

---

## 🧩 Быстрый тест — проверь себя

| Вопрос | Ответ |
|--------|-------|
| Что делает команда `pwd`? | Показывает текущую директорию (где ты находишься) |
| Что значит `chmod 755 script.sh`? | Владелец: rwx, группа: r-x, остальные: r-x |
| Чем `sudo` отличается от обычной команды? | Выполняется с правами суперпользователя root |
| Что такое SSH-ключ? | Пара файлов (приватный + публичный) для входа без пароля |
| Что делает `grep -r "текст" .`? | Ищет "текст" рекурсивно во всех файлах текущей папки |
| Как создать bash-скрипт и запустить его? | `touch script.sh`, `chmod +x script.sh`, `./script.sh` |

## 🧠 Чекпойнт понимания — обязательный

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/checkpoint.jpg" alt="Чекпойнт понимания" width="90%"/>
<br/><em>Три вопроса после каждого урока. Понимание важнее скорости.</em>
</div>

Прежде чем перейти к Модулю 2 — ответь себе вслух или письменно:

**1. Чем `chmod 755` отличается от `chmod 644`? Какие права даёт каждая?**

**2. Зачем Linux разделяет владельца, группу и остальных? Придумай реальный пример.**

**3. Что произойдёт если запустить `rm -rf /`? Почему это опасно?**

**4. Объясни SSH как метафору: что такое публичный ключ и приватный ключ — своими словами.**

> 💡 Если не можешь ответить на вопрос — вернись к соответствующему уроку. Понимание важнее скорости!

➡️ [Следующий модуль: Git →](../module2-git/)
