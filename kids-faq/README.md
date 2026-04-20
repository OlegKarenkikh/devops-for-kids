# ❓ Детский FAQ — 48 вопросов без страха

> Здесь собраны вопросы, которые боятся задать вслух. Нет глупых вопросов — есть неотвеченные!

**Быстрая навигация:** [Терминал](#терминал) · [Git](#git) · [Docker](#docker) · [Kubernetes](#kubernetes) · [Secrets & API](#secrets--api) · [Карьера](#карьера)

---

## Терминал

→ *Эти вопросы подробно разобраны в [Модуле 1 — Терминал](../lessons/module1-terminal/)*

<details>
<summary><b>Зачем вообще нужен терминал, если есть мышь?</b></summary>

Терминал быстрее, точнее и автоматизируем. То, что мышью занимает минуту (найти файл → открыть → изменить → сохранить), в терминале: `sed -i 's/старое/новое/g' файл`. Плюс серверы часто вообще без экрана — только терминал.

</details>

<details>
<summary><b>Что будет если ввести неправильную команду?</b></summary>

Обычно — просто ошибка и ничего страшного. Опасны только команды с `sudo`, `rm -rf`, `dd` — они могут удалить данные без корзины. Правило: не копируй команды из интернета не понимая что они делают.

</details>

<details>
<summary><b>Почему у команды cd нет вывода?</b></summary>

По философии Unix: «молчание = успех». Если команда отработала без ошибок — она молчит. Только при ошибке выводит сообщение.

</details>

<details>
<summary><b>Ctrl+C убивает процесс или копирует?</b></summary>

В терминале **Ctrl+C** = прервать процесс (SIGINT). Для копирования используй **Ctrl+Shift+C** (Linux) или **Cmd+C** (Mac).

</details>

---

## Git

→ *Эти вопросы подробно разобраны в [Модуле 2 — Git](../lessons/module2-git/)*

<details>
<summary><b>Зачем делать commit если можно просто сохранить файл?</b></summary>

Commit — это не просто сохранение. Это «снимок» всего проекта с описанием что изменилось и почему. Через месяц ты сможешь вернуться к любому моменту и понять что происходило.

</details>

<details>
<summary><b>Что делать если закоммитил секрет/пароль?</b></summary>

1. Немедленно смени пароль/токен на сайте
2. `git rebase -i` или `git filter-branch` чтобы удалить из истории
3. Force push: `git push --force`
4. Убедись что `.gitignore` защищает `.env`

Считай что секрет уже утёк — меняй в любом случае.

</details>

<details>
<summary><b>Можно ли работать с Git без GitHub?</b></summary>

Да! Git работает полностью локально. GitHub — это просто удалённое хранилище. Альтернативы: GitLab, Gitea, Forgejo, или просто папка на другом компьютере.

</details>

<details>
<summary><b>Что такое HEAD в Git?</b></summary>

HEAD — указатель на текущий коммит (где ты находишься сейчас). Обычно совпадает с верхушкой ветки. `git log` показывает `HEAD → main`.

</details>

---

## Docker

→ *Эти вопросы подробно разобраны в [Модуле 3 — Docker](../lessons/module3-docker/)*

<details>
<summary><b>Docker — это виртуальная машина?</b></summary>

Нет, хотя похоже. Виртуальная машина (VMware, VirtualBox) копирует целый компьютер включая ядро ОС — тяжело (гигабайты RAM). Docker делит ядро Linux с хостом — лёгкий (мегабайты RAM, секунды запуска).

</details>

<details>
<summary><b>Почему docker pull качает «слои»?</b></summary>

Image состоит из слоёв — каждая команда Dockerfile создаёт слой. Слои переиспользуются: если у тебя уже есть `ubuntu:22.04` слой, Docker не скачает его снова для другого image.

</details>

<details>
<summary><b>Что значит «container exited with code 1»?</b></summary>

Контейнер завершился с ошибкой. Смотри логи: `docker logs имя_контейнера`. Exit code 1 = общая ошибка, 137 = убит (OOM или kill), 127 = команда не найдена.

</details>

<details>
<summary><b>Как войти в запущенный контейнер?</b></summary>

```bash
docker exec -it имя_контейнера bash   # если есть bash
docker exec -it имя_контейнера sh     # если только sh (Alpine)
```

</details>

---

## Kubernetes

→ *Эти вопросы подробно разобраны в [Модуле 5 — Kubernetes](../lessons/module5-kubernetes/)*

<details>
<summary><b>Kubernetes нужен только большим компаниям?</b></summary>

Нет. Миникластер для разработки: `minikube start` — работает на ноутбуке с 4GB RAM. Kubernetes учат для понимания современного DevOps, даже если работаешь в маленькой команде.

</details>

<details>
<summary><b>Чем Service отличается от Pod?</b></summary>

Pod — временный, IP меняется при перезапуске. Service — постоянная точка входа с фиксированным именем/IP, которая направляет трафик на нужные Pod. Как DNS-имя для группы Pod.

</details>

<details>
<summary><b>Что такое namespace в Kubernetes?</b></summary>

Namespace — логическое разделение кластера. Как папки в файловой системе. `default` — для твоих приложений, `kube-system` — системные компоненты. Разные команды могут работать в разных namespace изолированно.

</details>

<details>
<summary><b>Почему Pod не запускается (Pending)?</b></summary>

Причины: не хватает ресурсов (CPU/RAM), нет подходящего Node, PVC не создан. Диагностика:
```bash
kubectl describe pod имя-pod
kubectl get events --sort-by='.lastTimestamp'
```

</details>

---

## Secrets & API

→ *Эти вопросы подробно разобраны в [Модуле 6 — Secrets & API](../lessons/module6-secrets-api/)*

<details>
<summary><b>Чем .env отличается от Kubernetes Secret?</b></summary>

| | .env | K8s Secret |
|---|---|---|
| Где | Локально на компьютере | В кластере Kubernetes |
| Шифрование | Нет (plain text) | Base64 (не настоящее шифрование!) |
| Для прода | Не рекомендуется | Лучше + можно добавить Vault |

</details>

<details>
<summary><b>Что такое curl и зачем он нужен?</b></summary>

`curl` — инструмент для HTTP-запросов из терминала. Тестировать API, скачивать файлы, отправлять данные:
```bash
curl https://api.github.com/users/OlegKarenkikh
curl -X POST -H "Content-Type: application/json" -d '{"key":"val"}' http://localhost:8080/api
```

</details>

<details>
<summary><b>HTTP 200, 404, 500 — что означают коды?</b></summary>

| Код | Значение |
|-----|---------|
| 200 | OK — всё хорошо |
| 201 | Created — создано |
| 400 | Bad Request — ошибка в запросе |
| 401 | Unauthorized — нужна авторизация |
| 403 | Forbidden — нет прав |
| 404 | Not Found — не найдено |
| 500 | Server Error — ошибка сервера |

</details>

---

## Карьера

<details>
<summary><b>С чего начать если хочу стать DevOps инженером?</b></summary>

1. Linux (этот курс — Модуль 1)
2. Git (Модуль 2)
3. Docker (Модуль 3)
4. CI/CD (Модуль 4)
5. Kubernetes (Модуль 5)
6. Облака (AWS/GCP/YC)
7. Мониторинг (Prometheus/Grafana)

Параллельно: пиши скрипты на Python/Bash, делай реальные проекты.

</details>

<details>
<summary><b>Нужно ли знать программирование чтобы стать DevOps?</b></summary>

Да, базово. Нужны: Bash (автоматизация), Python (скрипты, ansible), YAML (конфиги). Не нужны: сложные алгоритмы, фреймворки. DevOps = infrastructure as code, а не разработка продукта.

</details>

<details>
<summary><b>Сколько времени нужно чтобы выучить DevOps?</b></summary>

До первой junior-позиции: **6–12 месяцев** при ежедневной практике по 1–2 часа. Этот курс (~20 часов) — хорошая основа. Дальше: pet-проекты, open source, облачные сертификаты (CKA, AWS).

</details>

---

> 💬 Не нашёл ответ? [Открой issue](https://github.com/OlegKarenkikh/devops-for-kids/issues) — добавим в FAQ!
>
> ← Вернуться к [содержанию курса](../README.md)
