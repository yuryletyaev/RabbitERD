# RabbitMQ ERD Visualizer

Веб-приложение для визуализации топологии RabbitMQ в виде блок-схем. Показывает обмены (exchanges), очереди (queues) и связи между ними (bindings).

## Возможности

- 🎯 Интерактивная визуализация топологии RabbitMQ
- 🔄 Автоматическое обновление данных
- 🎨 Современный и адаптивный интерфейс
- 📊 Статистика по обменам, очередям и связям
- 🔍 Детальная информация по каждому элементу
- 🖱️ Интерактивное управление (зум, перетаскивание)
- 📱 Поддержка мобильных устройств

## Требования

- Python 3.8+
- RabbitMQ с включенным Management Plugin
- Доступ к RabbitMQ Management API (порт 15672)

## Установка

1. Клонируйте репозиторий или скачайте файлы проекта

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте подключение к RabbitMQ:
   - Скопируйте `config.example.json` в `config.json`:
   ```bash
   cp config.example.json config.json
   ```
   - Отредактируйте `config.json` под ваши настройки RabbitMQ:
   ```json
   {
     "rabbitmq": {
       "host": "localhost",
       "port": 5672,
       "username": "guest",
       "password": "guest",
       "vhost": "/",
       "management_port": 15672
     }
   }
   ```

## Запуск

### Тестирование подключения
Перед запуском рекомендуется проверить подключение к RabbitMQ:
```bash
python test_app.py
```

### Запуск приложения

#### Способ 1: Прямой запуск
```bash
python3 main.py
```

#### Способ 2: С uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Способ 3: Удобные скрипты
```bash
python3 run.py
```

Или если есть проблемы с uvicorn:
```bash
python3 run_simple.py
```

#### Способ 4: Базовый скрипт с проверками
```bash
python3 run_basic.py
```

После запуска откройте браузер и перейдите по адресу: http://localhost:8000

## Структура проекта

```
RabbitERD/
├── main.py                 # Основное FastAPI приложение
├── rabbitmq_client.py      # Клиент для работы с RabbitMQ Management API
├── config.json            # Конфигурация подключения
├── requirements.txt       # Зависимости Python
├── README.md              # Документация
├── templates/             # HTML шаблоны
│   ├── index.html         # Главная страница
│   └── error.html         # Страница ошибок
└── static/                # Статические файлы
    └── css/
        └── style.css      # Стили
```

## API Эндпоинты

- `GET /` - Главная страница с визуализацией
- `GET /api/topology` - Полная топология RabbitMQ
- `GET /api/exchanges` - Список обменов
- `GET /api/queues` - Список очередей
- `GET /api/bindings` - Список привязок

## Настройка

Все настройки находятся в файле `config.json`:

### RabbitMQ настройки
- `host` - адрес RabbitMQ сервера
- `port` - порт AMQP (обычно 5672)
- `username` - имя пользователя
- `password` - пароль
- `vhost` - виртуальный хост
- `management_port` - порт Management API (обычно 15672)

### Настройки визуализации
- `node_width` - ширина узлов
- `node_height` - высота узлов
- `spacing` - расстояние между узлами
- `colors` - цвета для разных типов элементов

## Использование

1. **Просмотр топологии**: На главной странице отображается интерактивная схема
2. **Информация об элементах**: Кликните на любой узел для просмотра деталей
3. **Управление**: Используйте кнопки для обновления, зума и сброса
4. **Перетаскивание**: Узлы можно перетаскивать для лучшего размещения

## Устранение неполадок

### Ошибка подключения к RabbitMQ
- Убедитесь, что RabbitMQ запущен
- Проверьте настройки в `config.json`
- Убедитесь, что Management Plugin включен
- Проверьте доступность порта 15672

### Ошибка "Cannot read properties of undefined" в браузере
- Проверьте консоль браузера на наличие ошибок
- Убедитесь, что D3.js загружается (проверьте подключение к интернету)
- Приложение автоматически попробует альтернативный CDN
- Проверьте, что RabbitMQ Management API доступен

### Ошибка "No module named 'uvicorn'"
- Установите uvicorn: `pip3 install uvicorn`
- Или установите все зависимости: `pip3 install -r requirements.txt`
- Используйте прямой запуск: `python3 main.py`
- Или используйте скрипт с проверками: `python3 run_basic.py`

### Ошибка "Failed to build installable wheels for aiohttp"
- Проблема совместимости с Python 3.13
- Установите предварительно скомпилированную версию: `pip3 install --only-binary=all aiohttp`
- Или используйте совместимые версии: `pip3 install -r requirements_py313.txt`
- Альтернатива: используйте Python 3.11 или 3.12

### Включение Management Plugin
```bash
rabbitmq-plugins enable rabbitmq_management
```

### Проверка статуса
```bash
rabbitmq-plugins list
```

## Технологии

- **Backend**: Python, FastAPI, aiohttp
- **Frontend**: HTML5, CSS3, JavaScript, D3.js
- **Визуализация**: D3.js с force simulation
- **Стили**: Современный CSS с градиентами и анимациями

## Лицензия

MIT License

## Безопасность

⚠️ **Важно**: Файл `config.json` содержит чувствительные данные (пароли, хосты) и исключен из Git репозитория. 

- Используйте `config.example.json` как шаблон
- Никогда не коммитьте реальные учетные данные
- Для продакшена используйте переменные окружения или внешние системы конфигурации

## Поддержка

При возникновении проблем проверьте:
1. Статус RabbitMQ сервера
2. Настройки в config.json
3. Доступность Management API
4. Логи приложения в консоли

