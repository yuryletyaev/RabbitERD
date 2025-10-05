from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import asyncio
from rabbitmq_client import RabbitMQClient
from typing import Dict, List, Any

app = FastAPI(title="RabbitMQ ERD Visualizer")

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
        return templates.TemplateResponse("index.html", {
            "request": request,
            "topology": topology
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        })

@app.get("/api/topology")
async def get_topology():
    """API эндпоинт для получения топологии RabbitMQ"""
    try:
        topology = await rabbitmq_client.get_topology()
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

