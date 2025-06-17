# Инструкция по ручному тестированию MR Generator

## 🎯 Обзор

Эта инструкция поможет вам протестировать все функции MR Generator и диагностировать возможные проблемы.

## 📋 Предварительные требования

### 1. Проверка окружения
```bash
# Убедитесь, что вы в правильной директории проекта
cd /path/to/mr-generator

# Проверьте наличие Python 3
python3 --version

# Проверьте установленные зависимости
pip3 list | grep -E "(requests|gitpython|rich|pydantic|python-dotenv)"
```

### 2. Проверка файлов проекта
```bash
# Проверьте основные файлы
ls -la src/mr_generator/ .env* pyproject.toml

# Должны быть файлы:
# - src/mr_generator/cli.py (основной CLI)
# - src/mr_generator/providers/ (провайдеры)
# - src/mr_generator/core/ (утилиты)
# - .env (конфигурация)
```

## 🔧 Этап 1: Диагностика API подключений

### 1.1 Проверка GigaChat API

```bash
# Быстрый тест подключения
python3 scripts/quick_gigachat_test.py
```

**Ожидаемые результаты:**
- ✅ **Успех (200)**: API ключ действителен, токен получен
- ❌ **401 Unauthorized**: Неверный или устаревший API ключ
- ❌ **Timeout**: Проблемы с сетью или заблокирован доступ
- ❌ **Connection Error**: Проблемы с DNS или firewall

### 1.2 Обновление API ключа GigaChat (если нужно)

1. Перейдите на https://developers.sber.ru/studio/workspaces
2. Войдите в свой аккаунт
3. Выберите ваш проект
4. Скопируйте новый ключ авторизации
5. Обновите файл `.env`:

```bash
# Откройте файл .env
nano .env

# Замените строку:
GIGACHAT_API_KEY=ваш_новый_ключ_здесь
```

### 1.3 Тест после обновления ключа

```bash
# Повторите тест
python3 quick_gigachat_test.py
```

## 🧪 Этап 2: Базовое тестирование функциональности

### 2.1 Проверка CLI интерфейса

```bash
# Проверка справки
python -m src.mr_generator.cli --help

# Должен показать все доступные параметры
```

### 2.2 Dry-run тестирование

```bash
# Тест с dry-run (без реальных API запросов)
python -m src.mr_generator.cli \
  --repo-path /path/to/test/repo \
  --branch feature/test-branch \
  --base-branch master \
  --provider gigachat \
  --dry-run
```

**Ожидаемый результат:**
- Показывает информацию о репозитории
- Анализирует diff между ветками
- Выводит статистику изменений
- Показывает mock-описание MR

### 2.3 Тестирование различных параметров

```bash
# Тест с английским языком
python -m src.mr_generator.cli \
  --repo-path /path/to/test/repo \
  --branch feature/test-branch \
  --provider gigachat \
  --language en \
  --dry-run

# Тест без технических деталей
python -m src.mr_generator.cli \
  --repo-path /path/to/test/repo \
  --branch feature/test-branch \
  --provider gigachat \
  --no-technical \
  --dry-run

# Тест с сохранением в файл
python -m src.mr_generator.cli \
  --repo-path /path/to/test/repo \
  --branch feature/test-branch \
  --provider gigachat \
  --output test_description.md \
  --dry-run
```

## 🚀 Этап 3: Реальное тестирование с API

### 3.1 Тест с маленьким diff

```bash
# Найдите ветку с небольшими изменениями
cd /path/to/test/repo
git branch -a
git diff master..feature/small-changes --stat

# Вернитесь в проект
cd /path/to/mr-generator

# Тест с реальным API (если ключ работает)
python -m src.mr_generator.cli \
  --repo-path /path/to/test/repo \
  --branch feature/small-changes \
  --provider gigachat
```

### 3.2 Анализ результатов

После успешного выполнения проверьте:
- ✅ Описание на русском языке
- ✅ Структурированный формат (заголовки, списки)
- ✅ Логичное содержание
- ✅ Соответствие реальным изменениям

## 🔍 Этап 4: Диагностика проблем

