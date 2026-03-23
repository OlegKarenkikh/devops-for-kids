# 🐧 Модуль 1 — Терминал и Linux (Уроки 1–8)

> **Цель:** освоить терминал, управление файлами, пользователями, правами доступа и безопасным входом по SSH.

---

## Урок 1 — Что такое терминал?

Представь, что твой компьютер — умный пёс. Обычно командуешь ему мышкой. Но **терминал** — способ говорить с ним текстом.

```bash
whoami        # Кто я?
pwd           # Где я?
date          # Который час?
uname -a      # Информация о системе
```

> 💡 Если ошибся — нажми `Ctrl+C`. Это кнопка «Стоп».

---

## Уроки 2–3 — Файлы и навигация

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-commands-cheatsheet.jpg" alt="Шпаргалка команд" width="80%"/>
<br/><em>Четыре главные операции с файлами и папками</em>
</div>

```bash
ls / ls -la           # Список файлов (с деталями)
cd Documents / cd ..  # Войти / выйти из папки
cd ~                  # Домой
mkdir мой-проект      # Создать папку
touch файл.txt        # Создать файл
echo "Привет" > f.txt # Записать текст
cat файл.txt          # Прочитать
cp от куда            # Скопировать
mv от куда            # Переместить
rm файл.txt           # Удалить ⚠️ (без корзины!)
```

### 🧪 Задание 2

```bash
mkdir урок2 && cd урок2
for fruit in яблоко банан манго апельсин; do
  echo "$fruit" >> фрукты.txt
done
cat фрукты.txt
grep "банан" фрукты.txt
wc -l фрукты.txt
```

---

## Урок 4 — Права доступа (chmod)

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-permissions.jpg" alt="Права доступа" width="80%"/>
<br/><em>Три группы: ты (owner), твоя группа, все остальные</em>
</div>

```
-rw-r--r-- 1 ivan devs 42 файл.txt
 ↑↑↑ └───── остальные: только читать
 ││└─────── группа: только читать
 │└──────── владелец: читать + писать
 └───────── тип: - файл, d папка, l ссылка
```

| Число | Права | Смысл |
|-------|-------|-------|
| 7 | rwx | всё |
| 6 | rw- | читать + писать |
| 5 | r-x | читать + запускать |
| 4 | r-- | только читать |
| 0 | --- | ничего |

```bash
chmod +x скрипт.sh       # Добавить право запуска
chmod 644 файл.txt       # rw-r--r-- (стандарт)
chmod 755 скрипт.sh      # rwxr-xr-x (исполняемый)
chmod 600 секрет.txt     # rw------- (только ты)
chmod 700 личная/        # rwx------ (закрытая папка)
```

---

## Урок 5 — Владелец файла: chown

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-chown.jpg" alt="chown — кому принадлежит файл" width="80%"/>
<br/><em>chown меняет «именной ярлык» файла — кто владелец и какая группа</em>
</div>

### 🧠 Объяснение

> Каждый файл в Linux имеет **хозяина** — как у вещи в шкафу. `chown` меняет хозяина.

```bash
ls -la файл.txt           # Посмотреть владельца
chown ivan файл.txt       # Новый владелец: ivan
chown ivan:devs файл.txt  # Владелец ivan, группа devs
chown :devs файл.txt      # Только группу
chown -R ivan папка/      # Всё внутри папки (рекурсивно)
sudo chown root:root /etc/важный.conf  # Системный файл
```

### 📊 Разница chmod vs chown

| Команда | Меняет | Пример |
|---------|--------|--------|
| `chmod` | **Права** (что можно делать) | `chmod 644 f.txt` |
| `chown` | **Владельца** (кому принадлежит) | `chown ivan f.txt` |

### 🧪 Задание 5

```bash
touch мой-файл.txt
ls -la мой-файл.txt           # Посмотри владельца
sudo useradd тест || true
sudo chown тест мой-файл.txt
ls -la мой-файл.txt           # Что изменилось?
sudo chown $USER мой-файл.txt # Вернуть себе
```

---

## Урок 6 — Пользователи и группы

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-users-groups.jpg" alt="Пользователи и группы" width="80%"/>
<br/><em>Пользователи — это студенты, группы — кружки в школе. Один студент в нескольких кружках!</em>
</div>

### 🧠 Зачем несколько пользователей?

На реальном сервере работает много людей и программ. Каждый должен видеть только **своё** — как отдельные комнаты в общежитии.

```bash
# Создание пользователя
sudo adduser alice          # Интерактивно (Ubuntu)
sudo useradd -m -s /bin/bash bob  # Вручную (все дистрибутивы)
sudo passwd bob             # Установить пароль

# Информация о пользователях
id                          # Твой UID, GID, группы
id alice                    # Информация о alice
whoami                      # Имя текущего пользователя
who                         # Кто сейчас в системе
last                        # История входов
cat /etc/passwd             # Все пользователи системы

# Переключение
su - alice                  # Стать alice (нужен пароль)
sudo su -                   # Стать root
exit                        # Выйти обратно
```

### Группы

