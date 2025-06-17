# MR Description Generator Makefile

# Переменные
REPO_PATH ?= .
PROVIDER ?= deepseek
BRANCH ?= 
VENV_NAME ?= venv
PYTHON ?= python3
PIP ?= $(VENV_NAME)/bin/pip
PYTHON_VENV ?= $(VENV_NAME)/bin/python

.PHONY: help install test setup clean demo venv venv-check

help: ## Показать справку
	@echo "🤖 MR Description Generator"
	@echo "=========================="
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Переменные:"
	@echo "  REPO_PATH - путь к git репозиторию (по умолчанию: .)"
	@echo "  PROVIDER  - провайдер LLM (по умолчанию: deepseek)"
	@echo "  BRANCH    - ветка для анализа (по умолчанию: текущая)"
	@echo "  VENV_NAME - имя виртуального окружения (по умолчанию: venv)"
	@echo ""
	@echo "Примеры:"
	@echo "  make setup                    # Полная настройка с venv"
	@echo "  make demo REPO_PATH=/path/to/repo"
	@echo "  make save REPO_PATH=/path/to/repo BRANCH=origin/feature-branch"

venv: ## Создать виртуальное окружение
	@echo "🐍 Создание виртуального окружения..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		$(PYTHON) -m venv $(VENV_NAME); \
		echo "✅ Виртуальное окружение '$(VENV_NAME)' создано"; \
	else \
		echo "⚠️  Виртуальное окружение '$(VENV_NAME)' уже существует"; \
	fi
	@echo "💡 Для активации используйте: source $(VENV_NAME)/bin/activate"

venv-check: ## Проверить активацию виртуального окружения
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "❌ Виртуальное окружение не найдено. Запустите: make venv"; \
		exit 1; \
	fi

setup: venv ## Первоначальная настройка проекта с venv
	@echo "🔧 Настройка проекта..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Создан .env файл из шаблона"; \
		echo "⚠️  Отредактируйте .env и добавьте ваши API ключи"; \
	else \
		echo "✅ .env файл уже существует"; \
	fi
	@echo "📦 Обновление pip..."
	$(PIP) install --upgrade pip
	@echo "📦 Установка зависимостей..."
	$(PIP) install -e .
	@echo "✅ Проект настроен! Активируйте venv: source $(VENV_NAME)/bin/activate"

demo: venv-check ## Показать демо с тестовыми данными
	@echo "🎬 Демонстрация работы..."
	@echo "Генерация описания для репозитория: $(REPO_PATH)"
	$(PYTHON_VENV) -m mr_generator.cli --provider $(PROVIDER) --repo-path "$(REPO_PATH)" --dry-run

demo-simple: venv-check ## Простая демонстрация модулей
	@echo "🎬 Проверка модулей..."
	$(PYTHON_VENV) scripts/demo.py

gigachat: venv-check ## Генерация с GigaChat
	$(PYTHON_VENV) -m mr_generator.cli --provider gigachat --repo-path "$(REPO_PATH)"

deepseek: venv-check ## Генерация с DeepSeek  
	$(PYTHON_VENV) -m mr_generator.cli --provider deepseek --repo-path "$(REPO_PATH)"

save: venv-check ## Генерация и сохранение в файл
	@if [ -n "$(BRANCH)" ]; then \
		$(PYTHON_VENV) -m mr_generator.cli --provider $(PROVIDER) --repo-path "$(REPO_PATH)" --branch "$(BRANCH)" --output mr_description.md; \
	else \
		$(PYTHON_VENV) -m mr_generator.cli --provider $(PROVIDER) --repo-path "$(REPO_PATH)" --output mr_description.md; \
	fi
	@echo "✅ Описание сохранено в generated/mr_description.md"

clean: ## Очистить временные файлы
	@echo "🧹 Очистка..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	@echo "✅ Временные файлы удалены"

clean-venv: ## Удалить виртуальное окружение
	@echo "🗑️  Удаление виртуального окружения..."
	rm -rf $(VENV_NAME)
	@echo "✅ Виртуальное окружение удалено"

clean-all: clean clean-venv ## Полная очистка

lint: ## Проверить код линтером
	@echo "🔍 Проверка кода..."
	python -m flake8 --max-line-length=100 --ignore=E203,W503 *.py
	@echo "✅ Проверка завершена"

check: install test ## Полная проверка (установка + тесты)

# Быстрые команды для разных языков
ru: ## Генерация на русском языке
	python mr_generator.py --provider deepseek --language ru

en: ## Генерация на английском языке  
	python mr_generator.py --provider deepseek --language en

# Команды для разных веток
current: ## Анализ текущей ветки
	@echo "📊 Анализ текущей ветки:"
	@git branch --show-current
	python mr_generator.py --provider deepseek

main: ## Анализ относительно main
	python mr_generator.py --provider deepseek --base-branch main

master: ## Анализ относительно master
	python mr_generator.py --provider deepseek --base-branch master

develop: ## Анализ относительно develop
	python mr_generator.py --provider deepseek --base-branch develop

# Команды для разработки
install: venv-check ## Установить зависимости
	@echo "📦 Установка зависимостей..."
	$(PIP) install -e .
	@echo "✅ Зависимости установлены"

install-dev: venv-check ## Установить зависимости для разработки
	@echo "📦 Установка зависимостей для разработки..."
	$(PIP) install -e ".[dev]"
	@echo "✅ Зависимости для разработки установлены"

test: venv-check ## Запустить тесты
	@echo "🧪 Запуск тестов..."
	$(PYTHON_VENV) -m pytest tests/ -v
	@echo "✅ Тесты завершены"

test-cov: venv-check ## Запустить тесты с покрытием
	@echo "🧪 Запуск тестов с покрытием..."
	$(PYTHON_VENV) -m pytest tests/ --cov=src/mr_generator --cov-report=html --cov-report=term
	@echo "✅ Тесты с покрытием завершены"

format: venv-check ## Форматировать код
	@echo "✨ Форматирование кода..."
	$(PYTHON_VENV) -m black src/ tests/
	@echo "✅ Код отформатирован"

format-check: venv-check ## Проверить форматирование
	@echo "🔍 Проверка форматирования..."
	$(PYTHON_VENV) -m black --check src/ tests/
	@echo "✅ Проверка форматирования завершена"

type-check: venv-check ## Проверить типы
	@echo "🔍 Проверка типов..."
	$(PYTHON_VENV) -m mypy src/
	@echo "✅ Проверка типов завершена"

lint-all: format-check type-check ## Полная проверка кода
	@echo "🔍 Полная проверка кода..."
	$(PYTHON_VENV) -m flake8 src/ tests/
	@echo "✅ Полная проверка завершена"

build: venv-check ## Собрать пакет
	@echo "🏗️ Сборка пакета..."
	$(PYTHON_VENV) -m build
	@echo "✅ Пакет собран"
