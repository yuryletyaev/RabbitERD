#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы RabbitMQ ERD Visualizer
"""
import asyncio
import json
from rabbitmq_client import RabbitMQClient

async def test_connection():
    """Тестирует подключение к RabbitMQ"""
    print("🔍 Тестирование подключения к RabbitMQ...")
    
    try:
        # Загружаем конфигурацию
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Создаем клиент
        client = RabbitMQClient(config)
        
        # Тестируем получение данных
        print("📊 Получение обменов...")
        exchanges = await client.get_exchanges()
        print(f"✅ Найдено обменов: {len(exchanges)}")
        
        print("📊 Получение очередей...")
        queues = await client.get_queues()
        print(f"✅ Найдено очередей: {len(queues)}")
        
        print("📊 Получение привязок...")
        bindings = await client.get_bindings()
        print(f"✅ Найдено привязок: {len(bindings)}")
        
        print("📊 Получение полной топологии...")
        topology = await client.get_topology()
        print(f"✅ Топология получена: {len(topology.get('connections', []))} связей")
        
        print("\n🎉 Все тесты пройдены успешно!")
        print("🚀 Можете запускать приложение: python run.py")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\n🔧 Возможные решения:")
        print("1. Убедитесь, что RabbitMQ запущен")
        print("2. Проверьте настройки в config.json")
        print("3. Убедитесь, что Management Plugin включен")
        print("4. Проверьте доступность порта 15672")

if __name__ == "__main__":
    asyncio.run(test_connection())
