#!/usr/bin/env python3
"""
Простой скрипт для разработки без PyCharm Professional
Работает в любой IDE и редакторе
"""
import sys
import os
from pathlib import Path

def main():
    """Запуск приложения для разработки"""
    print("🚀 RabbitMQ ERD Visualizer - Режим разработки")
    print("=" * 50)
    
    # Проверяем зависимости
    print("🔍 Проверка зависимостей...")
    try:
        import fastapi
        print("✅ FastAPI: OK")
    except ImportError:
        print("❌ FastAPI не найден")
        print("💡 Установите: pip3 install fastapi")
        return
    
    try:
        import uvicorn
        print("✅ Uvicorn: OK")
    except ImportError:
        print("❌ Uvicorn не найден")
        print("💡 Установите: pip3 install uvicorn")
        return
    
    try:
        import aiohttp
        print("✅ Aiohttp: OK")
    except ImportError:
        print("❌ Aiohttp не найден")
        print("💡 Установите: pip3 install aiohttp")
        return
    
    # Проверяем конфигурацию
    config_file = Path("config.json")
    if not config_file.exists():
        print("⚠️  Файл config.json не найден")
        print("💡 Создайте config.json на основе config.example.json")
        return
    
    print("✅ Конфигурация: OK")
    
    # Запускаем приложение
    print("\n🚀 Запуск приложения...")
    print("📊 Откройте браузер: http://localhost:8000")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        # Импортируем и запускаем
        from main import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        print("💡 Попробуйте:")
        print("   1. Проверить зависимости: pip3 install -r requirements.txt")
        print("   2. Проверить конфигурацию: python3 test_app.py")
        print("   3. Запустить в режиме отладки: python3 debug_app.py")

if __name__ == "__main__":
    main()
