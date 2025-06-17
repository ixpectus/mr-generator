#!/bin/bash

# Скрипт для активации виртуального окружения и запуска команд

VENV_NAME="venv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Переходим в корень проекта
cd "$PROJECT_DIR"

if [ ! -d "$VENV_NAME" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "💡 Запустите: make setup"
    exit 1
fi

# Активируем виртуальное окружение
source "$VENV_NAME/bin/activate"

echo "✅ Виртуальное окружение активировано"
echo "💡 Для деактивации используйте: deactivate"

# Если передали аргументы, выполняем команду
if [ $# -gt 0 ]; then
    echo "🚀 Выполняем: $@"
    "$@"
else
    # Запускаем новую оболочку с активированным venv
    echo "🐚 Запуск новой оболочки с активированным venv..."
    echo "   Для выхода используйте: exit"
    exec "$SHELL"
fi
