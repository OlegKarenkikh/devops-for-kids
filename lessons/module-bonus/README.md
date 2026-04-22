# 🎓 Продвинутый модуль — Сети, HTTPS, ИИ и реальные проекты

> **🎯 Цель бонусного модуля:** познакомиться с передовыми практиками DevOps — мониторингом, безопасностью, AI-инструментами и оркестрацией. Для тех, кто освоил основные модули и хочет идти дальше.


> **Для кого:** прошёл все базовые модули (1–5) и хочешь большего.
> **Что внутри:** модель OSI, HTTPS в своём проекте, Telegram-бот, LLM на GPU, FastAPI, путь к ИИ-агентам.

---

## Глава 1 — Модель OSI: как данные путешествуют по сети

### 🧠 Теория: зачем нужна модель OSI?

Когда ты открываешь сайт — данные проходят **7 уровней** обработки, от физического сигнала до текста на экране. Модель OSI — это как инструкция сборки: каждый уровень делает свою работу и передаёт результат следующему.

| Уровень | Название | Что делает | Протоколы |
|---------|----------|------------|----------|
| 7 | Приложение | Твои данные | HTTP, DNS, SSH |
| 6 | Представление | Шифрование, сжатие | TLS/SSL |
| 5 | Сеанс | Управление соединением | — |
| 4 | Транспорт | Надёжная доставка | TCP, UDP |
| 3 | Сеть | Маршрутизация | IP |
| 2 | Канал | Кадры данных | Ethernet, Wi-Fi |
| 1 | Физический | Биты/сигналы | Кабель, радио |

> 💡 DevOps работает преимущественно на уровнях 3–7: IP-адреса, TCP-порты, HTTP, TLS.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/osi_model.jpg" alt="Модель OSI — 7 уровней" width="90%"/>
<br/><em>7 этажей, на каждом свои правила — так устроена любая сеть в мире</em>
</div>

### Метафора: международная почта

Когда ты отправляешь письмо из России в Японию, оно проходит несколько этапов: написал → вложил в конверт → наклеил марку → отнёс на почту → грузовик → самолёт → японская почта → доставка. Каждый этап — отдельный слой. Каждый делает своё дело и не знает деталей других.

Сеть работает **точно так же** — 7 уровней модели OSI:

| Уровень | Название | Что делает | Протоколы | Где в нашем проекте |
|---------|---------|-----------|----------|-------------------|
| **7** | Прикладной | Данные для пользователя | **HTTP, HTTPS, DNS** | Flask API, браузер |
| **6** | Представления | Шифрование, сжатие | **TLS/SSL** | HTTPS сертификат |
| **5** | Сеансовый | Управление сессиями | WebSocket | Telegram соединение |
| **4** | Транспортный | Доставка пакетов, порты | **TCP, UDP** | Порт :8080, :443 |
| **3** | Сетевой | Маршрутизация по IP | **IP, ICMP** | Docker сети, Kubernetes |
| **2** | Канальный | Передача между устройствами | Ethernet, Wi-Fi | Физическая сеть |
| **1** | Физический | Биты по кабелю/эфиру | 10BASE-T, 802.11 | Провод в стене |

### Где находятся наши инструменты

Уровень 7 (Прикладной):  HTTP/HTTPS запросы к Flask/FastAPI
                          curl http://localhost:8080/items
                          Telegram Bot API

Уровень 4 (Транспортный): TCP-соединение, порты
                          docker run -p 8080:8080  ← порт здесь!
                          Kubernetes Service port: 80

Уровень 3 (Сетевой):      IP-адреса Docker контейнеров
                          docker network inspect → видишь IP
                          Pod'ы в Kubernetes получают IP

Уровень 2 (Канальный):    Docker bridge сеть
                          MAC-адреса виртуальных интерфейсов

Уровень 1 (Физический):   Провод сервера в дата-центре
                          (это уже не наша забота)


### HTTP vs HTTPS: в чём разница на уровне OSI

**HTTP** — данные летят открытым текстом на уровне 7. Любой, кто «стоит между» клиентом и сервером, может прочитать пароль.

