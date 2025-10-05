#!/usr/bin/env python3
"""
Скрипт для запуска RabbitMQ ERD Visualizer
"""
import uvicorn
import sys
import os

def main():
    """Запуск приложения"""
    print("🚀 Запуск RabbitMQ ERD Visualizer...")
    print("📊 Откройте браузер: http://localhost:8000")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
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
        sys.exit(1)

if __name__ == "__main__":
    main()
