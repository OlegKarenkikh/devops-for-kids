# ⚙️ Модуль 5 — Kubernetes (Уроки 24–28)

> **Цель:** понять зачем нужен Kubernetes, запустить первый кластер и научиться работать с Pod, Deployment, Service.

---

> 💡 **Что такое Pod? Как произносить kubectl? Чем Deployment отличается от Pod?**  
> → [Ответы в Детском FAQ](../kids-faq/#модуль-5--kubernetes)


## Урок 24 — Docker vs Kubernetes

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module5-docker-vs-k8s.png" alt="Docker один корабль, Kubernetes флот" width="85%"/>
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
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module5-k8s-cluster.png" alt="Архитектура кластера Kubernetes" width="85%"/>
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
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module5-k8s-objects.png" alt="Kubernetes: Pod, Deployment, Service" width="900"/>
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
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module5-k8s-self-healing.png" alt="Самовосстановление Kubernetes" width="85%"/>
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
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module5-kubectl.png" alt="kubectl шпаргалка" width="900"/>
  <br/><em>⚙️ Рис. 8 — Шпаргалка kubectl: смотреть / запускать / отлаживать</em>
</div>


<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/audit-unified-illustrations-faq/images/module5-k8s-autoscale.png" alt="HPA автомасштабирование" width="85%"/>
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


---

## 🎯 Практические задания

### Задание 1 — Запусти Minikube
```bash
minikube start
kubectl get nodes          # нода Ready?
minikube dashboard         # веб-интерфейс
```

### Задание 2 — Первый Deployment
```bash
cat > deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-kids
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-kids
  template:
    metadata:
      labels:
        app: hello-kids
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
EOF

kubectl apply -f deployment.yaml
kubectl get pods            # 2 пода Running?
```

### Задание 3 — Открой сервис в браузере
```bash
cat > service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: hello-kids-svc
spec:
  selector:
    app: hello-kids
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
EOF

kubectl apply -f service.yaml
minikube service hello-kids-svc   # откроет браузер!
```
> ✅ Страница nginx открылась через Kubernetes? Ты сделал это! ☸️

---

## ❓ Частые вопросы новичков по этому уроку

<details>
<summary><b>«Kubernetes» — откуда слово, как произносить?</b></summary>

Греческое (κυβερνήτης) = «кормчий». Произносится **«кубернэтес»** или **«кубик»**.
`k8s` = k + 8 букв + s. Создан Google в 2014, open source.

</details>

<details>
<summary><b>Pod — это стручок гороха?</b></summary>

Да! Внутри Pod — контейнеры, которые всегда вместе: один сервер, один localhost, общая сеть.

```bash
kubectl get pods && kubectl logs my-pod && kubectl exec -it my-pod -- bash
```

</details>

<details>
<summary><b>Чем Deployment отличается от Pod?</b></summary>

| | Pod | Deployment |
|---|---|---|
| Упал | Не перезапустится | Создаст новый автоматически |
| Масштаб | 1 | Любое количество реплик |
| Обновление | Вручную | Rolling update |

> 👔 Pod — рабочий. Deployment — менеджер, следящий за нужным числом рабочих.

</details>

<details>
<summary><b>kubectl — как произносится?</b></summary>

**«кубе-контрол»** или **«кубектл»** — единого стандарта нет. `kube` + `ctl` (control).

</details>

> 💬 [Полный FAQ](../kids-faq/) | [Задать вопрос](https://github.com/OlegKarenkikh/devops-for-kids/issues)