**HTTPS** = HTTP + TLS (уровень 6). TLS шифрует данные **до** того как они уходят на уровень 7. Даже если кто-то перехватит трафик — увидит только зашифрованный мусор.

```text
HTTP:   Браузер → [пароль: qwerty123 открыто] → Сервер
HTTPS:  Браузер → [X#9f@!kL2m зашифровано] → TLS расшифровка → Сервер
```

---

## Глава 2 — Добавить HTTPS в свой проект

### 🧠 Теория: что такое TLS и зачем HTTPS?

**HTTP** — данные передаются открытым текстом. Любой в твоей сети может перехватить пароль или куки. **HTTPS = HTTP + TLS** — данные зашифрованы.

**TLS-сертификат** — это как паспорт сайта: подтверждает что `example.com` — это действительно `example.com`, а не мошенник. **Let's Encrypt** выдаёт бесплатные сертификаты на 90 дней, **Certbot** автоматически их обновляет.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/https_nginx_certbot.jpg" alt="HTTPS через Nginx + Certbot" width="90%"/>
<br/><em>Nginx — ворота с замком. Certbot получает бесплатный сертификат. Flask не знает про HTTPS — это не его дело!</em>
</div>

### Принцип: разделение ответственности

Flask умеет обрабатывать запросы. Но заниматься SSL — не его работа. Для этого есть **Nginx** — профессиональный реверс-прокси.

```text
Пользователь → HTTPS :443 → Nginx → HTTP :8080 → Flask
                  🔒 TLS здесь          ✅ внутри без шифрования
```

**Nginx** принимает зашифрованный запрос, расшифровывает, передаёт Flask. Flask отвечает — Nginx зашифровывает и отдаёт пользователю. Flask работает как обычно — ничего не меняется в коде.

### Шаг 1: Получить домен

Бесплатные домены для практики: `имя.pp.ua`, `имя.eu.org`
Или купить домен: `nic.ru`, `reg.ru` (~100-200 руб/год)

DNS запись: `A 1.2.3.4` (IP твоего сервера)

### Шаг 2: docker-compose.yml с Nginx + Certbot

