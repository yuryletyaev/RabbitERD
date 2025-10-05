#!/usr/bin/env python3
"""
Скрипт для тестирования API RabbitMQ ERD Visualizer
Позволяет тестировать эндпоинты без браузера
"""
import asyncio
import aiohttp
import json
from pathlib import Path

async def test_api():
    """Тестирование API эндпоинтов"""
    base_url = "http://localhost:8000"
    
    print("🧪 Тестирование API RabbitMQ ERD Visualizer")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        try:
            # Тест главной страницы
            print("📄 Тестирование главной страницы...")
            async with session.get(f"{base_url}/") as response:
                if response.status == 200:
                    print("✅ Главная страница: OK")
                    content = await response.text()
                    if "RabbitMQ ERD Visualizer" in content:
                        print("✅ Заголовок найден")
                    else:
                        print("⚠️  Заголовок не найден")
                else:
                    print(f"❌ Главная страница: {response.status}")
            
            # Тест API топологии
            print("\n🔗 Тестирование API топологии...")
            async with session.get(f"{base_url}/api/topology") as response:
                if response.status == 200:
                    print("✅ API топологии: OK")
                    data = await response.json()
                    print(f"📊 Данные: {len(data.get('exchanges', []))} обменов, {len(data.get('queues', []))} очередей")
                else:
                    print(f"❌ API топологии: {response.status}")
            
            # Тест статических файлов
            print("\n📁 Тестирование статических файлов...")
            async with session.get(f"{base_url}/static/style.css") as response:
                if response.status == 200:
                    print("✅ CSS файл: OK")
                else:
                    print(f"❌ CSS файл: {response.status}")
            
            print("\n🎉 Тестирование завершено!")
            
        except aiohttp.ClientConnectorError:
            print("❌ Не удается подключиться к серверу")
            print("💡 Убедитесь, что приложение запущено на http://localhost:8000")
        except Exception as e:
            print(f"❌ Ошибка тестирования: {e}")

def main():
    """Главная функция"""
    print("🚀 Запуск тестирования API...")
    print("💡 Убедитесь, что приложение запущено: python3 main.py")
    print("-" * 50)
    
    try:
        asyncio.run(test_api())
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
