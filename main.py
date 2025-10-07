from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from rabbitmq_client import RabbitMQClient
from typing import Dict, List, Any
import logging

app = FastAPI(title="RabbitMQ ERD Visualizer")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логирование всех HTTP запросов"""
    start_time = asyncio.get_event_loop().time()
    
    # Пропускаем системные запросы
    if request.url.path.startswith("/.well-known") or request.url.path == "/favicon.ico":
        response = await call_next(request)
        return response
    
    logger.info(f"📥 {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = asyncio.get_event_loop().time() - start_time
    logger.info(f"📤 {response.status_code} - {process_time:.3f}s")
    
    return response

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Загружаем конфигурацию
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Инициализируем клиент RabbitMQ
rabbitmq_client = RabbitMQClient(config)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Главная страница с визуализацией RabbitMQ"""
    try:
        # Получаем данные о топологии RabbitMQ
        topology = await rabbitmq_client.get_topology()
        
        # Убеждаемся, что все поля присутствуют
        if not topology:
            topology = {"exchanges": [], "queues": [], "bindings": [], "connections": []}
        
        # Проверяем наличие обязательных полей
        for field in ["exchanges", "queues", "bindings", "connections"]:
            if field not in topology:
                topology[field] = []
        
        # Если нет данных (RabbitMQ недоступен), добавляем тестовые данные для демонстрации
        if (topology["exchanges"] == [] and topology["queues"] == [] and 
            topology["bindings"] == [] and topology["connections"] == []):
            print("RabbitMQ недоступен, загружаем тестовые данные для демонстрации")
            topology = {
                "exchanges": [
                    {"name": "test.exchange", "vhost": "/", "type": "direct"},
                    {"name": "user.exchange", "vhost": "/", "type": "topic"}
                ],
                "queues": [
                    {"name": "user.queue", "vhost": "/"},
                    {"name": "order.queue", "vhost": "/"},
                    {"name": "notification.queue", "vhost": "/"}
                ],
                "bindings": [
                    {"source": "test.exchange", "destination": "user.queue", "routing_key": "user.*", "destination_type": "queue", "vhost": "/"},
                    {"source": "user.exchange", "destination": "order.queue", "routing_key": "order.create", "destination_type": "queue", "vhost": "/"},
                    {"source": "user.exchange", "destination": "notification.queue", "routing_key": "user.*", "destination_type": "queue", "vhost": "/"}
                ],
                "connections": []
            }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "topology": topology
        })
    except Exception as e:
        print(f"Ошибка получения топологии: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        })

@app.get("/api/topology")
async def get_topology():
    """API эндпоинт для получения топологии RabbitMQ"""
    try:
        topology = await rabbitmq_client.get_topology()
        
        # Если нет данных (RabbitMQ недоступен), добавляем тестовые данные для демонстрации
        if (topology["exchanges"] == [] and topology["queues"] == [] and 
            topology["bindings"] == [] and topology["connections"] == []):
            print("RabbitMQ недоступен, загружаем тестовые данные для демонстрации")
            topology = {
                "exchanges": [
                    {"name": "test.exchange", "vhost": "/", "type": "direct"},
                    {"name": "user.exchange", "vhost": "/", "type": "topic"}
                ],
                "queues": [
                    {"name": "user.queue", "vhost": "/"},
                    {"name": "order.queue", "vhost": "/"},
                    {"name": "notification.queue", "vhost": "/"}
                ],
                "bindings": [
                    {"source": "test.exchange", "destination": "user.queue", "routing_key": "user.*", "destination_type": "queue", "vhost": "/"},
                    {"source": "user.exchange", "destination": "order.queue", "routing_key": "order.create", "destination_type": "queue", "vhost": "/"},
                    {"source": "user.exchange", "destination": "notification.queue", "routing_key": "user.*", "destination_type": "queue", "vhost": "/"}
                ],
                "connections": []
            }
        
        return {"status": "success", "data": topology}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/exchanges")
async def get_exchanges():
    """API эндпоинт для получения списка обменов"""
    try:
        exchanges = await rabbitmq_client.get_exchanges()
        return {"status": "success", "data": exchanges}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/queues")
async def get_queues():
    """API эндпоинт для получения списка очередей"""
    try:
        queues = await rabbitmq_client.get_queues()
        return {"status": "success", "data": queues}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/bindings")
async def get_bindings():
    """API эндпоинт для получения списка привязок"""
    try:
        bindings = await rabbitmq_client.get_bindings()
        return {"status": "success", "data": bindings}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Обработка системных запросов от браузеров и DevTools
@app.get("/.well-known/apps/ecific/com.chrome.devtools.json")
async def chrome_devtools():
    """Обработка запросов Chrome DevTools"""
    return {"status": "not_found", "message": "Chrome DevTools configuration not available"}

@app.get("/.well-known/{path:path}")
async def well_known(path: str):
    """Обработка запросов .well-known"""
    return {"status": "not_found", "message": f"Resource not found: {path}"}

@app.get("/favicon.ico")
async def favicon():
    """Обработка запросов favicon"""
    from fastapi.responses import Response
    return Response(status_code=204)

@app.get("/robots.txt")
async def robots():
    """Обработка запросов robots.txt"""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse("User-agent: *\nDisallow: /api/")

# Обработка всех остальных запросов
@app.get("/{path:path}")
async def catch_all(path: str):
    """Обработка всех остальных GET запросов"""
    if path.startswith("api/"):
        return {"status": "error", "message": f"API endpoint not found: {path}"}
    return {"status": "not_found", "message": f"Page not found: {path}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

