# 🚀 Быстрый старт

Инструкция для быстрого начала работы с MR Description Generator.

## 1. Подготовка

```bash
# Перейдите в директорию проекта
cd /path/to/mr-generator

# Создайте .env файл с API ключами
cp .env.example .env
# Отредактируйте .env и добавьте ваши ключи
```

## 2. Тестирование

```bash
# Быстрое тестирование (использует AI-experiments как пример)
./test_demo.sh

# Тестирование с вашим репозиторием
./quickstart.sh /path/to/your/repo
```

## 3. Использование

```bash
# Тестовый запуск (без API запросов)
python -m src.mr_generator.cli --provider deepseek --repo-path /path/to/repo --dry-run

# Реальная генерация
python -m src.mr_generator.cli --provider deepseek --repo-path /path/to/repo

# С сохранением в файл
python -m src.mr_generator.cli --provider deepseek --repo-path /path/to/repo --output description.md
```

## 4. Makefile команды

```bash
# Демо с dry-run
make demo REPO_PATH=/path/to/repo

# Генерация с DeepSeek
make deepseek REPO_PATH=/path/to/repo

# Генерация с GigaChat
make gigachat REPO_PATH=/path/to/repo

# Справка
make help
```

## 🔑 API Ключи

### DeepSeek
1. Зарегистрируйтесь на https://platform.deepseek.com/
2. Создайте API ключ в личном кабинете
3. Добавьте в .env: `DEEPSEEK_API_KEY=your_key`

### GigaChat
1. Зарегистрируйтесь на https://developers.sber.ru/docs/ru/gigachat/api/overview
2. Получите авторизационные данные
3. Добавьте в .env: `GIGACHAT_API_KEY=your_key`

## 🆘 Проблемы?

- **Нет API ключей?** Используйте `--dry-run` для тестирования
- **Ошибки зависимостей?** Запустите `pip install -r requirements.txt`
- **Git ошибки?** Убедитесь, что указанная директория - git репозиторий

## 📚 Полная документация

См. [README.md](README.md) для детальной информации.
