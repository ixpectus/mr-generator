#!/bin/bash

# Быстрый старт для MR Generator
# Этот скрипт поможет новым пользователям быстро настроить и протестировать проект

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "🚀 Быстрый старт MR Generator"
echo "=============================="

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Пожалуйста, установите Python 3.8+."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Python версия: $PYTHON_VERSION"

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "🐍 Создание виртуального окружения..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "✅ Виртуальное окружение уже существует"
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Обновляем pip
echo "📦 Обновление pip..."
pip install --upgrade pip --quiet

# Устанавливаем проект
echo "📦 Установка проекта..."
pip install -e . --quiet

echo "✅ Установка завершена!"
echo ""

# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "🔧 Создание .env файла из шаблона..."
        cp .env.example .env
        echo "✅ Файл .env создан"
        echo "⚠️  ВАЖНО: Отредактируйте .env и добавьте ваши API ключи!"
        echo ""
    else
        echo "⚠️  Файл .env.example не найден. Создайте .env файл вручную."
    fi
else
    echo "✅ Файл .env уже существует"
fi

# Запускаем базовые тесты
echo "🧪 Запуск базовых тестов..."
if python -m pytest tests/test_basic.py -v --tb=short; then
    echo "✅ Базовые тесты прошли успешно!"
else
    echo "⚠️  Некоторые тесты не прошли, но это не критично для начала работы"
fi

echo ""
echo "🎉 Настройка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте .env файл и добавьте API ключи"
echo "2. Активируйте виртуальное окружение: source venv/bin/activate"
echo "3. Попробуйте команды:"
echo "   - make help                    # Справка по командам"
echo "   - make demo                    # Демо-запуск"
echo "   - python -m mr_generator.cli --help  # Справка по CLI"
echo ""
echo "📚 Документация: README.md"
echo "🐛 Проблемы? Проверьте docs/MANUAL_TESTING_GUIDE.md"
echo ""
echo "Удачной работы! 🚀"
