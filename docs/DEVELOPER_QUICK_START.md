# Developer Quick Start

Краткое руководство для разработчиков по настройке и работе с проектом MR Generator.

## 🚀 Быстрый старт

### 1. Клонирование и настройка

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd mr-generator

# Полная настройка (создание venv + установка зависимостей)
make setup

# Установка зависимостей для разработки
make install-dev
```

### 2. Активация виртуального окружения

```bash
# Вариант 1: Стандартная активация
source venv/bin/activate

# Вариант 2: Использование helper скрипта
./scripts/activate-venv.sh

# Вариант 3: Запуск команд через скрипт
./scripts/activate-venv.sh python -m mr_generator.cli --help
```

### 3. Конфигурация API ключей

```bash
# Скопируйте и отредактируйте .env файл
cp .env.example .env

# Добавьте ваши API ключи в .env:
# GIGACHAT_API_KEY=your_gigachat_key
# DEEPSEEK_API_KEY=your_deepseek_key
```

## 🧪 Разработка

### Запуск тестов

```bash
make test          # Базовые тесты
make test-cov      # Тесты с покрытием кода
```

### Качество кода

```bash
make format        # Форматирование кода (Black)
make format-check  # Проверка форматирования
make type-check    # Проверка типов (MyPy)
make lint-all      # Полная проверка качества
```

### Сборка

```bash
make build         # Сборка пакета
make clean         # Очистка временных файлов
make clean-all     # Полная очистка + удаление venv
```

## 🎯 Тестирование функциональности

### Демо режим

```bash
make demo                                    # Демо для текущего репозитория
make demo REPO_PATH=/path/to/other/project   # Демо для другого проекта
```

### Генерация описаний

```bash
make deepseek                               # DeepSeek для текущего проекта
make gigachat REPO_PATH=~/my-project        # GigaChat для указанного проекта
make save PROVIDER=deepseek                 # Сохранение в файл
```

## 📁 Структура проекта

```
src/mr_generator/          # Основной код
├── cli.py                 # CLI интерфейс
├── config.py              # Конфигурация
├── core/                  # Базовая логика
│   ├── base_provider.py   # Базовый класс провайдеров
│   └── git_helper.py      # Git утилиты
└── providers/             # LLM провайдеры
    ├── deepseek_provider.py
    └── gigachat_provider.py

tests/                     # Тесты
docs/                      # Документация
scripts/                   # Вспомогательные скрипты
```

## 🔧 Полезные команды

| Команда | Описание |
|---------|----------|
| `make help` | Показать все доступные команды |
| `make setup` | Первоначальная настройка проекта |
| `make install-dev` | Установка dev зависимостей |
| `make test-cov` | Тесты с покрытием |
| `make lint-all` | Полная проверка кода |
| `make demo` | Демонстрация работы |
| `make clean-all` | Полная очистка |

## 🐛 Отладка

### Проверка установки

```bash
# Проверка виртуального окружения
source venv/bin/activate
python --version
pip list | grep mr-generator

# Проверка модуля
python -c "import mr_generator; print('OK')"
python -m mr_generator.cli --help
```

### Логи и диагностика

```bash
# Запуск в debug режиме
python -m mr_generator.cli --provider deepseek --repo-path . --dry-run

# Проверка git репозитория
git status
git log --oneline -5
```

## 📋 Чек-лист для разработчика

- [ ] Виртуальное окружение создано (`make venv`)
- [ ] Зависимости установлены (`make install-dev`)
- [ ] API ключи настроены (`.env` файл)
- [ ] Тесты проходят (`make test`)
- [ ] Код отформатирован (`make format`)
- [ ] Нет ошибок линтера (`make lint-all`)
- [ ] Демо работает (`make demo`)

## 🤝 Участие в разработке

1. Создайте feature ветку
2. Внесите изменения
3. Запустите тесты и проверки качества
4. Создайте Pull Request

```bash
git checkout -b feature/your-feature
# ... ваши изменения ...
make lint-all
make test-cov
git commit -m "Add: your feature description"
git push origin feature/your-feature
```