```bash
# Создание и управление группами
sudo addgroup developers
sudo groupadd sysadmins     # Альтернатива

# Добавить пользователя в группу
sudo usermod -aG developers alice   # -a = добавить, G = группа
sudo usermod -aG docker alice       # Дать доступ к Docker
sudo gpasswd -a bob developers      # Альтернатива

# Просмотр групп
groups                      # Твои группы
groups alice                # Группы alice
cat /etc/group              # Все группы системы

# Удаление
sudo userdel -r alice       # Удалить пользователя + домашнюю папку
sudo groupdel developers    # Удалить группу
```

### 🧪 Задание 6

```bash
sudo adduser студент
sudo addgroup класс
sudo usermod -aG класс студент
groups студент              # Проверить
mkdir /tmp/проект
sudo chown студент:класс /tmp/проект
sudo chmod 770 /tmp/проект
ls -la /tmp/ | grep проект
```

---

## Урок 7 — SSH: безопасный вход на сервер

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module1-ssh-keys.jpg" alt="SSH ключи — вход без пароля" width="80%"/>
<br/><em>Пароль = шёпот на ухо (можно подслушать). SSH-ключ = уникальный замок+ключ (нельзя угадать)</em>
</div>

### 🧠 Что такое SSH?

SSH (Secure Shell) — зашифрованный туннель между твоим компьютером и сервером. Всё что ты пишешь — **зашифровано**.

```bash
# Подключение по паролю (базовый способ)
ssh username@192.168.1.100
ssh username@server.example.com
ssh -p 2222 username@server.com   # Нестандартный порт

# Базовые команды SSH
ssh user@host "ls -la"            # Выполнить команду без входа
ssh user@host "cat /etc/os-release"
scp файл.txt user@host:~/         # Скопировать файл на сервер
scp -r папка/ user@host:~/        # Скопировать папку
```

### SSH-ключи — вход без пароля

```bash
# ШАГ 1: Создать пару ключей (на СВОЁМ компьютере)
ssh-keygen -t ed25519 -C "мой-сервер"
# Создаст:
# ~/.ssh/id_ed25519      ← ПРИВАТНЫЙ КЛЮЧ (никому не давать!)
# ~/.ssh/id_ed25519.pub  ← Публичный ключ (можно везде)

# ШАГ 2: Отправить публичный ключ на сервер
ssh-copy-id username@server.com
# ИЛИ вручную:
cat ~/.ssh/id_ed25519.pub | ssh user@host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# ШАГ 3: Войти без пароля!
ssh username@server.com   # 🎉 Не спрашивает пароль!
```

### Конфигурация ~/.ssh/config

```
# ~/.ssh/config — псевдонимы для серверов
Host мой-сервер
    HostName 192.168.1.100
    User ivan
    IdentityFile ~/.ssh/id_ed25519
    Port 22

Host github
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

```bash
ssh мой-сервер   # Теперь так вместо длинной команды!
```

### Безопасность SSH

```bash
# Запретить вход root по паролю (на сервере):
sudo nano /etc/ssh/sshd_config
# Изменить: PermitRootLogin no
#           PasswordAuthentication no
#           PubkeyAuthentication yes
sudo systemctl restart sshd

# Просмотр попыток входа:
sudo cat /var/log/auth.log | grep "Failed password"
sudo journalctl -u ssh -n 50
```

### 🧪 Задание 7

```bash
# На своём компьютере:
ssh-keygen -t ed25519 -f ~/.ssh/учебный
cat ~/.ssh/учебный.pub   # Это твой публичный ключ
ls -la ~/.ssh/           # Посмотри файлы
```

---

## Урок 8 — Bash-скрипты: автоматизируем работу

```bash
#!/bin/bash
# мой-скрипт.sh — информация о системе

echo "=== Система ==="
echo "Пользователь: $(whoami)"
echo "Хост: $(hostname)"
echo "ОС: $(uname -s -r)"
echo ""
echo "=== Диск ==="
df -h / | tail -1
echo ""
echo "=== Память ==="
free -h | grep Mem
echo ""
echo "=== Загрузка ==="
uptime
```

```bash
chmod +x мой-скрипт.sh
./мой-скрипт.sh
```

### Переменные и условия

```bash
#!/bin/bash
ИМЯ="Alice"
ВОЗРАСТ=10

echo "Привет, $ИМЯ! Тебе $ВОЗРАСТ лет."

if [ $ВОЗРАСТ -ge 18 ]; then
    echo "Ты взрослый!"
else
    echo "Ты ещё ребёнок 🧒"
fi

# Цикл
for ЧИСЛО in 1 2 3 4 5; do
    echo "Число: $ЧИСЛО"
done
```

---

## 📋 Шпаргалка Модуля 1

| Тема | Команда | Что делает |
|------|---------|-----------|
| Навигация | `pwd / ls / cd` | Где я, что здесь, перейти |
| Файлы | `touch / cp / mv / rm` | Создать, копировать, переместить, удалить |
| Права | `chmod 755 файл` | Изменить права доступа |
| Владелец | `chown user:group файл` | Изменить владельца |
| Пользователи | `adduser / usermod -aG` | Создать, добавить в группу |
| Группы | `addgroup / groups` | Создать, просмотреть |
| SSH вход | `ssh user@host` | Подключиться к серверу |
| SSH ключи | `ssh-keygen / ssh-copy-id` | Создать / отправить ключ |
| Скрипты | `chmod +x / ./скрипт.sh` | Сделать исполняемым / запустить |

➡️ [Следующий модуль: Git →](../module2-git/)
