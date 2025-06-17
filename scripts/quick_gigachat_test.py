#!/usr/bin/env python3
"""
Простой тест GigaChat API
"""

import os
import sys
import requests
import uuid
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные окружения из конкретного файла
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def quick_test():
    """Быстрый тест GigaChat API"""
    
    print("🔍 Диагностика загрузки .env файла...")
    print(f"📁 Текущая директория: {os.getcwd()}")
    print(f"📄 Путь к .env файлу: {env_path}")
    print(f"📄 Абсолютный путь: {env_path.resolve()}")
    print(f"📄 .env файл существует: {env_path.exists()}")
    
    # Проверяем другие возможные .env файлы
    possible_env_files = [
        Path('.env'),
        Path('/.env'),
        Path.home() / '.env',
        Path(__file__).parent / '.env',
        Path(__file__).parent.parent / '.env',
        Path(os.getcwd()) / '.env'
    ]
    
    print("\n🔍 Проверяем все возможные .env файлы:")
    for env_file in possible_env_files:
        abs_path = env_file.resolve()
        exists = env_file.exists()
        print(f"  {'✅' if exists else '❌'} {abs_path}")
        if exists:
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    if 'GIGACHAT_API_KEY=' in content:
                        # Находим строку с ключом
                        for line in content.split('\n'):
                            if line.strip().startswith('GIGACHAT_API_KEY='):
                                key = line.split('=', 1)[1].strip()
                                print(f"    🔑 Содержит ключ: {key[:15]}...{key[-15:]}")
                                break
            except Exception as e:
                print(f"    ❌ Ошибка чтения: {e}")
    
    # Проверяем переменные окружения
    print(f"\n🌐 Переменная окружения GIGACHAT_API_KEY:")
    env_key = os.environ.get('GIGACHAT_API_KEY')
    if env_key:
        print(f"  ✅ Найдена: {env_key[:15]}...{env_key[-15:]}")
    else:
        print(f"  ❌ Не найдена")
    
    # Принудительно читаем ключ прямо из файла, игнорируя dotenv
    print(f"\n🔧 Принудительно читаем ключ из файла...")
    api_key = None
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip().startswith('GIGACHAT_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    print(f"📄 Ключ загружен напрямую из файла: {api_key[:15]}...{api_key[-15:]}")
                    break
    
    if not api_key:
        print("❌ GIGACHAT_API_KEY не найден в файле")
        return False
    print(f"📏 Длина ключа: {len(api_key)} символов")
    
    # Проверим, что это правильный ключ из .env
    expected_ending = "NjczOQ=="  # последние символы из вашего рабочего ключа
    if api_key.endswith(expected_ending):
        print("✅ Используется правильный API ключ")
    else:
        print(f"⚠️  Возможно используется старый ключ. Ожидается окончание: {expected_ending}")
        print(f"   Фактическое окончание: {api_key[-6:]}")
    
    # URL согласно документации
    auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': 'f6e5e1e8-9fd1-4151-9870-e2b265cc3193',
        'Authorization': f'Basic {api_key}'
    }
    
    data = {'scope': 'GIGACHAT_API_PERS'}
    
    print(f"🌐 URL: {auth_url}")
    print(f"🆔 RqUID: {headers['RqUID']}")
    
    # Логируем запрос в curl формате
    print("\n📋 Эквивалентный curl команда:")
    curl_cmd = f"""curl -L -X POST '{auth_url}' \\
  -H 'Content-Type: application/x-www-form-urlencoded' \\
  -H 'Accept: application/json' \\
  -H 'RqUID: {headers['RqUID']}' \\
  -H 'Authorization: Basic {api_key}' \\
  --data-urlencode 'scope=GIGACHAT_API_PERS'"""
    print(curl_cmd)
    print()
    
    print("📡 Отправляем запрос (с allow_redirects=True)...")
    
    try:
        response = requests.post(
            auth_url, 
            headers=headers, 
            data=data, 
            verify=False,
            timeout=10,
            allow_redirects=True
        )
        
        print(f"📊 Статус: {response.status_code}")
        print(f"📄 Полный ответ: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            access_token = result.get('access_token', '')
            print(f"✅ Токен получен: {access_token[:20]}...")
            return True
        else:
            print(f"❌ Ошибка {response.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Простой тест GigaChat API")
    print("=" * 40)
    
    success = quick_test()
    
    print("=" * 40)
    if success:
        print("🎉 Тест прошел успешно!")
        sys.exit(0)
    else:
        print("😞 Тест неудачный")
        sys.exit(1)
