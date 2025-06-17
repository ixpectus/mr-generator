# MR Description Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Issues](https://img.shields.io/github/issues/antonpetrosyan/mr-description-generator)](https://github.com/antonpetrosyan/mr-description-generator/issues)

Умный генератор описаний merge request с использованием ИИ моделей GigaChat и DeepSeek.

> 🎯 **Готов к выделению в отдельный репозиторий** - полнофункциональное решение с модульной архитектурой

## 🚀 Возможности

- 🤖 **Поддержка нескольких ИИ провайдеров**: GigaChat, DeepSeek
- 📊 **Умная обработка больших diff'ов**: автоматическое сжатие до 95% от исходного размера
- 🎯 **Автоматическое определение типа MR**: feature, bugfix, refactor, infrastructure, docs
- 📝 **3 типа промптов**: basic (простой), detailed (подробный), concise (краткий)
- 🚫 **Устранение "водянистых" фраз**: строгие шаблоны без общих формулировок
- 🌍 **Многоязычность**: поддержка русского и английского языков
- 🔧 **Модульная архитектура**: легкое добавление новых ИИ провайдеров
- ⚡ **CLI интерфейс**: простое использование из командной строки
- 📁 **Автоматическое сохранение**: результаты сохраняются в папку `generated/`

## 📦 Установка

### Быстрый старт

```bash
# Автоматическая настройка (рекомендуется)
./scripts/quick-start.sh

# Или используйте Makefile
make setup
```

### Ручная установка

```bash
# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка проекта
pip install -e .

# Создание .env файла с API ключами
cp .env.example .env
# Отредактируйте .env файл и добавьте ваши API ключи
```

### Для разработчиков

```bash
# Установка с зависимостями для разработки
make install-dev

# Или вручную
pip install -e ".[dev]"
```

## 🔧 Настройка

### API ключи

Вы можете указать API ключи несколькими способами:

1. **Переменные окружения** (рекомендуется):
```bash
export GIGACHAT_API_KEY="your_gigachat_key"
export DEEPSEEK_API_KEY="your_deepseek_key"
```

2. **Файл .env**:
```
GIGACHAT_API_KEY=your_gigachat_key
DEEPSEEK_API_KEY=your_deepseek_key
```

3. **Параметр командной строки**:
```bash
python -m mr_generator.cli --api-key your_key --provider gigachat
```

### GigaChat

