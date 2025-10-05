#!/usr/bin/env python3
"""
Скрипт для отладки RabbitMQ ERD Visualizer
Работает в любой IDE, включая PyCharm Community
"""
import sys
import os
import asyncio
from pathlib import Path

def main():
    """Запуск приложения в режиме отладки"""
    print("🐛 Запуск в режиме отладки...")
    print("📊 Откройте браузер: http://localhost:8000")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        # Добавляем текущую директорию в путь
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Импортируем приложение
        from main import app
        print("✅ Приложение загружено")
        
        # Импортируем uvicorn
        import uvicorn
        print("✅ Uvicorn загружен")
        
        # Запускаем с отладочными настройками
        uvicorn.run(
            app,
            host="127.0.0.1",  # Локальный хост для отладки
            port=8000,
            reload=True,
            log_level="debug",  # Подробные логи
            access_log=True,    # Логи доступа
            debug=True          # Режим отладки
        )
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Установите зависимости:")
        print("   pip3 install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        print("💡 Попробуйте:")
        print("   1. Установить зависимости: pip3 install -r requirements.txt")
        print("   2. Проверить конфигурацию: python3 test_app.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