### 4.1 Общие ошибки и решения

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `GIGACHAT_API_KEY не найден` | Отсутствует .env файл | Создайте .env с API ключом |
| `credentials doesn't match` | Неверный API ключ | Обновите ключ в личном кабинете |
| `Timeout` | Проблемы с сетью | Проверьте интернет, VPN |
| `ModuleNotFoundError` | Отсутствуют зависимости | `pip3 install -r requirements.txt` |
| `Нет изменений в ветке` | Неверные ветки | Проверьте существование веток |

### 4.2 Диагностические команды

```bash
# Проверка зависимостей
python3 -c "import requests, git, rich, pydantic, dotenv; print('Все модули доступны')"

# Проверка git репозитория
cd /path/to/test/repo
git status
git log --oneline -5

# Проверка .env файла
cat .env
```

### 4.3 Детальная диагностика GigaChat

```bash
# Запуск полной диагностики
python3 scripts/quick_gigachat_test.py
```

## 📊 Этап 5: Тестирование различных сценариев

### 5.1 Различные типы изменений

```bash
# 1. Ветка с новыми файлами
python -m src.mr_generator.cli --repo-path /path/to/repo --branch feature/new-files --provider gigachat --dry-run

# 2. Ветка с изменениями кода
python -m src.mr_generator.cli --repo-path /path/to/repo --branch bugfix/critical-fix --provider gigachat --dry-run

# 3. Ветка с документацией
python -m src.mr_generator.cli --repo-path /path/to/repo --branch docs/update-readme --provider gigachat --dry-run
```

### 5.2 Различные размеры diff

```bash
# Маленький diff (< 1000 строк)
git diff master..small-branch | wc -l

# Средний diff (1000-5000 строк)
git diff master..medium-branch | wc -l

# Большой diff (> 5000 строк) - может потребовать разбиения
git diff master..large-branch | wc -l
```

## 🎛️ Этап 6: Настройка параметров

### 6.1 Оптимизация параметров модели

```bash
# Более креативный ответ
python -m src.mr_generator.cli --provider gigachat --temperature 0.9 --dry-run

# Более консервативный ответ
python -m src.mr_generator.cli --provider gigachat --temperature 0.3 --dry-run

# Короткие описания
python -m src.mr_generator.cli --provider gigachat --max-tokens 500 --dry-run

# Подробные описания
python -m src.mr_generator.cli --provider gigachat --max-tokens 2000 --dry-run
```

## 📝 Этап 7: Документирование результатов

### 7.1 Создание отчета о тестировании

```bash
# Создайте файл с результатами
cat > test_results.md << 'EOF'
# Результаты тестирования MR Generator

## Дата тестирования
$(date)

## Тестовая среда
- OS: $(uname -s)
- Python: $(python3 --version)
- Git: $(git --version)

## Результаты тестов

### API подключения
- [ ] GigaChat: Успех/Ошибка
- [ ] DeepSeek: Не тестировался

### Функциональные тесты
- [ ] Dry-run: Успех/Ошибка
- [ ] Реальная генерация: Успех/Ошибка
- [ ] Различные языки: Успех/Ошибка

### Проблемы
1. Описание проблемы
2. Описание проблемы

### Рекомендации
1. Рекомендация
2. Рекомендация
EOF
```

## 🚨 Критические проверки

Перед завершением тестирования убедитесь:

- [ ] API ключ GigaChat действителен
- [ ] Все зависимости установлены
- [ ] Git репозиторий доступен
- [ ] CLI интерфейс работает корректно
- [ ] Dry-run режим функционирует
- [ ] Генерируется осмысленное описание MR
- [ ] Файлы сохраняются корректно

## 🔄 Следующие шаги

1. **При успешном тестировании**: Переходите к реальному использованию
2. **При проблемах с API**: Обновите ключи или свяжитесь с поддержкой
3. **При функциональных проблемах**: Проверьте код и зависимости

---

## 📞 Поддержка

При возникновении проблем:
1. Запустите диагностические скрипты
2. Проверьте логи ошибок
3. Обратитесь к документации API провайдеров
4. Создайте issue с подробным описанием проблемы
