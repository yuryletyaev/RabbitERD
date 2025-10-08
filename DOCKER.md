# Docker Setup для RabbitMQ ERD Visualizer

## Быстрый старт

### 1. Запуск с Docker Compose (рекомендуется)

```bash
# Клонирование и переход в директорию
git clone <repository-url>
cd RabbitERD

# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 2. Доступ к приложению

- **RabbitMQ ERD Visualizer**: http://localhost:8000
- **RabbitMQ Management UI**: http://localhost:15672 (guest/guest)

## Команды Docker

### Сборка образа
```bash
docker build -t rabbitmq-erd .
```

### Запуск контейнера
```bash
docker run -d \
  --name rabbitmq-erd-app \
  -p 8000:8000 \
  -v $(pwd)/config.json:/app/config.json \
  rabbitmq-erd
```

### Просмотр логов
```bash
docker logs -f rabbitmq-erd-app
```

### Остановка и удаление
```bash
docker stop rabbitmq-erd-app
docker rm rabbitmq-erd-app
```

## Docker Compose команды

### Основные команды
```bash
# Запуск в фоне
docker-compose up -d

# Запуск с пересборкой
docker-compose up --build -d

# Просмотр статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Остановка с удалением volumes
docker-compose down -v
```

### Управление сервисами
```bash
# Запуск только RabbitMQ
docker-compose up -d rabbitmq

# Перезапуск приложения
docker-compose restart app

# Пересборка приложения
docker-compose up --build -d app
```

## Конфигурация

### Переменные окружения

Создайте файл `.env` для настройки:

```env
# RabbitMQ настройки
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/

# Приложение
APP_PORT=8000
APP_HOST=0.0.0.0
```

### Настройка config.json

Убедитесь, что файл `config.json` содержит правильные настройки для подключения к RabbitMQ:

```json
{
  "host": "rabbitmq",
  "port": 5672,
  "username": "guest",
  "password": "guest",
  "vhost": "/"
}
```

## Troubleshooting

### Проблемы с подключением к RabbitMQ
```bash
# Проверка статуса RabbitMQ
docker-compose exec rabbitmq rabbitmq-diagnostics ping

# Просмотр логов RabbitMQ
docker-compose logs rabbitmq
```

### Проблемы с приложением
```bash
# Проверка healthcheck
docker-compose exec app curl -f http://localhost:8000/

# Просмотр логов приложения
docker-compose logs app
```

### Очистка и перезапуск
```bash
# Полная очистка
docker-compose down -v
docker system prune -f
docker-compose up --build -d
```

## Production настройки

### Безопасность
- Измените пароли по умолчанию
- Используйте secrets для паролей
- Настройте SSL/TLS

### Масштабирование
- Используйте внешнюю базу данных
- Настройте load balancer
- Мониторинг с Prometheus/Grafana

### Пример production docker-compose.yml
```yaml
version: '3.8'
services:
  rabbitmq:
    image: rabbitmq:3-management
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - rabbitmq_network
    restart: unless-stopped

  app:
    build: .
    environment:
      - RABBITMQ_HOST=rabbitmq
      - RABBITMQ_USER=${RABBITMQ_USER}
      - RABBITMQ_PASS=${RABBITMQ_PASS}
    depends_on:
      - rabbitmq
    networks:
      - rabbitmq_network
    restart: unless-stopped
```
