#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работоспособности MR Generator
"""

import os
import sys
from pathlib import Path

# Добавляем текущую директорию в Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from git_helper import GitHelper

def test_environment():
    """Проверка окружения и конфигурации"""
    print("🧪 Тестирование окружения MR Generator")
    print("=" * 50)
    
    # Проверка конфигурации
    try:
        config = Config()
        print("✅ Конфигурация загружена успешно")
        
        # Проверка API ключей
        if hasattr(config, 'gigachat_api_key') and config.gigachat_api_key:
            print("✅ GigaChat API ключ найден")
        else:
            print("❌ GigaChat API ключ не найден")
            
        if hasattr(config, 'deepseek_api_key') and config.deepseek_api_key:
            print("✅ DeepSeek API ключ найден") 
        else:
            print("❌ DeepSeek API ключ не найден")
            
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False
    
    # Проверка Git репозитория
    try:
        git_helper = GitHelper(".")
        current_branch = git_helper.get_current_branch()
        print(f"✅ Git репозиторий найден, текущая ветка: {current_branch}")
        
        # Проверка наличия изменений
        try:
            base_branch = git_helper.get_base_branch(current_branch)
            print(f"✅ Базовая ветка определена: {base_branch}")
            
            diff = git_helper.get_diff(current_branch, base_branch)
            if diff.strip():
                print(f"✅ Найдены изменения ({len(diff)} символов)")
            else:
                print("⚠️  Изменения между ветками не найдены")
                
        except Exception as e:
            print(f"⚠️  Не удалось получить diff: {e}")
            
    except Exception as e:
        print(f"❌ Ошибка Git: {e}")
        return False
    
    print("\n🎯 Готовность к тестированию:")
    
    # Проверка зависимостей
    try:
        import requests
        print("✅ requests установлен")
    except ImportError:
        print("❌ requests не установлен (pip install requests)")
        
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv установлен")
    except ImportError:
        print("❌ python-dotenv не установлен (pip install python-dotenv)")
    
    return True

def test_providers():
    """Тестирование провайдеров LLM"""
    print("\n🤖 Тестирование провайдеров")
    print("=" * 50)
    
    try:
        from gigachat_provider import GigaChatProvider
        from deepseek_provider import DeepSeekProvider
        
        config = Config()
        
        # Тест GigaChat
        if hasattr(config, 'gigachat_api_key') and config.gigachat_api_key != 'your_gigachat_api_key_here':
            try:
                gigachat = GigaChatProvider(config.gigachat_api_key)
                print(f"✅ GigaChat провайдер инициализирован: {gigachat.get_model_name()}")
            except Exception as e:
                print(f"❌ Ошибка GigaChat: {e}")
        else:
            print("⚠️  GigaChat API ключ не настроен")
            
        # Тест DeepSeek  
        if hasattr(config, 'deepseek_api_key') and config.deepseek_api_key != 'your_deepseek_api_key_here':
            try:
                deepseek = DeepSeekProvider(config.deepseek_api_key)
                print(f"✅ DeepSeek провайдер инициализирован: {deepseek.get_model_name()}")
            except Exception as e:
                print(f"❌ Ошибка DeepSeek: {e}")
        else:
            print("⚠️  DeepSeek API ключ не настроен")
            
    except ImportError as e:
        print(f"❌ Ошибка импорта провайдеров: {e}")

def test_cli():
    """Тестирование CLI интерфейса"""
    print("\n💻 Тестирование CLI")
    print("=" * 50)
    
    try:
        # Проверка импорта основного модуля
        import mr_generator
        print("✅ mr_generator модуль импортирован успешно")
        
        # Тест парсинга аргументов
        if hasattr(mr_generator, 'parse_arguments'):
            print("✅ Функция parse_arguments найдена")
        
        print("\n📋 Для полного тестирования запустите:")
        print("python mr_generator.py --help")
        
    except ImportError as e:
        print(f"❌ Ошибка импорта mr_generator: {e}")

if __name__ == "__main__":
    print("🚀 Запуск тестов MR Description Generator\n")
    
    success = test_environment()
    if success:
        test_providers()
        test_cli()
    
    print("\n" + "=" * 50)
    print("🏁 Тестирование завершено")
    
    if not success:
        print("\n💡 Убедитесь, что:")
        print("1. Создан .env файл с API ключами")
        print("2. Установлены зависимости: pip install -r requirements.txt")
        print("3. Вы находитесь в Git репозитории")
        sys.exit(1)
    else:
        print("\n🎉 Система готова к использованию!")
