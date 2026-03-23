# ⚙️ Модуль 5 — Kubernetes (Уроки 14–20)

> **Цель:** понять, что такое Kubernetes, научиться развёртывать приложения в кластере, настраивать масштабирование и сервисы.

---

## 📖 Урок 14 — Что такое Kubernetes?

### 🧠 Объяснение

Docker — это один корабль с контейнерами. Но что если контейнеров **тысячи**, и они разбросаны по **сотням серверов**? Нужен **капитан флота** — и это Kubernetes!

**Kubernetes (k8s)** управляет множеством контейнеров:
- 🔄 **Автоматически перезапускает** упавшие контейнеры
- 📈 **Масштабирует** — добавляет серверы при нагрузке
- 🔀 **Балансирует трафик** между копиями приложения
- 🚢 **Обновляет** без простоя (rolling update)

### 🆚 Docker vs Kubernetes

| | Docker | Kubernetes |
|--|--|--|
| Масштаб | 1 сервер | 1–10 000 серверов |
| Управление | Вручную | Автоматически |
| Самовосстановление | Нет | Да |
| Балансировка | Нет | Встроена |
| Сложность | Просто | Сложнее |
| Когда нужен | Dev, малые проекты | Production, BigTech |

### 💻 Установка для практики (minikube)

```bash
# Устанавливаем kubectl — командная строка k8s
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/

# Устанавливаем minikube — локальный k8s кластер
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Запускаем кластер:
minikube start

# Проверяем:
kubectl get nodes
kubectl cluster-info
```

---

## 📖 Урок 15 — Основные объекты Kubernetes

### 📦 Pod — минимальная единица

Pod (стручок) — один или несколько контейнеров, работающих вместе.

```yaml
# pod.yaml
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

```bash
kubectl apply -f pod.yaml          # Создать
kubectl get pods                   # Посмотреть
kubectl describe pod мой-pod       # Подробности
kubectl logs мой-pod               # Логи
kubectl exec -it мой-pod -- sh     # Войти внутрь
kubectl delete pod мой-pod         # Удалить
```

### 🔄 Deployment — управляем Pod'ами

Deployment следит, чтобы всегда работало нужное число Pod'ов.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: мой-сайт
spec:
  replicas: 3                      # Хочу 3 копии
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
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

```bash
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get pods
kubectl rollout status deployment/мой-сайт
```

### 🌐 Service — открываем доступ

Service находит нужные Pod'ы и балансирует нагрузку между ними.

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: мой-сайт-svc
spec:
  selector:
    app: мой-сайт             # Найти Pod'ы с этим label
  ports:
  - port: 80
    targetPort: 80
  type: NodePort              # Доступен снаружи кластера
```

```bash
kubectl apply -f service.yaml
kubectl get services
minikube service мой-сайт-svc  # Открыть в браузере
```

---

## 📖 Урок 16 — Kubernetes самовосстановление

### 🧠 Объяснение

Одна из главных суперспособностей k8s — он **автоматически восстанавливает** упавшие контейнеры. Удали Pod — Deployment немедленно создаст новый!

```bash
# Запусти Deployment с 3 репликами:
kubectl apply -f deployment.yaml

# Посмотри на Pod'ы:
kubectl get pods

# Удали один Pod вручную:
kubectl delete pod ИМЯ-ПОДА-xxxxxxx

# Сразу смотри — Kubernetes создаёт новый:
kubectl get pods -w    # -w = watch (следить в реальном времени)
```

Kubernetes заметит, что Pod исчез, и немедленно запустит новый. Всегда будет 3 рабочих Pod'а!

---

## 📖 Урок 17 — Масштабирование

### 💻 Ручное масштабирование

```bash
# Изменить количество реплик:
kubectl scale deployment мой-сайт --replicas=5
kubectl get pods    # Теперь 5 Pod'ов

# Или через YAML — поменяй replicas: 3 на replicas: 5:
kubectl apply -f deployment.yaml
```

