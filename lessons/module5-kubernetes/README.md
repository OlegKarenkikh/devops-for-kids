# ⚙️ Модуль 5 — Kubernetes (Уроки 24–28)

> **Цель:** понять зачем нужен Kubernetes, запустить первый кластер и научиться работать с Pod, Deployment, Service.

---

> 💡 **Что такое Pod? Как произносить kubectl? Чем Deployment отличается от Pod?**  
> → [Ответы в Детском FAQ](../kids-faq/#модуль-5--kubernetes)


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





### 🧠 Теория: Control Plane и Worker Nodes

Kubernetes-кластер состоит из двух типов машин:

**Control Plane** (мозг) — принимает решения:
- `kube-apiserver` — принимает все команды (через kubectl)
- `etcd` — база данных кластера, хранит всё состояние
- `scheduler` — решает, на каком Node запустить Pod
- `controller-manager` — следит что реальность соответствует желаемому

**Worker Nodes** (рабочие) — выполняют работу:
- `kubelet` — агент на каждой ноде, запускает Pod'ы
- `kube-proxy` — управляет сетью между Pod'ами
- `container runtime` — Docker или containerd — запускает сами контейнеры

> 💡 На minikube всё это работает на одной машине — Control Plane + Node в одном.

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



### 🧠 Теория: что такое YAML и почему его использует Kubernetes?

**YAML** — это формат для записи конфигурации. Как JSON, но читается людьми. Правила:
- Отступы = структура (всегда пробелы, **никогда табы**)
- `ключ: значение` — пара
- `- элемент` — список
- `#` — комментарий

```yaml
# Пример YAML — список сервисов
services:            # ключ верхнего уровня
  - name: nginx      # список (дефис = элемент)
    port: 80         # вложенное значение
  - name: postgres
    port: 5432
```

**Три главных объекта Kubernetes:**
| Объект | Что делает | Аналогия |
|--------|-----------|----------|
| `Pod` | Запускает 1+ контейнеров | Один рабочий |
| `Deployment` | Управляет N копиями Pod'ов | Бригадир + рабочие |
| `Service` | Даёт постоянный адрес Pod'ам | Ресепшн — не важно кто отвечает |

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-objects.jpg" alt="Kubernetes: Pod, Deployment, Service" width="90%"/>
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



### 🧠 Теория: Reconciliation Loop

Kubernetes работает по принципу **«желаемое состояние»**: ты говоришь «хочу 3 реплики», и Kubernetes **постоянно** проверяет — а сколько реплик сейчас? Если меньше — запускает новые. Если упал Pod — замечает за секунды и поднимает замену автоматически, без твоего участия.

Это называется **Reconciliation Loop** (петля согласования):
```
Желаемое состояние (replicas: 3)
         ↓
  Проверка каждые ~5 сек
         ↓
Реальное состояние (2 пода — один упал)
         ↓
Действие: запустить новый Pod
```

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





### 🧠 Теория: что такое HPA и cpu-percent?

**HPA (Horizontal Pod Autoscaler)** — автоматически добавляет или убирает Pod'ы в зависимости от нагрузки.

`--cpu-percent=70` означает: **если среднее использование CPU всех Pod'ов превысит 70% от их `requests.cpu` — добавь новые Pod'ы**.

```
requests.cpu: 100m  →  лимит = 100 миллицпу
Текущее использование = 80m  →  80%  →  > 70%  →  HPA добавит Pod
Текущее использование = 50m  →  50%  →  < 70%  →  HPA уберёт лишние Pod'ы
```

Диапазон `--min=2 --max=10`: никогда не меньше 2 Pod'ов (надёжность), никогда больше 10 (защита от перерасхода ресурсов).

<div align="center">
  <img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-kubectl.jpg" alt="kubectl шпаргалка" width="90%"/>
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

![module5-k8s-rolling-update](https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/module5-k8s-rolling-update.jpg)


> 💡 **Задание к уроку 27 — Самовосстановление:**
> ```bash
> # 1. Запусти Deployment из урока 26
> # 2. Открой два терминала: в первом смотри поды, во втором удаляй
> kubectl get pods -w                     # терминал 1 — наблюдай в реальном времени
> kubectl delete pod <имя-любого-пода>    # терминал 2 — убей Pod
> # Видишь? Новый Pod поднялся автоматически за несколько секунд ✅
> ```

> 💡 **Задание к уроку 28 — Автомасштабирование:**
> ```bash
> minikube addons enable metrics-server
> kubectl autoscale deployment hello-kids --min=2 --max=5 --cpu-percent=50
> kubectl get hpa -w                      # наблюдай изменения в реальном времени
> # Нагрузи сервис (в другом терминале):
> kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://hello-kids-svc; done"
> # Смотри как растёт REPLICAS в kubectl get hpa ✅
> ```

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

## 🧩 Быстрый тест — проверь себя

| Вопрос | Ответ |
|--------|-------|
| Минимальная единица в Kubernetes? | Pod (один или несколько контейнеров) |
| Что делает Deployment при падении Pod'а? | Автоматически создаёт новый (self-healing) |
| Как Service находит нужные Pod'ы? | По меткам (`selector: app: myapp`) |
| Что такое Rolling Update? | Замена Pod'ов по одному — без простоя |
| Команда для просмотра всех Pod'ов? | `kubectl get pods` |
| Как масштабировать вручную до 5 реплик? | `kubectl scale deployment myapp --replicas=5` |

## 🧠 Чекпойнт понимания — обязательный

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/checkpoint.jpg" alt="Чекпойнт понимания" width="90%"/>
<br/><em>Три вопроса после каждого урока. Понимание важнее скорости.</em>
</div>

Прежде чем перейти к Модулю 6 — ответь себе вслух или письменно:

**1. Зачем нужен Kubernetes если уже есть Docker Compose? Когда один заменяет другой?**

**2. Что такое Pod, Deployment и Service? Объясни каждый одним предложением.**

**3. Как HPA (Horizontal Pod Autoscaler) понимает, что нужно добавить Pod'ы?**

**4. Что такое Rolling Update и почему он лучше чем просто остановить всё и перезапустить?**

> 💡 Если не можешь ответить на вопрос — вернись к соответствующему уроку. Понимание важнее скорости!

➡️ [Следующий модуль: Секреты и API →](../module6-secrets-api/)
