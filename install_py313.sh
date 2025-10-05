#!/bin/bash
# Скрипт для установки зависимостей для Python 3.13

echo "🐍 Установка зависимостей для Python 3.13..."
echo "================================================"

# Проверяем версию Python
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "📋 Версия Python: $python_version"

if [[ "$python_version" == "3.13" ]]; then
    echo "⚠️  Обнаружен Python 3.13 - возможны проблемы с компиляцией"
    echo "💡 Устанавливаем предварительно скомпилированные пакеты..."
    
    # Устанавливаем предварительно скомпилированные версии
    pip3 install --only-binary=all fastapi==0.104.1
    pip3 install --only-binary=all uvicorn[standard]==0.24.0
    pip3 install --only-binary=all aiohttp==3.9.1
    pip3 install --only-binary=all jinja2==3.1.2
    pip3 install --only-binary=all python-multipart==0.0.6
    
    echo "✅ Установка завершена!"
    echo "🚀 Теперь можно запустить: python3 main.py"
else
    echo "✅ Python $python_version - стандартная установка"
    pip3 install -r requirements.txt
fi

echo "================================================"
echo "🎉 Готово! Приложение можно запускать."
