# ⚙️ Модуль 5 — Kubernetes (Уроки 14–20)

> **Цель:** управлять множеством контейнеров в production — масштабирование, самовосстановление, обновления без простоя.

---

## 📖 Урок 14 — Что такое Kubernetes?

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-docker-vs-k8s.png" alt="Docker vs Kubernetes" width="85%"/>
<br/><em>Docker — один корабль с контейнерами. Kubernetes — капитан, управляющий целым флотом</em>
</div>

### 🧠 Объяснение

Docker отлично справляется с одним сервером. Но что если серверов **сотни**, а контейнеров **тысячи**? Нужен **капитан флота** — это **Kubernetes (k8s)**.

### 🆚 Docker vs Kubernetes

| | Docker | Kubernetes |
|--|--|--|
| Масштаб | 1 сервер | 1–10 000 серверов |
| Управление | Вручную | Автоматически |
| Самовосстановление | Нет | ✅ Да |
| Балансировка трафика | Нет | ✅ Встроена |
| Rolling updates | Нет | ✅ Да |
| Сложность | Просто | Сложнее |

### 💻 Установка minikube

```bash
# kubectl — командная строка k8s
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/

# minikube — локальный кластер
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

minikube start
kubectl get nodes
```

---

## 📖 Урок 15 — Архитектура кластера

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-cluster.png" alt="Архитектура кластера Kubernetes" width="85%"/>
<br/><em>Control Plane = мозг кластера, Nodes = рабочие лошадки, Pods = контейнеры на нодах</em>
</div>

### 📦 Главные объекты Kubernetes

**Pod** — минимальная единица, один или несколько контейнеров:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: мой-pod
  labels:
    app: мой-сайт
spec:
  containers:
  - name: веб
    image: nginx:alpine
    ports:
    - containerPort: 80
```

**Deployment** — управляет репликами Pod'ов:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: мой-сайт
spec:
  replicas: 3
  selector:
    matchLabels:
      app: мой-сайт
  template:
    metadata:
      labels:
        app: мой-сайт
    spec:
      containers:
      - name: веб
        image: nginx:alpine
        ports:
        - containerPort: 80
```

**Service** — находит Pod'ы и балансирует трафик:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: мой-сайт-svc
spec:
  selector:
    app: мой-сайт
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
```

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get all
minikube service мой-сайт-svc
```

---

## 📖 Урок 16 — Самовосстановление

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-self-healing.png" alt="Kubernetes самовосстановление" width="80%"/>
<br/><em>Упал Pod → Kubernetes заметил → создал новый. Всегда работает нужное число реплик!</em>
</div>

```bash
kubectl get pods -w    # Следим в реальном времени
# В другом терминале:
kubectl delete pod ИМЯ-ПОДА
# Смотри: Kubernetes немедленно создаёт новый!
```

---

## 📖 Урок 17 — Масштабирование

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-autoscale.png" alt="Автомасштабирование Kubernetes" width="80%"/>
<br/><em>Растёт трафик → HPA добавляет Pod'ы. Падает → убирает лишние. Автоматически!</em>
</div>

```bash
# Ручное масштабирование:
kubectl scale deployment мой-сайт --replicas=5
kubectl get pods

# Автомасштабирование (HPA):
kubectl autoscale deployment мой-сайт --min=2 --max=10 --cpu-percent=70
kubectl get hpa
```

---

## 📖 Урок 18 — Объекты: Service, Ingress, ConfigMap, Secret

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-objects.png" alt="Объекты Kubernetes: Deployment, Service, Ingress" width="85%"/>
<br/><em>Deployment = кухня, Service = официант, Ingress = входная дверь для внешнего трафика</em>
</div>

```bash
# ConfigMap — конфигурация
kubectl create configmap app-config --from-literal=APP_MODE=production

# Secret — пароли и ключи
kubectl create secret generic app-secret --from-literal=DB_PASSWORD=СуперСекрет

# Ingress — внешний доступ через домен
# Требует ingress controller (nginx-ingress)
```

---

## 📖 Урок 19 — Rolling Update и откат

```bash
# Обновить версию образа:
kubectl set image deployment/мой-сайт веб=nginx:1.25

# Следить за обновлением:
kubectl rollout status deployment/мой-сайт

# История обновлений:
kubectl rollout history deployment/мой-сайт

# Откат (что-то пошло не так):
kubectl rollout undo deployment/мой-сайт
```

---

## 📖 Урок 20 — Итоговый проект

```bash
mkdir k8s-проект && cd k8s-проект

# Создаём все манифесты:
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment-db.yaml
kubectl apply -f deployment-web.yaml

# Проверяем:
kubectl get all
kubectl get events

# Открываем в браузере:
minikube service webapp-svc

# Масштабируем:
kubectl scale deployment webapp --replicas=5

# Обновляем:
kubectl set image deployment/webapp веб=nginx:1.25
kubectl rollout status deployment/webapp
```

---

## 📋 Шпаргалка Модуля 5

| Команда | Что делает |
|---------|-----------|
| `kubectl get all` | Всё в namespace |
| `kubectl apply -f файл.yaml` | Создать/обновить |
| `kubectl delete -f файл.yaml` | Удалить |
| `kubectl describe pod имя` | Подробности |
| `kubectl logs имя` | Логи Pod |
| `kubectl exec -it имя -- sh` | Войти в Pod |
| `kubectl scale deployment имя --replicas=5` | Масштаб |
| `kubectl rollout undo deployment имя` | Откат |
| `kubectl get events` | События |
| `minikube dashboard` | Веб-интерфейс |

---

## 🏆 Поздравляем! Ты прошёл весь курс

```
🐧 Терминал  →  🌿 Git  →  🐳 Docker  →  🎼 Compose  →  ⚙️ Kubernetes
     ✅              ✅          ✅              ✅              ✅
```

➡️ [Итоговые проекты](../../projects/)
