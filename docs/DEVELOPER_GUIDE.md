# Руководство разработчика

## 🚀 Быстрый старт для разработчиков

### 1. Клонирование и настройка

```bash
git clone <repository_url>
cd mr-generator

# Автоматическая настройка
./scripts/quick-start.sh

# Или ручная настройка
make setup
make install-dev
```

### 2. Активация виртуального окружения

```bash
# Способ 1: Напрямую
source venv/bin/activate

# Способ 2: Через скрипт
./scripts/activate-venv.sh

# Способ 3: Через скрипт с командой
./scripts/activate-venv.sh python -m mr_generator.cli --help
```

### 3. Команды разработки

```bash
# Тестирование
make test              # Базовые тесты
make test-cov          # Тесты с покрытием кода

# Качество кода
make format            # Форматирование (black)
make format-check      # Проверка форматирования
make type-check        # Проверка типов (mypy)
make lint-all          # Полная проверка кода

# Сборка
make build             # Создание пакета для распространения

# Очистка
make clean             # Очистка временных файлов
make clean-venv        # Удаление venv
make clean-all         # Полная очистка
```

## 🏗️ Архитектура проекта

### Структура кода

```
src/mr_generator/
├── __init__.py              # Инициализация пакета
├── cli.py                   # CLI интерфейс
├── config.py                # Конфигурация и константы
├── core/                    # Основная логика
│   ├── __init__.py
│   ├── base_provider.py     # Базовый класс провайдеров
│   └── git_helper.py        # Утилиты для работы с Git
└── providers/               # Провайдеры LLM
    ├── __init__.py
    ├── deepseek_provider.py # Провайдер DeepSeek
    └── gigachat_provider.py # Провайдер GigaChat
```

### Принципы архитектуры

1. **Модульность**: Каждый провайдер LLM - отдельный модуль
2. **Расширяемость**: Легко добавлять новые провайдеры
3. **Разделение ответственности**: CLI, логика, конфигурация разделены
4. **Тестируемость**: Модули легко тестировать изолированно

## 🔧 Добавление нового провайдера

### 1. Создайте файл провайдера

```python
# src/mr_generator/providers/newprovider_provider.py
from ..core.base_provider import LLMProvider

class NewProviderProvider(LLMProvider):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        # Инициализация специфичная для провайдера
    
    def generate_description(self, diff_content: str, branch_name: str, **kwargs) -> str:
        # Реализация генерации описания
        pass
    
    def get_model_name(self) -> str:
        return "NewProvider-Model"
```

### 2. Обновите конфигурацию

```python
# config.py
DEFAULT_CONFIGS = {
    # ...existing providers...
    'newprovider': {
        'model': 'newprovider-model',
        'temperature': 0.7,
        'base_url': 'https://api.newprovider.com/v1',
        'max_tokens': 1000
    }
}
```

### 3. Добавьте в CLI

```python
# cli.py - в функцию create_provider()
elif provider_name == 'newprovider':
    from .providers.newprovider_provider import NewProviderProvider
    return NewProviderProvider(api_key, **provider_config)
```

### 4. Добавьте тесты

```python
# tests/test_providers.py
def test_newprovider_provider():
    from mr_generator.providers.newprovider_provider import NewProviderProvider
    provider = NewProviderProvider("test_key")
    assert provider.get_model_name() == "NewProvider-Model"
```

## 🧪 Тестирование

### Структура тестов

```
tests/
├── __init__.py
├── test_basic.py           # Базовые тесты импортов
├── test_cli.py            # Тесты CLI интерфейса
├── test_providers.py      # Тесты провайдеров
├── test_git_helper.py     # Тесты Git утилит
└── fixtures/              # Тестовые данные
```

### Запуск тестов

```bash
# Все тесты
make test

# Конкретный файл
python -m pytest tests/test_basic.py -v

# С покрытием кода
make test-cov

# Только интеграционные тесты
python -m pytest -m integration

# Только быстрые тесты
python -m pytest -m "not slow"
```

### Создание тестов

```python
import pytest
from mr_generator.providers.deepseek_provider import DeepSeekProvider

class TestDeepSeekProvider:
    def test_initialization(self):
        provider = DeepSeekProvider("test_key")
        assert provider.api_key == "test_key"
    
    @pytest.mark.integration
    def test_api_call(self):
        # Интеграционный тест (требует реальный API ключ)
        pass
```

## 📋 Стандарты кода

### Форматирование

- **Black**: Автоматическое форматирование кода
- **Длина строки**: 88 символов (Black default)
- **Импорты**: Сортировка через isort (встроен в Black)

### Типизация

- **MyPy**: Статическая проверка типов
- **Type hints**: Обязательны для всех функций
- **Pydantic**: Для валидации конфигурации

### Документация

```python
def generate_description(
    self, 
    diff_content: str, 
    branch_name: str, 
    **kwargs
) -> str:
    """
    Генерирует описание MR на основе diff содержимого.
    
    Args:
        diff_content: Содержимое git diff
        branch_name: Имя ветки
        **kwargs: Дополнительные параметры
    
    Returns:
        Сгенерированное описание MR
        
    Raises:
        APIError: При ошибке API запроса
    """
```

## 🔍 Отладка

### Логирование

```python
import logging

logger = logging.getLogger(__name__)

def some_function():
    logger.debug("Отладочная информация")
    logger.info("Информационное сообщение")
    logger.warning("Предупреждение")
    logger.error("Ошибка")
```

### Переменные среды для отладки

```bash
export DEBUG=1                    # Включить отладочный режим
export LOG_LEVEL=DEBUG           # Уровень логирования
export MR_GENERATOR_DEBUG=1      # Специфичные отладочные сообщения
```

### Тестирование API без запросов

```python
# Используйте mock для тестирования без реальных API вызовов
from unittest.mock import patch

@patch('requests.post')
def test_api_call(mock_post):
    mock_post.return_value.json.return_value = {"result": "test"}
    # Ваш тест здесь
```

## 📦 Релизы

### Подготовка релиза

1. Обновите версию в `pyproject.toml`
2. Обновите `CHANGELOG.md`
3. Запустите полное тестирование: `make lint-all && make test`
4. Создайте пакет: `make build`

### Создание тега

```bash
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

## 🤝 Вклад в проект

### Pull Request Checklist

- [ ] Тесты написаны и проходят
- [ ] Код отформатирован (`make format`)
- [ ] Типы проверены (`make type-check`)
- [ ] Документация обновлена
- [ ] CHANGELOG.md обновлен
- [ ] Новые зависимости добавлены в `pyproject.toml`

### Соглашения о коммитах

```
feat: добавлен новый провайдер OpenAI
fix: исправлена ошибка обработки больших diff'ов
docs: обновлена документация API
test: добавлены тесты для GigaChat провайдера
refactor: рефакторинг базового класса провайдера
```

## 📚 Полезные ресурсы

- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