### 💻 Автомасштабирование (HPA)

```yaml
# hpa.yaml — автоматически добавляй Pod'ы при нагрузке
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: мой-сайт-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: мой-сайт
  minReplicas: 2             # Минимум 2 Pod'а
  maxReplicas: 10            # Максимум 10 Pod'ов
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70   # Масштабировать при CPU > 70%
```

```bash
kubectl apply -f hpa.yaml
kubectl get hpa
```

---

## 📖 Урок 18 — ConfigMap и Secret

### 💻 ConfigMap — конфигурация

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: настройки-приложения
data:
  APP_COLOR: blue
  APP_MODE: production
  DATABASE_HOST: postgres-service
```

### 💻 Secret — секреты (пароли)

```bash
# Создать Secret из командной строки:
kubectl create secret generic мои-секреты \
  --from-literal=DB_PASSWORD=МойПароль \
  --from-literal=API_KEY=abc123
```

### 💻 Использование в Deployment

```yaml
spec:
  containers:
  - name: app
    image: мой-образ:v1
    envFrom:
    - configMapRef:
        name: настройки-приложения    # Загрузить все переменные
    - secretRef:
        name: мои-секреты             # Загрузить все секреты
```

---

## 📖 Урок 19 — Rolling Update и откат

### 🚢 Обновление без простоя

Kubernetes обновляет Pod'ы по одному — пользователи не заметят!

```bash
# Обновить образ (новая версия):
kubectl set image deployment/мой-сайт веб=nginx:1.25

# Следить за процессом обновления:
kubectl rollout status deployment/мой-сайт

# Посмотреть историю обновлений:
kubectl rollout history deployment/мой-сайт
```

### 🔙 Откат к предыдущей версии

```bash
# Что-то пошло не так? Откат:
kubectl rollout undo deployment/мой-сайт

# Откат к конкретной версии:
kubectl rollout undo deployment/мой-сайт --to-revision=2
```

---

## 📖 Урок 20 — Итоговый проект на Kubernetes

### 💻 Полное приложение: сайт + база данных

**Структура файлов:**
```
k8s-проект/
├── deployment-web.yaml
├── deployment-db.yaml
├── service-web.yaml
├── service-db.yaml
├── configmap.yaml
└── secret.yaml
```

**configmap.yaml:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DB_HOST: postgres-svc
  DB_NAME: myapp
  DB_USER: appuser
```

**secret.yaml:**
```bash
kubectl create secret generic app-secret \
  --from-literal=DB_PASSWORD=СуперСекрет
```

**deployment-db.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        envFrom:
        - configMapRef:
            name: app-config
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: DB_PASSWORD
        volumeMounts:
        - name: pgdata
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: pgdata
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-svc
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
```

**deployment-web.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: веб
        image: nginx:alpine
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: webapp-svc
spec:
  selector:
    app: webapp
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
```

```bash
# Запускаем всё:
kubectl apply -f .

# Проверяем:
kubectl get all
minikube service webapp-svc
```

---

## 📋 Шпаргалка Модуля 5

| Команда | Что делает |
|---------|-----------|
| `kubectl get nodes` | Ноды кластера |
| `kubectl get pods` | Все Pod'ы |
| `kubectl get all` | Всё в namespace |
| `kubectl apply -f файл.yaml` | Создать/обновить объект |
| `kubectl delete -f файл.yaml` | Удалить объект |
| `kubectl describe pod имя` | Подробности о Pod |
| `kubectl logs имя` | Логи Pod |
| `kubectl exec -it имя -- sh` | Войти в Pod |
| `kubectl scale deployment имя --replicas=5` | Масштабировать |
| `kubectl rollout undo deployment имя` | Откатить |
| `kubectl get events` | События кластера |
| `minikube start/stop` | Запустить/остановить |
| `minikube dashboard` | Веб-интерфейс |