Для получения API ключа GigaChat:
1. Зарегистрируйтесь в [GigaChat API](https://developers.sber.ru/docs/ru/gigachat/api/overview)
2. Получите авторизационные данные
3. Используйте их в формате Base64

### DeepSeek

Для получения API ключа DeepSeek:
1. Зарегистрируйтесь на [DeepSeek Platform](https://platform.deepseek.com/)
2. Создайте API ключ в личном кабинете

## 🎯 Использование

### Быстрый старт с wrapper скриптом

```bash
# Простая генерация
./mr /path/to/your/repo

# С выбором провайдера
./mr -p gigachat /path/to/your/repo

# Сохранение в файл
./mr -o description.md /path/to/your/repo

# Тестовый режим
./mr -d /path/to/your/repo

# Справка по wrapper
./mr --help
```

### Использование через виртуальное окружение

```bash
# Активация виртуального окружения
source venv/bin/activate

# Или используйте скрипт активации
./scripts/activate-venv.sh

# Генерация описания
python -m mr_generator.cli --provider deepseek --repo-path /path/to/your/repo
```

### Использование с Makefile

```bash
# Демо-режим
make demo REPO_PATH=/path/to/repo

# Генерация с GigaChat
make gigachat REPO_PATH=/path/to/repo

# Генерация с DeepSeek
make deepseek REPO_PATH=/path/to/repo
```

### Базовое использование

```bash
# Генерация для текущей ветки с GigaChat (подробный формат)
python -m mr_generator.cli --provider gigachat --repo-path /path/to/your/repo

# Краткое описание без воды
python -m mr_generator.cli --provider gigachat --repo-path /path/to/your/repo --prompt-type concise

# Генерация для конкретной ветки с DeepSeek
python -m mr_generator.cli --branch feature/new-api --provider deepseek --repo-path /path/to/your/repo

# Генерация на английском языке
python -m mr_generator.cli --provider deepseek --language en --repo-path /path/to/your/repo --prompt-type detailed
```

### Примеры по типам промптов

```bash
# Краткий формат - минимум слов, максимум информации
python -m mr_generator.cli --provider gigachat --repo-path /path/to/repo --prompt-type concise

# Подробный формат - полная структура с эмодзи и техническими деталями  
python -m mr_generator.cli --provider gigachat --repo-path /path/to/repo --prompt-type detailed

# Базовый формат - простая структура без излишеств
python -m mr_generator.cli --provider gigachat --repo-path /path/to/repo --prompt-type basic
```

### Расширенные параметры

```bash
# Сохранение в файл
python -m mr_generator.cli --provider gigachat --repo-path /path/to/repo --output description.md

# Краткое описание без воды
python -m mr_generator.cli --provider deepseek --repo-path /path/to/repo --prompt-type concise

# Подробное описание на английском
python -m mr_generator.cli --provider gigachat --repo-path /path/to/repo --prompt-type detailed --language en

# Без технических деталей
python -m mr_generator.cli --provider deepseek --repo-path /path/to/repo --no-technical

# Настройка параметров модели
python -m mr_generator.cli --provider gigachat --repo-path /path/to/repo --temperature 0.5 --max-tokens 1500

# Указание базовой ветки
python -m mr_generator.cli --provider deepseek --repo-path /path/to/repo --base-branch develop

# Тестовый режим без API запросов
python -m mr_generator.cli --provider gigachat --repo-path /path/to/repo --dry-run
```

### Полный список параметров

```bash
python -m mr_generator.cli --help
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--branch, -b` | Название ветки | Текущая ветка |
| `--base-branch` | Базовая ветка для сравнения | Автоопределение |
| `--provider, -p` | Провайдер (gigachat/deepseek) | Обязательный |
| `--api-key, -k` | API ключ | Из переменных окружения |
| `--output, -o` | Файл для сохранения | Автосохранение в `generated/` |
| `--language, -l` | Язык (ru/en) | ru |
| `--prompt-type, -t` | Тип промпта (basic/detailed/concise) | detailed |
| `--no-technical` | Исключить технические детали | false |
| `--temperature` | Температура модели (0.0-1.0) | 0.7 |
| `--max-tokens` | Максимум токенов | 1000 |
| `--repo-path, -r` | Путь к Git репозиторию | Обязательный |
| `--dry-run` | Тестовый режим без API запросов | false |

## 📝 Примеры вывода

### Краткий формат (concise)

```markdown
## Изменения
• Добавлен класс AuthService в auth.py
• Удален метод legacy_login из user.py
• Изменена конфигурация в settings.json

## Цель
Упрощение системы аутентификации

## Файлы
• `auth.py` - новый класс AuthService
• `user.py` - удален legacy_login
• `settings.json` - обновлена конфигурация
```

### Подробный формат (detailed)

```markdown
## 📋 Сводка
Добавлена поддержка JWT токенов для аутентификации API

## 🔧 Изменения

### Код
• Класс `AuthService` с методами login/logout
• Middleware `jwtAuth` для проверки токенов
• Эндпоинт `/api/auth/login` для входа

### Конфигурация
• Переменная `JWT_SECRET` в .env
• Таймаут `JWT_EXPIRES_IN` = 24h

### Тесты
• Тест `test_auth_login_success` - проверка успешного входа
• Тест `test_jwt_middleware` - валидация токенов

## 🎯 Цель
Защита API эндпоинтов от неавторизованного доступа

## 🏗️ Технические детали
• Библиотека PyJWT для создания токенов
• Алгоритм HS256 для подписи
• Хранение секрета в переменных окружения

## 📁 Ключевые файлы
• `auth/service.py` - логика аутентификации
• `middleware/jwt.py` - проверка токенов
• `tests/test_auth.py` - тесты аутентификации
```

### Базовый формат (basic)

```markdown
## Изменения
• Добавлена аутентификация через JWT
• Обновлены API эндпоинты
• Создан middleware для проверки токенов

## Цель
Повышение безопасности API

## Компоненты
• auth/service.py
• middleware/jwt.py
```

## 🏗 Архитектура

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

## 🔄 Алгоритм работы

1. **Определение контекста**: Получение информации о репозитории и ветке
2. **Анализ изменений**: Извлечение git diff между веткой и базой
3. **Умная обработка**: Автоматическое сжатие больших diff'ов (>50KB)
4. **Определение типа MR**: Автоматическое распознавание типа изменений
5. **Выбор шаблона**: Подбор подходящего промпта (basic/detailed/concise)
6. **Сбор метаданных**: Получение списка файлов, коммитов, статистики
7. **Генерация промпта**: Формирование строгого запроса без "водянистых" фраз
8. **API запрос**: Отправка запроса в выбранную LLM
9. **Форматирование**: Обработка и валидация ответа
10. **Автосохранение**: Сохранение результата в папку `generated/`

## 🛠 Расширение функциональности

### Добавление нового провайдера

1. Создайте класс, наследующий от `LLMProvider`
2. Реализуйте методы `generate_description()` и `get_model_name()`
3. Добавьте провайдера в `SUPPORTED_PROVIDERS` в `cli.py`

```python
from llm_provider import LLMProvider

class NewProvider(LLMProvider):
    def generate_description(self, diff_content: str, branch_name: str, **kwargs) -> str:
        # Ваша реализация
        pass
    
    def get_model_name(self) -> str:
        return "New-Model-Name"
```

### Настройка промптов

Отредактируйте `src/mr_generator/config.py` для изменения шаблонов промптов или добавления новых.

**Доступные типы промптов:**
- `basic_ru/en` - Простой формат без лишних деталей
- `detailed_ru/en` - Подробный формат с эмодзи и техническими деталями  
- `concise_ru/en` - Максимально краткий формат без "воды"

**Ключевые особенности промптов:**
- Строгие запреты на "водянистые" фразы
- Примеры правильного формата в каждом шаблоне
- Автоматическая подстановка контекстной информации
- Fallback к базовому шаблону при ошибках

## 🚨 Ограничения и особенности

### Ограничения размера
- **Максимальный размер diff**: 50KB (настраивается в `config.py`)
- **Автоматическая оптимизация**: diff'ы >100KB сжимаются до 50KB
- **Умная обработка**: приоритет отдается важным изменениям

### Исключаемые файлы
Следующие типы файлов автоматически исключаются из анализа:
- Lock файлы (`*.lock`, `package-lock.json`, `yarn.lock`)
- Логи и временные файлы (`*.log`, `*.tmp`, `*.cache`)
- Скомпилированные файлы (`*.pyc`, `*.min.js`, `*.min.css`)
- Служебные папки (`__pycache__`, `node_modules`, `.git`)

### Системные требования
- **Python**: 3.8+
- **Git**: установлен и настроен
- **Интернет**: для API запросов к языковым моделям
- **API ключи**: активные ключи для выбранных провайдеров

## 🐛 Решение проблем

### Ошибка аутентификации
```bash
❌ Ошибка: API ключ не найден
```
**Решение:**
- Проверьте правильность API ключей в `.env` файле
- Убедитесь, что ключи активны и имеют необходимые права
- Для GigaChat используйте Base64 формат авторизационных данных

### Нет изменений в ветке
```bash
❌ Ошибка: Нет изменений в ветке относительно базовой ветки
```
**Решение:**
- Убедитесь, что ветка содержит коммиты отличные от базовой ветки
- Проверьте, что вы в правильном Git репозитории
- Попробуйте указать базовую ветку явно: `--base-branch main`

### Слишком большой diff
```bash
🧠 Diff слишком большой! Применяем умную обработку...
```
**Это нормально!** Система автоматически оптимизирует большие diff'ы.
Если результат неудовлетворительный:
- Разбейте изменения на несколько MR
- Настройте `MAX_DIFF_SIZE` в `config.py`
- Исключите ненужные файлы через `.gitignore`

### Проблемы с виртуальным окружением
```bash
ModuleNotFoundError: No module named 'mr_generator'
```
**Решение:**
```bash
# Активируйте виртуальное окружение
source venv/bin/activate
# Переустановите проект
pip install -e .
```

## 📚 Документация

- **[REQUIREMENTS.md](docs/REQUIREMENTS.md)** - полные требования к проекту и критерии приемки
- **[IMPROVED_PROMPTS.md](docs/IMPROVED_PROMPTS.md)** - детали улучшенных промптов и борьба с "водянистыми" фразами
- **[SMART_DIFF_HANDLING.md](docs/SMART_DIFF_HANDLING.md)** - алгоритмы обработки больших diff'ов  
- **[MANUAL_TESTING_GUIDE.md](docs/MANUAL_TESTING_GUIDE.md)** - руководство по тестированию
- **[DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** - руководство для разработчиков
- **[PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - краткое описание архитектуры проекта
- **[CHANGELOG.md](docs/CHANGELOG.md)** - история изменений

### Папка generated/
Все сгенерированные описания автоматически сохраняются в папку `generated/` с временными метками:
- `generated/mr-description-YYYYMMDD-HHMMSS.md` - автоматические имена
- `generated/custom-name.md` - при использовании `--output`
- `generated/README.md` - документация по использованию папки

## 🔗 Полезные ссылки

- [GigaChat API Documentation](https://developers.sber.ru/docs/ru/gigachat/api/overview)
- [DeepSeek API Documentation](https://platform.deepseek.com/api-docs/)
- [Git Documentation](https://git-scm.com/docs)

---

## 🎉 Результаты и качество

### Улучшения в качестве описаний
- ✅ **Устранены "водянистые" фразы** типа "из diff видно", "можно предположить"
- ✅ **Структурированный формат** с четкими разделами  
- ✅ **Конкретные технические детали** вместо общих формулировок
- ✅ **Автоматическое определение типа MR** для подбора оптимального стиля
- ✅ **Многоуровневая система промптов** для разных потребностей

### Тестирование
Проект протестирован на реальных репозиториях с различными типами изменений:
- 🧪 Infrastructure изменения (CI/CD, Docker, Makefile)
- 🧪 Feature добавления (новый функционал)
- 🧪 Bugfix исправления
- 🧪 Refactoring кода

### Производительность
- ⚡ **Умная обработка**: diff'ы до 200KB автоматически оптимизируются
- ⚡ **Быстрая генерация**: среднее время ответа 3-10 секунд
- ⚡ **Надежность**: fallback механизмы и обработка ошибок

---

**Готов к production использованию!** 🚀
