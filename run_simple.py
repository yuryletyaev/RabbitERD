#!/usr/bin/env python3
"""
Простой скрипт для запуска RabbitMQ ERD Visualizer без uvicorn
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
        # Импортируем и запускаем приложение
        from main import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Попробуйте установить зависимости:")
        print("   pip3 install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
