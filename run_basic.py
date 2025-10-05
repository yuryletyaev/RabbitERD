#!/usr/bin/env python3
"""
Базовый скрипт для запуска RabbitMQ ERD Visualizer
"""
import sys
import os

def main():
    """Запуск приложения"""
    print("🚀 Запуск RabbitMQ ERD Visualizer...")
    print("📊 Откройте браузер: http://localhost:8000")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        # Проверяем наличие uvicorn
        try:
            import uvicorn
            print("✅ uvicorn найден")
        except ImportError:
            print("❌ uvicorn не найден")
            print("💡 Установите uvicorn:")
            print("   pip3 install uvicorn")
            sys.exit(1)
        
        # Импортируем приложение
        from main import app
        print("✅ Приложение загружено")
        
        # Запускаем сервер
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        print("💡 Попробуйте:")
        print("   1. Установить зависимости: pip3 install -r requirements.txt")
        print("   2. Запустить напрямую: python3 main.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
