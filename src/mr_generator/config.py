"""
Конфигурация для MR Generator
"""

# Настройки по умолчанию для различных провайдеров
DEFAULT_CONFIGS = {
    "gigachat": {
        "model": "GigaChat",
        "temperature": 0.7,
        "base_url": "https://gigachat.devices.sberbank.ru/api/v1",
        "max_tokens": 1000,
    },
    "deepseek": {
        "model": "deepseek-chat",
        "temperature": 0.7,
        "base_url": "https://api.deepseek.com/v1",
        "max_tokens": 1000,
    },
}

# Шаблоны промптов
PROMPT_TEMPLATES = {
    "basic_ru": """ИНСТРУКЦИЯ: Создай описание merge request БЕЗ вводных фраз и общих слов.

ЗАПРЕЩЕННЫЕ ФРАЗЫ:
- "из diff видно"
- "можно предположить" 
- "были внесены"
- "возможно"
- "вероятно"
- "судя по всему"

Diff для ветки '{branch_name}':
```
{diff_content}
```

СТРОГИЙ ФОРМАТ (начинай именно с ## Изменения):

## Изменения
• [точное техническое изменение]
• [точное техническое изменение]

## Цель
[конкретная цель без общих слов]

## Компоненты
• [название файла/модуля]
• [название файла/модуля]""",

    "basic_en": """INSTRUCTION: Create merge request description WITHOUT filler phrases.

BANNED PHRASES:
- "from the diff we can see"
- "it appears that"
- "seems like"
- "this suggests"
- "based on the changes"

Diff for branch '{branch_name}':
```
{diff_content}
```

STRICT FORMAT:

## Changes
• [specific technical change]
• [specific technical change]

## Purpose
[concrete goal without fluff]

## Components
• [file/module name]
• [file/module name]""",

    "detailed_ru": """ЗАДАЧА: Создать описание MR для '{branch_name}' по ТОЧНОМУ шаблону.

КОНТЕКСТ: {repo_name}, файлов: {changed_files_count}, коммитов: {commits_count}

DIFF:
```
{diff_content}
```

АБСОЛЮТНО ЗАПРЕЩЕНО:
- Любые вводные фразы
- "Данный PR", "В данном", "Этот MR"
- "можно увидеть", "видно что", "судя по"
- Общие формулировки

ОБЯЗАТЕЛЬНЫЙ ФОРМАТ (начинай с ## 📋):

## 📋 Сводка
[Одно конкретное предложение - что добавлено/изменено/удалено]

## 🔧 Изменения

### Код
• [конкретная функция/класс/метод]
• [конкретная функция/класс/метод]

### Конфигурация
• [конкретный файл конфига и что изменено]
• [конкретный файл конфига и что изменено]

### Тесты
• [конкретный тест и что проверяет]
• [конкретный тест и что проверяет]

## 🎯 Цель
[Конкретная техническая цель]

## 🏗️ Технические детали
• [конкретная технология/библиотека]
• [конкретный алгоритм/подход]

## 📁 Ключевые файлы
• `точное_имя_файла` - [что именно изменено]
• `точное_имя_файла` - [что именно изменено]

ПРИМЕР ПРАВИЛЬНОГО ОТВЕТА:

## 📋 Сводка
Добавлена аутентификация через JWT токены

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
• `tests/test_auth.py` - тесты аутентификации""",

    "detailed_en": """TASK: Create MR description for '{branch_name}' following EXACT template.

CONTEXT: {repo_name}, files: {changed_files_count}, commits: {commits_count}

DIFF:
```
{diff_content}
```

STRICTLY FORBIDDEN:
- Any introductory phrases
- "This PR", "This MR", "Based on"
- "We can see", "It appears", "Seems like"
- Vague statements

MANDATORY FORMAT (start with ## 📋):

## 📋 Summary
[One concrete sentence - what was added/changed/removed]

## 🔧 Changes

### Code
• [specific function/class/method]
• [specific function/class/method]

### Configuration
• [specific config file and what changed]
• [specific config file and what changed]

### Tests
• [specific test and what it checks]
• [specific test and what it checks]

## 🎯 Purpose
[Concrete technical goal]

## 🏗️ Technical Details
• [specific technology/library]
• [specific algorithm/approach]

## 📁 Key Files
• `exact_filename` - [what exactly changed]
• `exact_filename` - [what exactly changed]

EXAMPLE OF CORRECT RESPONSE:

## 📋 Summary
Added JWT token authentication

## 🔧 Changes

### Code
• Class `AuthService` with login/logout methods
• Middleware `jwtAuth` for token validation
• Endpoint `/api/auth/login` for authentication

### Configuration
• Variable `JWT_SECRET` in .env
• Timeout `JWT_EXPIRES_IN` = 24h

### Tests
• Test `test_auth_login_success` - validates successful login
• Test `test_jwt_middleware` - validates token verification

## 🎯 Purpose
Protect API endpoints from unauthorized access

## 🏗️ Technical Details
• PyJWT library for token creation
• HS256 algorithm for signing
• Secret storage in environment variables

## 📁 Key Files
• `auth/service.py` - authentication logic
• `middleware/jwt.py` - token validation
• `tests/test_auth.py` - authentication tests""",

    "concise_ru": """СОЗДАЙ максимально лаконичное описание для '{branch_name}'.

ПРАВИЛА:
- Только факты из кода
- Никаких общих фраз
- Максимум 5 слов на пункт
- Начинать с действия (добавлен, удален, изменен)

DIFF:
```
{diff_content}
```

ФОРМАТ:

## Изменения
• [Действие] [что] [где]
• [Действие] [что] [где]

## Цель
[Одно предложение без воды]

## Файлы
• `файл` - [действие]
• `файл` - [действие]

ПРИМЕР:

## Изменения
• Добавлен класс User в models.py
• Удален метод old_auth из auth.py
• Изменена конфигурация в settings.json

## Цель
Упрощение системы аутентификации

## Файлы
• `models.py` - новый класс User
• `auth.py` - удален old_auth
• `settings.json` - обновлена конфигурация""",

    "concise_en": """CREATE ultra-concise description for '{branch_name}'.

RULES:
- Only code facts
- No generic phrases
- Maximum 5 words per bullet
- Start with action (added, removed, changed)

DIFF:
```
{diff_content}
```

FORMAT:

## Changes
• [Action] [what] [where]
• [Action] [what] [where]

## Purpose
[One sentence without fluff]

## Files
• `file` - [action]
• `file` - [action]

EXAMPLE:

## Changes
• Added User class in models.py
• Removed old_auth method from auth.py
• Changed configuration in settings.json

## Purpose
Simplify authentication system

## Files
• `models.py` - added User class
• `auth.py` - removed old_auth
• `settings.json` - updated config""",
}

# Ограничения размера diff для отправки в API
MAX_DIFF_SIZE = 50000  # символов

# Файлы которые нужно исключить из анализа
EXCLUDE_FILES = [
    "*.lock",
    "*.log",
    "*.tmp",
    "*.cache",
    "*.pyc",
    "__pycache__/*",
    "node_modules/*",
    ".git/*",
    "*.min.js",
    "*.min.css",
    "package-lock.json",
    "yarn.lock",
    "Pipfile.lock",
]


class Config:
    """Класс для работы с конфигурацией"""

    @staticmethod
    def get_provider_config(provider_name):
        """Получить конфигурацию для провайдера"""
        return DEFAULT_CONFIGS.get(provider_name, {})

    @staticmethod
    def get_prompt_template(template_name):
        """Получить шаблон промпта"""
        return PROMPT_TEMPLATES.get(template_name, PROMPT_TEMPLATES["basic_ru"])

    @staticmethod
    def get_max_diff_size():
        """Получить максимальный размер diff"""
        return MAX_DIFF_SIZE

    @staticmethod
    def get_exclude_files():
        """Получить список исключаемых файлов"""
        return EXCLUDE_FILES
