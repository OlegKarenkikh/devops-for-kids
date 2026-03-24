<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/course-roadmap.jpg" alt="DevOps для детей" width="100%"/>

# 🐧🐳⚙️ DevOps для детей и начинающих

> **Полный курс от терминала до Kubernetes** — простым языком, с иллюстрациями и задачами в терминале Linux.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Lessons](https://img.shields.io/badge/уроков-35-blue)](#️-карта-курса-35-уроков)
[![Language](https://img.shields.io/badge/язык-Русский-red)](README.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## 🗺️ Начни здесь — Вводный модуль

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/intro_full_architecture.jpg" alt="Полная архитектура системы" width="90%"/>
<br/><em>Ты построишь именно такую систему — от нуля до продакшена</em>
</div>

**[📖 Модуль 0: Вводный — зачем это всё и как устроен мир →](lessons/module0-intro/)**

Прочитай этот модуль первым, прежде чем запускать первую команду. Здесь объясняется:
- Как работает любое приложение (три слоя)
- Что такое DevOps Pipeline и зачем он нужен
- Полный глоссарий всех терминов курса с простыми метафорами
- Как читать YAML, ENV, JSON файлы
- Порты, переменные окружения, файловая система Linux
- Психология обучения: как не бросить

---

## 🗺️ Карта курса (35 уроков)

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/overview-roadmap.jpg" alt="Карта курса" width="900"/>
<br/><em>Путь от нуля до Kubernetes — 6 модулей, 35 уроков, 1 финальный проект</em>
</div>

| # | Модуль | Уроки | Что изучаем |
|---|--------|-------|------------|
| 0 | 📖 [Введение](lessons/module0-intro/) | — | Как всё устроено, глоссарий, психология обучения |
| 1 | 🐧 [Терминал и Linux](lessons/module1-terminal/) | 1–8 | Команды, файлы, chmod, SSH, bash-скрипты |
| 2 | 🌿 [Git и GitHub](lessons/module2-git/) | 9–11 | Версии кода, ветки, SSH-ключи |
| 3 | 🐳 [Docker](lessons/module3-docker/) | 12–18 | Контейнеры, Dockerfile, exec, volumes |
| 4 | 🎼 [Compose + Мониторинг](lessons/module4-compose/) | 19–23 | Docker Compose, Prometheus, Grafana |
| 5 | ⚙️ [Kubernetes](lessons/module5-kubernetes/) | 24–28 | Pod, Deployment, Service, HPA |
| 6 | 🔐 [Секреты и REST API](lessons/module6-secrets-api/) | 29–35 | .env, Flask API, Kubernetes Secrets |
| ⭐ | [Бонус](lessons/module-bonus/) | — | GPU, AI, HTTPS, Telegram-бот, FastAPI |

➡️ **[🏆 Итоговый проект — «Моя Коллекция»](projects/final-project/)**

---

## 🚀 Быстрый старт

```bash
# Убедись что терминал работает:
whoami
```

**[👉 Начать с Урока 1 →](lessons/module1-terminal/)**  
**[📚 Шпаргалки по всем темам →](cheatsheets/)**  
**[🤝 Как помочь проекту →](CONTRIBUTING.md)**

---

## 🏗️ Структура репозитория

```
devops-for-kids/
├── lessons/
│   ├── module0-intro/         # Введение и глоссарий
│   ├── module1-terminal/      # Уроки 1–8 + 🎯 задания
│   ├── module2-git/           # Уроки 9–11 + 🎯 задания
│   ├── module3-docker/        # Уроки 12–18 + 🎯 задания
│   ├── module4-compose/       # Уроки 19–23 + 🎯 задания
│   ├── module5-kubernetes/    # Уроки 24–28 + 🎯 задания
│   ├── module6-secrets-api/   # Уроки 29–35 + 🎯 задания
│   └── module-bonus/          # GPU, AI, Nginx, Telegram-бот
├── projects/
│   └── final-project/         # 🏆 Flask + PostgreSQL + K8s
├── cheatsheets/               # Шпаргалки по всем темам
├── images/                    # Иллюстрации (PNG + JPEG)
├── CONTRIBUTING.md            # Как внести вклад
└── README.md
```

---

## 📖 Полезные ресурсы

| Ресурс | Что делает |
|--------|-----------|
| [play-with-docker.com](https://play-with-docker.com) | Docker прямо в браузере, без установки |
| [killercoda.com](https://killercoda.com) | Kubernetes в браузере |
| [learngitbranching.js.org](https://learngitbranching.js.org) | Визуальное изучение Git |
| [labs.play-with-k8s.com](https://labs.play-with-k8s.com) | Kubernetes playground |

---

<div align="center">MIT License · Используй свободно, учи других! 🚀</div>
