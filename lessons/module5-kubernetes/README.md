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
|---|-----------|-----------|
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

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-objects.jpg" alt="Kubernetes: Pod, Deployment, Service" width="900"/>
  <br/><em>☸️ Рис. 7 — Три главных объекта k8s: Pod → Deployment → Service с YAML примерами</em>
</div>


> **Важно:** имена объектов в Kubernetes — только латиница, цифры и дефис. Кириллица не работает!

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-website          # ✅ латиница, без пробелов
spec:
  replicas: 3               # Три копии — всегда работает хотя бы одна
  selector:
    matchLabels:
      app: website
  template:
    metadata:
      labels:
        app: website
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
  name: website-service     # ✅ латиница
spec:
  selector:
    app: website
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
```

```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get services
minikube service website-service --url
```

---

## Урок 27 — Самовосстановление

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-self-healing.jpg" alt="Самовосстановление Kubernetes" width="85%"/>
<br/><em>Упал Pod → Kubernetes заметил → за 5 секунд запустил новый. Автоматически, без тебя!</em>
</div>

```bash
kubectl get pods -w
kubectl delete pod <имя-пода>
kubectl rollout status deployment/my-website
kubectl rollout history deployment/my-website
kubectl rollout undo deployment/my-website
```

---

## Урок 28 — Автомасштабирование HPA

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-kubectl.jpg" alt="kubectl шпаргалка" width="900"/>
  <br/><em>⚙️ Рис. 8 — Шпаргалка kubectl: смотреть / запускать / отлаживать</em>
</div>


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-autoscale.jpg" alt="HPA автомасштабирование" width="85%"/>
<br/><em>HPA следит за нагрузкой: больше запросов → больше Pod'ов. Меньше — уменьшает. Экономия и надёжность</em>
</div>

```bash
minikube addons enable metrics-server
kubectl autoscale deployment my-website --min=2 --max=10 --cpu-percent=70
kubectl get hpa
kubectl describe hpa my-website
```

---

## 📋 Шпаргалка Kubernetes

| Команда | Действие |
|---------|---------|
| `kubectl get pods` | Список Pod'ов |
| `kubectl apply -f file.yaml` | Применить конфиг |
| `kubectl describe pod <имя>` | Детали Pod'а |
| `kubectl logs <имя>` | Логи Pod'а |
| `kubectl exec -it <имя> -- bash` | Войти в Pod |
| `kubectl delete pod <имя>` | Удалить Pod |
| `kubectl rollout undo deploy/<имя>` | Откатить |
| `kubectl get hpa` | Автомасштаб |

➡️ [Следующий модуль: Секреты и API →](../module6-secrets-api/)
