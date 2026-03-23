# ⚙️ Модуль 5 — Kubernetes (Уроки 24–28)

> **Цель:** понять зачем нужен Kubernetes, запустить первый кластер и научиться работать с Pod, Deployment, Service.

---

## Урок 24 — Docker vs Kubernetes

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-docker-vs-k8s.jpg" alt="Docker один корабль, Kubernetes флот" width="85%"/>
<br/><em>Docker — один корабль. Kubernetes — целый флот с капитаном. Нужно много контейнеров? Kubernetes!</em>
</div>

### 🧠 Когда нужен Kubernetes?

| | Docker | Kubernetes |
|---|--------|-----------|
| Контейнеров | 1–10 | 10–10 000 |
| Автоперезапуск | Нет | ✅ |
| Автомасштаб | Нет | ✅ |
| Балансировка | Ручная | ✅ |
| Rolling update | Нет | ✅ |

```bash
# Установка minikube (локальный K8s)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start

# kubectl — утилита управления
kubectl get nodes
kubectl get pods
kubectl get all
```

---

## Урок 25 — Архитектура кластера

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-cluster.jpg" alt="Архитектура кластера Kubernetes" width="85%"/>
<br/><em>Control Plane — мозг (планирует и управляет). Nodes — рабочие (запускают Pod'ы)</em>
</div>

```bash
kubectl get nodes -o wide       # Все узлы кластера
kubectl describe node minikube  # Детали узла
kubectl top nodes               # CPU/RAM узлов (нужен metrics-server)
```

---

## Урок 26 — Pod, Deployment, Service

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: мой-сайт
spec:
  replicas: 3                    # Три копии
  selector:
    matchLabels:
      app: сайт
  template:
    metadata:
      labels:
        app: сайт
    spec:
      containers:
      - name: web
        image: nginx:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: сайт-сервис
spec:
  selector:
    app: сайт
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
```

```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get services
minikube service сайт-сервис --url   # Открыть в браузере
```

---

## Урок 27 — Самовосстановление

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-self-healing.jpg" alt="Самовосстановление Kubernetes" width="85%"/>
<br/><em>Упал Pod → Kubernetes заметил → за 5 секунд запустил новый. Автоматически, без тебя!</em>
</div>

```bash
kubectl get pods -w              # Следить за состоянием (Ctrl+C)
kubectl delete pod ИМЯ_ПОДА      # Удалить Pod
# Смотри: K8s сразу создаст новый!

kubectl rollout status deployment/мой-сайт
kubectl rollout history deployment/мой-сайт
kubectl rollout undo deployment/мой-сайт    # Откатить!
```

---

## Урок 28 — Автомасштабирование HPA

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-autoscale.jpg" alt="HPA автомасштабирование" width="85%"/>
<br/><em>HPA следит за нагрузкой: больше запросов → больше Pod'ов. Меньше — уменьшает. Экономия и надёжность</em>
</div>

```bash
# Включить metrics-server
minikube addons enable metrics-server

# Создать HPA
kubectl autoscale deployment мой-сайт \
  --min=2 --max=10 --cpu-percent=70

# Проверить
kubectl get hpa
kubectl describe hpa мой-сайт

# Нагрузочный тест
kubectl run -i --tty load --image=busybox \
  --restart=Never -- sh -c "while true; do wget -q -O- http://сайт-сервис; done"
# В соседнем окне: kubectl get hpa -w  (смотри как растёт!)
```

---

## 📋 Шпаргалка Kubernetes

| Команда | Действие |
|---------|---------|
| `kubectl get pods` | Список Pod'ов |
| `kubectl apply -f file.yaml` | Применить конфиг |
| `kubectl describe pod ИМЯ` | Детали Pod'а |
| `kubectl logs ИМЯ` | Логи Pod'а |
| `kubectl exec -it ИМЯ -- bash` | Войти в Pod |
| `kubectl delete pod ИМЯ` | Удалить Pod |
| `kubectl rollout undo deploy/ИМЯ` | Откатить |
| `kubectl get hpa` | Автомасштаб |

➡️ [Следующий модуль: Секреты и API →](../module6-secrets-api/)
