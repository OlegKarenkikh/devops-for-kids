# 📋 Полная шпаргалка: Терминал, Git, Docker, Kubernetes

> **🎯 Цель:** быстро найти нужную команду не гугля. Открой, скопируй, запусти.


## 🐧 Linux / Bash

```bash
pwd                        # Текущая папка
ls -la                     # Все файлы с правами
cd папка / cd .. / cd ~   # Навигация
mkdir имя                  # Создать папку
touch файл.txt             # Создать файл
cat / head -n5 / tail -n5  # Читать файл
echo "текст" > файл        # Записать
echo "текст" >> файл       # Добавить
cp от куда                 # Копировать
mv от куда                 # Переместить/переименовать
rm файл / rm -rf папка/    # Удалить ⚠️
grep "слово" файл          # Найти в файле
find . -name "*.txt"       # Найти файлы
chmod +x файл              # Право запуска
chmod 644 / 755 / 600      # Установить права
sudo команда               # От администратора
```

## 🌿 Git

```bash
git init                           # Начать репозиторий
git status                         # Что изменилось
git add . / git add файл           # Добавить к коммиту
git commit -m "Текст"             # Сохранить
git log --oneline                  # История
git diff                           # Разница
git branch / git branch имя        # Ветки
git checkout имя                   # Переключиться
git checkout -b новая-ветка        # Создать и переключиться
git merge имя                      # Слить ветку
git remote add origin URL          # Привязать GitHub
git push / git push -u origin main # Отправить
git pull                           # Получить
git clone URL                      # Скачать
git stash / git stash pop          # Спрятать/достать
git reset --hard HEAD~1            # Откатить коммит ⚠️
```

## 🐳 Docker

```bash
docker images                       # Образы
docker pull имя:тег                 # Скачать образ
docker build -t имя:тег .           # Собрать из Dockerfile
docker push имя:тег                 # Отправить в реестр
docker rmi имя                      # Удалить образ

docker ps / docker ps -a            # Контейнеры
docker run -d -p 8080:80 имя        # Запустить в фоне
docker run -it имя bash             # Войти внутрь
docker run --rm имя                 # Удалить после остановки
docker stop / start / restart имя  # Управление
docker rm имя                       # Удалить контейнер
docker logs -f имя                  # Следить за логами
docker exec -it имя bash            # Терминал внутри
docker stats                        # Нагрузка
docker inspect имя                  # Полная инфо
docker system prune                 # Очистить лишнее

docker login                        # Войти в Docker Hub
```

## 🎼 Docker Compose

```bash
docker compose up -d                # Запустить все
docker compose ps                   # Статус
docker compose logs -f              # Следить за логами
docker compose stop                 # Остановить
docker compose down                 # Удалить контейнеры
docker compose down -v              # + удалить тома
docker compose build                # Пересобрать
docker compose exec сервис bash     # Войти в сервис
docker compose pull                 # Обновить образы
```

## ⚙️ Kubernetes (kubectl)

```bash
kubectl get nodes                           # Ноды
kubectl get pods / get pods -A             # Pod'ы
kubectl get deployments / services / all   # Объекты
kubectl apply -f файл.yaml                 # Создать/обновить
kubectl delete -f файл.yaml               # Удалить
kubectl describe pod имя                   # Подробности
kubectl logs имя / logs -f имя            # Логи
kubectl exec -it имя -- sh                 # Войти в Pod
kubectl scale deployment имя --replicas=5  # Масштаб
kubectl rollout status deployment/имя      # Статус обновления
kubectl rollout undo deployment/имя        # Откат
kubectl rollout history deployment/имя     # История
kubectl get events                         # События
kubectl create secret generic имя --from-literal=KEY=VAL  # Секрет
kubectl create configmap имя --from-literal=KEY=VAL       # Конфиг

# minikube:
minikube start / stop                       # Кластер
minikube dashboard                          # Веб-интерфейс
minikube service имя                        # Открыть сервис
```

---

## 🔢 Права доступа chmod

| Число | Символ | Значение |
|-------|--------|---------|
| 7 | rwx | Читать + писать + запускать |
| 6 | rw- | Читать + писать |
| 5 | r-x | Читать + запускать |
| 4 | r-- | Только читать |
| 0 | --- | Нет прав |

**Часто используемые:**
- `644` → владелец rw-, остальные r-- (обычные файлы)
- `755` → владелец rwx, остальные r-x (исполняемые)
- `600` → владелец rw-, остальные --- (секреты)
- `777` → все rwx (⚠️ небезопасно!)

---

## 🎯 Быстрая самопроверка

Открой терминал и выполни — всё должно работать без ошибок:

```bash
# Linux & Git
pwd && ls -la && git --version

# Docker
docker --version && docker run hello-world

# Kubernetes (если установлен)
kubectl version --client

# Python
python3 --version && python3 -c "print('Всё работает!')"
```

