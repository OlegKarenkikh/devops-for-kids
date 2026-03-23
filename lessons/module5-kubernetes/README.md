# ⚙️ Модуль 5 — Kubernetes (Уроки 24–28)

> **Цель:** научиться управлять множеством контейнеров в кластере.

---

## Урок 24 — Зачем Kubernetes?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-docker-vs-k8s.jpg" alt="Docker vs Kubernetes" width="85%"/>
<br/><em>Docker — один корабль. Kubernetes — флот с капитаном, который управляет тысячами кораблей.</em>
</div>

### 🧠 Простое объяснение

> Docker управляет одним контейнером. Kubernetes управляет **тысячами** контейнеров на **многих серверах**. Он как дирижёр оркестра.

| Docker | Kubernetes |
|--------|-----------|
| Один контейнер | Тысячи контейнеров |
| Один сервер | Много серверов (кластер) |
| Ручное управление | Автоматическое |
| Нет самовосстановления | Автоматически восстанавливает |
| Нет автомасштабирования | Масштабирует сам |

---

## Урок 25 — Архитектура кластера

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-cluster.jpg" alt="Кластер Kubernetes" width="85%"/>
<br/><em>Кластер = Control Plane (капитан) + Worker Nodes (рабочие корабли) + Pod'ы (контейнеры)</em>
</div>

### 🧠 Основные понятия

| Объект | Что это |
|--------|---------|
| **Кластер** | Группа серверов под управлением K8s |
| **Control Plane** | Мозг кластера (управляет всем) |
| **Node** | Сервер-рабочий (там запускаются Pod'ы) |
| **Pod** | Наименьшая единица (1+ контейнеров) |
| **Deployment** | Правило: сколько Pod'ов и каких |
| **Service** | Постоянный адрес для Pod'ов |

```bash
# Установить minikube (локальный K8s)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Запустить кластер
minikube start

# Проверить
kubectl get nodes               # Список нод
kubectl get pods -A             # Все Pod'ы
kubectl cluster-info            # Информация о кластере
```

---

## Урок 26 — Самовосстановление

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-self-healing.jpg" alt="Самовосстановление Kubernetes" width="85%"/>
<br/><em>Pod упал → Kubernetes мгновенно запускает новый. Сайт не останавливается!</em>
</div>

### 🧠 Простое объяснение

> Kubernetes никогда не спит. Если Pod упал — он сразу создаёт новый. Это называется **самовосстановление**.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: мой-сайт
spec:
  replicas: 3          # Всегда держать 3 копии
  selector:
    matchLabels:
      app: мой-сайт
  template:
    metadata:
      labels:
        app: мой-сайт
    spec:
      containers:
      - name: web
        image: nginx:latest
        ports:
        - containerPort: 80
```

```bash
kubectl apply -f deployment.yaml
kubectl get pods                    # 3 Pod'а запущены
kubectl get pods -w                 # Следить в реальном времени

# Удаляем Pod — K8s сразу создаст новый!
kubectl delete pod $(kubectl get pods -o name | head -1 | cut -d/ -f2)
kubectl get pods                    # Уже создаётся новый
```

---

## Урок 27 — Автомасштабирование HPA

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-autoscale.jpg" alt="Автомасштабирование HPA" width="85%"/>
<br/><em>Утром — 2 Pod'а, днём нагрузка выросла — K8s добавил Pod'ы, вечером нагрузка спала — убрал</em>
</div>

### 🧠 Простое объяснение

> HPA (Horizontal Pod Autoscaler) — автомасштабирование. Нагрузка выросла → K8s добавляет Pod'ы. Нагрузка упала → убирает лишние.

```bash
# Создать HPA
kubectl autoscale deployment мой-сайт --min=2 --max=10 --cpu-percent=70

# Посмотреть статус
kubectl get hpa
kubectl describe hpa мой-сайт
```

---

## Урок 28 — Rolling Update: обновление без остановки

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-rolling-update.jpg" alt="Rolling update без простоя" width="85%"/>
<br/><em>Обновление поочерёдно: старые Pod'ы заменяются новыми по одному. Сайт работает всё время!</em>
</div>

### 🧠 Простое объяснение

> Rolling Update заменяет Pod'ы по одному, не останавливая сайт. Пользователи не замечают обновления.

```bash
# Обновить образ (деплой новой версии)
kubectl set image deployment/мой-сайт web=nginx:1.25

# Следить за обновлением
kubectl rollout status deployment/мой-сайт

# История обновлений
kubectl rollout history deployment/мой-сайт

# Откат если что-то пошло не так
kubectl rollout undo deployment/мой-сайт
kubectl rollout undo deployment/мой-сайт --to-revision=1
```

---

## 📋 Шпаргалка Модуля 5

| Команда | Что делает |
|---------|------------|
| `kubectl get nodes` | Ноды кластера |
| `kubectl get pods` | Pod'ы в namespace |
| `kubectl apply -f файл.yaml` | Применить конфигурацию |
| `kubectl delete -f файл.yaml` | Удалить ресурсы |
| `kubectl logs имя-пода` | Логи Pod'а |
| `kubectl exec -it имя-пода -- bash` | Войти в Pod |
| `kubectl describe pod имя` | Подробности о Pod |
| `kubectl rollout status deployment/имя` | Статус обновления |
| `kubectl rollout undo deployment/имя` | Откат обновления |
| `kubectl autoscale deployment имя --min=2 --max=10` | Автомасштабирование |

---

## 🎓 Итоговый проект курса

```bash
# Финальный стек: Python + PostgreSQL + Redis + Prometheus + Grafana + K8s HPA
# Полные файлы в папке projects/

cd projects/
cat README.md    # Инструкции по запуску
```

🎉 **Поздравляем!** Ты прошёл путь от терминала до Kubernetes!
