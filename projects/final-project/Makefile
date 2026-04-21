# Makefile — удобные команды для проекта «Моя Коллекция»
# Запуск: make <команда>

.PHONY: run build compose-up compose-down k8s-deploy k8s-delete test clean

## Локальный запуск (Python напрямую)
run:
	python app.py

## Сборка Docker-образа
build:
	docker build -t my-collection:latest .

## Docker Compose — запустить
compose-up: build
	docker compose up -d
	@echo "\n✅ Сервис запущен: http://localhost:8080"

## Docker Compose — остановить
compose-down:
	docker compose down

## Показать логи
logs:
	docker compose logs -f

## Kubernetes — задеплоить всё
k8s-deploy: build
	kubectl apply -f k8s/
	kubectl rollout status deployment/my-collection
	@echo "\n✅ Деплой завершён"
	@minikube service collection-service --url 2>/dev/null || true

## Kubernetes — удалить
k8s-delete:
	kubectl delete -f k8s/ --ignore-not-found

## Тест API
test:
	@echo "=== Проверяем API ==="
	curl -s http://localhost:8080/ | python3 -m json.tool
	@echo "\n--- Добавляем предмет ---"
	curl -s -X POST http://localhost:8080/items \
	  -H "Content-Type: application/json" \
	  -d '{"name":"Тест","emoji":"🧪","comment":"тестовый предмет"}' | python3 -m json.tool
	@echo "\n--- Список предметов ---"
	curl -s http://localhost:8080/items | python3 -m json.tool

## Очистка
clean:
	docker compose down -v --rmi local 2>/dev/null || true
	rm -f collection.db
	@echo "\n🧹 Очищено"

## Помощь
help:
	@echo "Доступные команды:"
	@echo "  make run          — запустить локально (Python)"
	@echo "  make build        — собрать Docker-образ"
	@echo "  make compose-up   — запустить через Docker Compose"
	@echo "  make compose-down — остановить Docker Compose"
	@echo "  make k8s-deploy   — задеплоить в Kubernetes"
	@echo "  make k8s-delete   — удалить из Kubernetes"
	@echo "  make test         — тест API"
	@echo "  make clean        — очистить всё"