```yaml
# docker-compose.yml
version: "3.9"
services:
  app:
    build: .
    expose:
      - "8080"              # Только внутри Docker сети — не снаружи!
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"             # HTTP — нужен Certbot для проверки
      - "443:443"           # HTTPS — основной
    volumes:
      - ./nginx/conf:/etc/nginx/conf.d     # Конфиг Nginx
      - certbot_www:/var/www/certbot       # Для проверки Let's Encrypt
      - certbot_conf:/etc/letsencrypt      # Сертификаты
    depends_on:
      - app
    restart: unless-stopped

  certbot:
    image: certbot/certbot
    volumes:
      - certbot_www:/var/www/certbot
      - certbot_conf:/etc/letsencrypt
    # Обновляет сертификат каждые 12 часов (если нужно)
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h; done'"

volumes:
  certbot_www:
  certbot_conf:

### Шаг 3: конфиг Nginx

nginx
# nginx/conf/app.conf

# Сначала — только HTTP, для получения сертификата
server {
    listen 80;
    server_name твой-домен.ru;

    # Let's Encrypt проверяет владение доменом через этот путь
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Все остальные запросы — перенаправить на HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS — добавить после получения сертификата
server {
    listen 443 ssl;
    server_name твой-домен.ru;

    ssl_certificate     /etc/letsencrypt/live/твой-домен.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/твой-домен.ru/privkey.pem;

    # Рекомендованные настройки безопасности
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://app:8080;           # Передать Flask
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

### Шаг 4: получить сертификат

bash
# 1. Запустить только nginx (HTTP)
docker compose up -d nginx

# 2. Получить сертификат
docker compose run --rm certbot certonly   --webroot -w /var/www/certbot   --email твой@email.com   --agree-tos --no-eff-email   -d твой-домен.ru

# 3. Раскомментировать HTTPS блок в nginx.conf
# 4. Перезапустить
docker compose restart nginx

# 5. Проверить
curl https://твой-домен.ru/items

> ✅ **Сертификат бесплатный** от Let's Encrypt, обновляется автоматически каждые 90 дней.

---

## Глава 3 — Telegram-бот на Python в Docker

### 🧠 Теория: как работает Telegram Bot API?

Telegram предоставляет **Bot API** — HTTP интерфейс для управления ботами. Твой Python-скрипт делает `long polling`: каждые несколько секунд спрашивает Telegram «есть новые сообщения?». Получает — обрабатывает — отвечает.


[Пользователь] → Telegram серверы → [Bot API] → твой Python → [Bot API] → Telegram → [Пользователь]

**Токен бота** — как пароль: получить у @BotFather, хранить в `.env`, никогда не коммитить.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/telegram_bot_arch.jpg" alt="Telegram Bot архитектура" width="90%"/>
<br/><em>Бот — это обычный Python процесс в контейнере, который слушает Telegram через API</em>
</div>

### Два режима работы бота

| Режим | Как работает | Когда использовать |
|-------|-------------|-------------------|
| **Polling** | Бот каждые N секунд спрашивает Telegram: «есть новые сообщения?» | Разработка, простые боты |
| **Webhook** | Telegram сам отправляет запрос на твой сервер при каждом сообщении | Продакшен, нужен HTTPS |

### Создать бота


1. Написать @BotFather в Telegram
2. /newbot → дать имя → получить TOKEN
3. Сохранить TOKEN в .env файл

### Код бота (python-telegram-bot v20+)

python
# bot.py — асинхронный бот с командами
import asyncio, os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"Привет, {name}! 👋\n"
        f"Я бот-коллекция. Команды:\n"
        f"/add Гитара — добавить предмет\n"
        f"/list — посмотреть коллекцию\n"
        f"/ask <вопрос> — спросить ИИ"
    )

# Обработчик команды /add
async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи название: /add Гитара")
        return
    item = " ".join(context.args)
    # Здесь можно сохранить в PostgreSQL или через HTTP в наш API
    await update.message.reply_text(f"✅ Добавил: {item}")

# Обработчик команды /ask — запрос к LLM
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Задай вопрос: /ask Что такое Docker?")
        return
    question = " ".join(context.args)
    await update.message.reply_text("🤔 Думаю...")
    
    # Запрос к Ollama (запущен рядом в Docker Compose)
    import httpx
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post("http://ollama:11434/api/generate", json={
            "model": "llama3.2",
            "prompt": question,
            "stream": False
        })
        answer = resp.json()["response"]
    await update.message.reply_text(answer)

# Обработчик обычных сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Ты написал: {text}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_item))
    app.add_handler(CommandHandler("ask", ask_ai))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("Бот запущен...")
    app.run_polling()          # Режим polling — для разработки

if __name__ == "__main__":
    main()

### Docker Compose для бота

yaml
# docker-compose.yml
version: "3.9"
services:
  bot:
    build: .
    environment:
      TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: bot_db
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
bash
# .env
TELEGRAM_TOKEN=1234567890:AAF-твой-токен-от-BotFather
DB_PASSWORD=секрет

# Запустить
docker compose up -d
docker compose logs -f bot

---

## Глава 4 — LLM в Docker: Ollama и vLLM

### 🧠 Теория: что такое LLM и зачем запускать локально?

**LLM (Large Language Model)** — большая языковая модель, как ChatGPT. Запускать локально нужно когда: данные конфиденциальны, нет интернета, нужен полный контроль.

**Ollama** — простой способ запустить LLM одной командой. **vLLM** — высокопроизводительный сервер для продакшна с поддержкой параллельных запросов.

| | Ollama | vLLM |
|---|---|---|
| Установка | `curl ollama.ai/install.sh \| sh` | `pip install vllm` |
| Для | Разработки, экспериментов | Продакшн, нагрузка |
| GPU | Опционально | Обязательно для скорости |
| API | OpenAI-совместимый | OpenAI-совместимый |

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/ollama_vs_vllm.jpg" alt="Ollama vs vLLM" width="90%"/>
<br/><em>Ollama — для старта и разработки. vLLM — для нагрузки и продакшена</em>
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/gpu_docker.jpg" alt="GPU в Docker" width="90%"/>
<br/><em>GPU попадает в контейнер через NVIDIA Container Toolkit — одна установка, затем параметр --gpus all</em>
</div>

### Ollama — самый простой старт

bash
# Установить NVIDIA Container Toolkit (один раз на сервере)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor   -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Проверить что GPU виден
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
yaml
# docker-compose.yml с Ollama
version: "3.9"
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"           # REST API Ollama
    volumes:
      - ollama_models:/root/.ollama   # Модели сохраняются!
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1           # Количество GPU
              capabilities: [gpu]
    restart: unless-stopped

volumes:
  ollama_models:
bash
# Запустить и скачать модель
docker compose up -d ollama

# Скачать модели (выбери по VRAM)
docker compose exec ollama ollama pull llama3.2        # 2GB VRAM — маленькая, быстрая
docker compose exec ollama ollama pull qwen2.5:7b      # 5GB VRAM — хорошее качество
docker compose exec ollama ollama pull qwen2.5:14b     # 9GB VRAM — высокое качество
docker compose exec ollama ollama pull llava:13b       # 8GB VRAM — видит картинки (VLM)

# Тест API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Что такое Docker? Кратко",
  "stream": false
}'

### Как подобрать модель по VRAM

| VRAM GPU | Рекомендуемая модель | Качество | Скорость |
|----------|---------------------|---------|---------|
| 4 GB | `llama3.2:3b`, `phi3.5:mini` | Базовое | Быстро |
| 6–8 GB | `llama3.2`, `qwen2.5:7b`, `mistral` | Хорошее | Нормально |
| 10–12 GB | `qwen2.5:14b`, `llava:13b` (VLM) | Отличное | Нормально |
| 16–24 GB | `qwen2.5:32b`, `llama3.1:70b (Q4)` | Очень высокое | Медленно |
| CPU only | `llama3.2:3b` (медленно) | Базовое | Очень медленно |

> 📥 Все модели: [ollama.com/library](https://ollama.com/library) — ищи по тегу количества параметров

### vLLM — для продакшена

yaml
# docker-compose с vLLM (OpenAI-совместимый API)
services:
  vllm:
    image: vllm/vllm-openai:latest
    ports:
      - "8000:8000"
    volumes:
      - hf_cache:/root/.cache/huggingface
    environment:
      HF_TOKEN: ${HF_TOKEN}         # Токен HuggingFace для приватных моделей
    command: >
      --model Qwen/Qwen2.5-7B-Instruct
      --dtype auto                      # Автовыбор float16/bfloat16
      --max-model-len 8192              # Максимум токенов в контексте
      --gpu-memory-utilization 0.90     # 90% GPU памяти под модель
      --tensor-parallel-size 1          # Количество GPU (>1 для больших моделей)
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  hf_cache:
python
# Использование vLLM — OpenAI-совместимый API
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",  # Наш vLLM
    api_key="not-needed"                  # vLLM не требует ключ
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {"role": "system", "content": "Ты помощник DevOps-инженера."},
        {"role": "user", "content": "Объясни разницу между CMD и ENTRYPOINT в Dockerfile"}
    ],
    temperature=0.7,
    max_tokens=500
)
print(response.choices[0].message.content)

---

## Глава 5 — Типы AI моделей: что бывает

### 🧠 Теория: карта AI моделей

AI-модели специализированы — каждая делает одно, но делает хорошо:

| Тип | Расшифровка | Что умеет | Пример |
|-----|-------------|-----------|--------|
| LLM | Large Language Model | Текст → Текст | LLaMA, Mistral |
| VLM | Vision Language Model | Текст + Картинка → Текст | LLaVA, Gemma3 |
| STT | Speech-to-Text | Аудио → Текст | Whisper |
| TTS | Text-to-Speech | Текст → Аудио | Coqui, Bark |
| Diffusion | — | Текст → Картинка | Stable Diffusion |

DevOps-задача: запустить нужную модель в контейнере и дать к ней API-доступ.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/ai_model_types.jpg" alt="Типы AI моделей" width="90%"/>
<br/><em>LLM, VLM, STT, TTS, Image Gen — каждая модель решает свою задачу</em>
</div>

### VLM — модели работающие с изображениями

VLM (Vision Language Model) — LLM которая видит картинки. На вход: текст + картинка. На выходе: текст.

python
# LLaVA / Qwen-VL через Ollama — анализ изображения
import httpx, base64

# Загрузить картинку в base64
with open("screenshot.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

response = httpx.post("http://localhost:11434/api/generate", json={
    "model": "llava:13b",           # или qwen2.5vl, llava-phi3
    "prompt": "Что на этом скриншоте? Опиши ошибку",
    "images": [img_b64],
    "stream": False
})
print(response.json()["response"])

**Популярные VLM модели (2025–2026):**

| Модель | VRAM | Особенности |
|--------|------|------------|
| `llava:13b` | 8GB | Классика, стабильная |
| `qwen2.5vl:7b` | 6GB | Лучшее соотношение, понимает русский |
| `llava-phi3:mini` | 4GB | Маленькая, быстрая |
| `moondream2` | 2GB | Минимальные ресурсы |

### Whisper — голос в текст (STT)

yaml
# docker-compose фрагмент
  whisper:
    image: onerahmet/openai-whisper-asr-webservice:latest
    ports:
      - "9000:9000"
    environment:
      ASR_MODEL: base            # tiny/base/small/medium/large
      ASR_ENGINE: openai_whisper
python
# Транскрибировать аудио
import httpx

with open("voice.ogg", "rb") as f:
    resp = httpx.post("http://localhost:9000/asr",
        files={"audio_file": f},
        data={"language": "ru", "output": "json"}
    )
print(resp.json()["text"])

### Полный docker-compose.yml для AI стека

yaml
# docker-compose.yml — полный AI стек
version: "3.9"
services:
  # Telegram бот
  bot:
    build: ./bot
    environment:
      TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}
      OLLAMA_URL: http://ollama:11434
      WHISPER_URL: http://whisper:9000
      DB_URL: postgresql://user:${DB_PASSWORD}@db:5432/botdb
    depends_on: [ollama, whisper, db]
    restart: unless-stopped

  # FastAPI gateway
  api:
    build: ./api
    ports:
      - "8080:8080"
    environment:
      DB_URL: postgresql://user:${DB_PASSWORD}@db:5432/botdb
      OLLAMA_URL: http://ollama:11434
    depends_on: [ollama, db]
    restart: unless-stopped

  # LLM (Ollama)
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  # STT (Whisper)
  whisper:
    image: onerahmet/openai-whisper-asr-webservice:latest
    environment:
      ASR_MODEL: small
    restart: unless-stopped

  # База данных
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: botdb
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  # Кэш сессий
  redis:
    image: redis:7-alpine
    restart: unless-stopped

  # Мониторинг
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    depends_on: [prometheus]
    restart: unless-stopped

volumes:
  ollama_data:
  pgdata:

networks:
  default:
    name: ai-stack

---

## Глава 6 — FastAPI: современный способ делать API

### 🧠 Теория: Flask vs FastAPI — что выбрать?

| | Flask | FastAPI |
|---|---|---|
| Скорость разработки | Простой старт | Простой старт + автодокументация |
| Производительность | Средняя | Высокая (async) |
| Документация | Вручную | Автоматически (`/docs`) |
| Валидация данных | Вручную | Автоматически (Pydantic) |
| Когда использовать | Простые проекты, обучение | Продакшн API, AI сервисы |

**Pydantic** — библиотека для валидации: ты описываешь структуру данных классом, FastAPI сам проверяет что пришло правильное.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/fastapi_intro.jpg" alt="FastAPI" width="90%"/>
<br/><em>FastAPI генерирует документацию автоматически — зайди на /docs и тестируй без curl</em>
</div>

### Почему FastAPI лучше Flask для API

| | Flask | FastAPI |
|-|-------|---------|
| Скорость | Средняя | В 2–3 раза быстрее (async) |
| Документация | Вручную | **Авто-генерация /docs** |
| Типы данных | Нет | Pydantic валидация |
| async/await | Плохо | Отлично |
| WebSocket | Плохо | Отлично |

### Код FastAPI — коллекция с документацией

python
# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx, os

app = FastAPI(
    title="Моя Коллекция API",
    description="REST API для управления коллекцией с ИИ",
    version="2.0.0"
)

# Pydantic модель — автоматическая валидация входных данных
class Item(BaseModel):
    name: str                          # Обязательное
    emoji: Optional[str] = "📦"       # Необязательное
    comment: Optional[str] = None

class AskRequest(BaseModel):
    question: str
    model: str = "llama3.2"

# Хранилище (в продакшене — PostgreSQL)
items_db = []

@app.get("/")
def root():
    return {"service": "Коллекция API", "version": "2.0", "docs": "/docs"}

@app.get("/items")
def list_items():
    return {"items": items_db, "total": len(items_db)}

@app.post("/items", status_code=201)
def add_item(item: Item):
    # FastAPI автоматически валидирует item.name, item.emoji
    new_item = {"id": len(items_db) + 1, **item.dict()}
    items_db.append(new_item)
    return new_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            return items_db.pop(i)
    raise HTTPException(status_code=404, detail="Предмет не найден")

# Эндпоинт для вопросов к ИИ
@app.post("/ask")
async def ask_ai(req: AskRequest):
    ollama_url = os.environ.get("OLLAMA_URL", "http://ollama:11434")
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{ollama_url}/api/generate", json={
            "model": req.model,
            "prompt": req.question,
            "stream": False
        })
        return {"answer": resp.json()["response"], "model": req.model}

# Эндпоинт здоровья (для Kubernetes liveness probe)
@app.get("/health")
def health():
    return {"status": "ok"}
bash
# Установить и запустить
pip install fastapi uvicorn httpx

# Запустить
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# Открыть авто-документацию в браузере:
# http://localhost:8080/docs   ← Swagger UI
# http://localhost:8080/redoc  ← ReDoc

---

## Глава 7 — Полная архитектура AI агента

### 🧠 Теория: что такое AI агент?

**AI агент** — это LLM + инструменты. Обычная LLM отвечает на вопросы. Агент может **действовать**: искать в интернете, читать файлы, вызывать API, запускать код.


Пользователь: "Найди погоду в Москве и пришли в Telegram"
        ↓
   AI агент (LLM)
        ↓ решает какой инструмент использовать
   [поиск погоды API] → [Telegram API]
        ↓
Ответ пользователю: "В Москве +15°C ☁️"

> Ты уже знаешь все компоненты: Docker, API (Flask/FastAPI), секреты (.env), Telegram-боты. Агент — это их комбинация.

<div align="center">
<img src="https://raw.githubusercontent.com/OlegKarenkikh/devops-for-kids/main/images/ai_agent_architecture.jpg" alt="AI агент — полная архитектура" width="90%"/>
<br/><em>Это следующий шаг — курс «AI Agents». Ты уже знаешь все компоненты!</em>
</div>

### Что такое AI агент?

Обычная LLM отвечает на вопрос и всё. **Агент** — это LLM которая может:
1. Принимать решения: что сделать дальше
2. Вызывать инструменты: поиск в интернете, база данных, API
3. Помнить контекст: история разговора
4. Работать в цикле: думать → действовать → наблюдать → думать

python
# Простой агент с памятью (LangChain / llama-index стиль)
class SimpleAgent:
    def __init__(self, ollama_url: str, db_conn):
        self.llama = OllamaClient(ollama_url, model="qwen2.5:7b")
        self.db = db_conn
        self.history = []              # Память

    async def chat(self, user_message: str) -> str:
        # Добавить в историю
        self.history.append({"role": "user", "content": user_message})
        
        # Системный промпт — инструкция агенту
        system = "Ты помощник по коллекциям. Отвечай кратко и по-русски."
        
        # Отправить историю в модель
        response = await self.llama.chat(
            messages=self.history,
            system=system
        )
        
        # Сохранить ответ в историю
        self.history.append({"role": "assistant", "content": response})
        
        # Сохранить историю в PostgreSQL
        await self.db.save_message(user_message, response)
        
        return response

### Дорожная карта: куда двигаться дальше


Этот курс (DevOps для начинающих):
  ✅ Терминал → Git → Docker → Compose → Kubernetes

Следующий курс (AI Agents):
  📚 LLM API (OpenAI, Anthropic, Ollama)
  📚 Промпт-инжиниринг — как правильно писать инструкции моделям
  📚 Память агента (ChromaDB, pgvector)
  📚 Инструменты агента (RAG, поиск, API вызовы)
  📚 Multi-agent системы (CrewAI, AutoGen)
  📚 Fine-tuning — обучить модель на своих данных

Продвинутый уровень:
  🎯 MLOps — управление моделями в продакшене
  🎯 Kubernetes + GPU оркестрация
  🎯 A/B тестирование моделей
  🎯 Streaming ответы (WebSocket + SSE)

### Где скачать модели

| Ресурс | Что там | Как использовать |
|--------|---------|----------------|
| [ollama.com/library](https://ollama.com/library) | Готовые модели для Ollama | `ollama pull имя` |
| [huggingface.co](https://huggingface.co) | Все модели мира | vLLM, transformers |
| [lmstudio.ai](https://lmstudio.ai) | GUI для запуска моделей локально | Удобно для старта |
| [openrouter.ai](https://openrouter.ai) | API к 100+ моделям | Один ключ — все модели |

---

*Ты освоил полный современный стек — от терминала до AI агентов. Дальше — только практика!*

➡️ [← Вернуться к модулям](../../README.md)


---

## 🎯 Практические задания бонусного модуля

### Задание 1 — HTTPS с Nginx + Certbot (локальная симуляция)
bash
# Запусти Nginx и получи самоподписанный сертификат
docker run -d -p 443:443 -p 80:80 --name nginx-ssl nginx:alpine

# Подключись внутрь и сгенерируй SSL
docker exec -it nginx-ssl sh
apk add openssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl.key -out /etc/nginx/ssl.crt \
  -subj "/CN=localhost"
exit
> ✅ Понял разницу между HTTP и HTTPS? Ключ + сертификат = замок!

### Задание 2 — Telegram-бот за 10 минут
bash
pip install python-telegram-bot

cat > bot.py << 'EOF'
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-DevOps 🤖")

async def hello(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(f"Привет, {name}! Ты изучаешь DevOps — это круто! 🚀")

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.run_polling()
EOF

# Получи токен у @BotFather в Telegram и запусти:
export BOT_TOKEN="твой_токен"
python bot.py
> ✅ Бот отвечает на /start? Ты написал рабочего Telegram-бота!

### Задание 3 — Ollama: локальная AI-модель
bash
# Установи Ollama (Linux/Mac)
curl -fsSL https://ollama.ai/install.sh | sh

# Скачай маленькую модель и поговори с ней
ollama pull phi3:mini          # ~2GB, быстрая модель от Microsoft
ollama run phi3:mini
# Напиши: "Объясни Docker простыми словами"
# Выйди: /bye
> ✅ AI ответила прямо на твоём компьютере, без облака!

### Задание 4 — FastAPI
bash
pip install fastapi uvicorn

cat > main.py << 'EOF'
from fastapi import FastAPI
app = FastAPI()

skills = ["Linux", "Git", "Docker", "Kubernetes"]

@app.get("/")
def root():
    return {"message": "DevOps Academy API 🚀"}

@app.get("/skills")
def get_skills():
    return {"skills": skills, "count": len(skills)}

@app.post("/skills/{skill}")
def add_skill(skill: str):
    skills.append(skill)
    return {"added": skill, "total": len(skills)}
EOF

uvicorn main:app --reload
# Открой http://localhost:8000/docs — автодокументация!
```
> ✅ Видишь Swagger UI с твоим API? FastAPI сгенерировал документацию сам!

