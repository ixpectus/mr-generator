#!/usr/bin/env python3
"""
MR Description Generator

Скрипт для автоматической генерации описаний merge request
на основе git diff с использованием различных языковых моделей.
"""

import argparse
import os
import sys
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Добавляем текущую директорию в путь для импорта
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from .core.git_helper import GitHelper
from .providers.gigachat_provider import GigaChatProvider
from .providers.deepseek_provider import DeepSeekProvider
from .core.base_provider import LLMProvider


class MRDescriptionGenerator:
    """Генератор описаний для Merge Request"""
    
    SUPPORTED_PROVIDERS = {
        'gigachat': GigaChatProvider,
        'deepseek': DeepSeekProvider
    }
    
    def __init__(self, repo_path: str = "."):
        self.git_helper = GitHelper(repo_path)
        self.repo_path = repo_path
    
    def create_provider(self, provider_name: str, api_key: str, **kwargs) -> LLMProvider:
        """Создает провайдера языковой модели"""
        if provider_name not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Неподдерживаемый провайдер: {provider_name}. "
                           f"Доступные: {list(self.SUPPORTED_PROVIDERS.keys())}")
        
        provider_class = self.SUPPORTED_PROVIDERS[provider_name]
        return provider_class(api_key, **kwargs)
    
    def generate_description(
        self,
        branch: str,
        provider_name: str,
        api_key: str,
        base_branch: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Генерирует описание MR
        
        Args:
            branch: Название ветки
            provider_name: Название провайдера (gigachat, deepseek)
            api_key: API ключ
            base_branch: Базовая ветка (определяется автоматически если не указана)
            **kwargs: Дополнительные параметры
            
        Returns:
            Сгенерированное описание
        """
        
        # Проверяем, что мы в git репозитории
        if not self.git_helper.is_git_repo():
            raise Exception("Текущая директория не является Git репозиторием")
        
        # Получаем информацию о репозитории
        repo_info = self.git_helper.get_repo_info()
        print(f"📁 Репозиторий: {repo_info.get('repo_name', 'Unknown')}")
        print(f"🌿 Текущая ветка: {repo_info.get('current_branch', 'Unknown')}")
        
        # Получаем diff
        print(f"🔍 Получаем diff для ветки '{branch}'...")
        diff_content = self.git_helper.get_diff(branch, base_branch)
        
        if not diff_content.strip():
            raise Exception(f"Нет изменений в ветке '{branch}' относительно базовой ветки")
        
        # 🧠 УМНАЯ ОБРАБОТКА БОЛЬШИХ DIFF'ОВ
        original_size = len(diff_content)
        print(f"📏 Размер diff: {original_size:,} символов")
        
        # Определяем стратегию обработки
        if original_size > 100000:  # Больше 100К символов
            print("🧠 Diff слишком большой! Применяем умную обработку...")
            diff_content = self._smart_truncate_diff(diff_content, max_size=50000)
            print(f"📉 Размер после оптимизации: {len(diff_content):,} символов")
        elif original_size > 50000:  # Больше 50К символов
            print("⚡ Применяем легкую оптимизацию...")
            diff_content = self._smart_truncate_diff(diff_content, max_size=30000)
            print(f"📉 Размер после оптимизации: {len(diff_content):,} символов")
        
        # Получаем дополнительную информацию
        changed_files = self.git_helper.get_changed_files(branch, base_branch)
        commit_messages = self.git_helper.get_commit_messages(branch, base_branch)
        
        print(f"📄 Измененных файлов: {len(changed_files)}")
        print(f"📝 Коммитов: {len(commit_messages)}")
        
        # Создаем провайдера и генерируем описание
        provider = self.create_provider(provider_name, api_key, **kwargs)
        print(f"🤖 Используем модель: {provider.get_model_name()}")
        
        # Добавляем дополнительную информацию в kwargs
        kwargs.update({
            'changed_files': changed_files,
            'commit_messages': commit_messages,
            'repo_name': repo_info.get('repo_name', ''),
        })
        
        print("⏳ Генерируем описание...")
        description = provider.generate_description(diff_content, branch, **kwargs)
        
        return description
    
    def _smart_truncate_diff(self, diff_content: str, max_size: int = 50000) -> str:
        """Умно обрезает diff, сохраняя важную информацию"""
        
        if len(diff_content) <= max_size:
            return diff_content
        
        lines = diff_content.split('\n')
        
        # Собираем статистику
        stats = {
            'files_changed': 0,
            'additions': 0,
            'deletions': 0,
            'file_types': {}
        }
        
        important_lines = []
        current_file = None
        files_shown = 0
        max_files_to_show = 15  # Показываем первые 15 файлов
        
        for line in lines:
            # Всегда сохраняем заголовки файлов
            if line.startswith('diff --git'):
                stats['files_changed'] += 1
                if files_shown < max_files_to_show:
                    important_lines.append(line)
                    current_file = line
                    files_shown += 1
                else:
                    break
            
            # Сохраняем метаданные
            elif line.startswith('index ') or line.startswith('---') or line.startswith('+++'):
                if files_shown <= max_files_to_show:
                    important_lines.append(line)
            
            # Сохраняем контекстные заголовки
            elif line.startswith('@@'):
                if files_shown <= max_files_to_show:
                    important_lines.append(line)
            
            # Подсчитываем изменения и сохраняем некоторые
            elif line.startswith('+') and not line.startswith('+++'):
                stats['additions'] += 1
                # Сохраняем первые несколько строк изменений для каждого файла
                if files_shown <= max_files_to_show and len(important_lines) < max_size // 2:
                    important_lines.append(line)
            
            elif line.startswith('-') and not line.startswith('---'):
                stats['deletions'] += 1
                if files_shown <= max_files_to_show and len(important_lines) < max_size // 2:
                    important_lines.append(line)
            
            # Сохраняем контекстные строки (без + или -)
            elif files_shown <= max_files_to_show and len(important_lines) < max_size // 2:
                if len(line.strip()) > 0:  # Пропускаем пустые строки
                    important_lines.append(line)
        
        # Создаем итоговый diff
        result_lines = [
            f"=== УМНОЕ РЕЗЮМЕ DIFF'А ===",
            f"Оригинальный размер: {len(diff_content):,} символов",
            f"Файлов изменено: {stats['files_changed']:,}",
            f"Добавлено строк: {stats['additions']:,}",
            f"Удалено строк: {stats['deletions']:,}",
            f"Показаны первые {min(files_shown, max_files_to_show)} файлов из {stats['files_changed']}",
            "",
            "=== КЛЮЧЕВЫЕ ИЗМЕНЕНИЯ ===",
            ""
        ]
        
        result_lines.extend(important_lines)
        
        if stats['files_changed'] > max_files_to_show:
            result_lines.extend([
                "",
                f"... и еще {stats['files_changed'] - max_files_to_show} файлов не показаны для экономии места",
                "",
                "[АВТОМАТИЧЕСКИ СОКРАЩЕНО ДЛЯ ОБРАБОТКИ ИИ]"
            ])
        
        return '\n'.join(result_lines)
    
    def save_description(self, description: str, output_file: Optional[str] = None):
        """Сохраняет описание в файл"""
        if output_file:
            # Создаем папку generated, если её нет
            generated_dir = Path("generated")
            generated_dir.mkdir(exist_ok=True)
            
            # Если путь не абсолютный и не начинается с generated/, добавляем папку
            output_path = Path(output_file)
            if not output_path.is_absolute() and not str(output_path).startswith("generated/"):
                output_path = generated_dir / output_path
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(description)
            print(f"💾 Описание сохранено в: {output_path}")
        else:
            print("\n" + "="*50)
            print("📋 СГЕНЕРИРОВАННОЕ ОПИСАНИЕ MR:")
            print("="*50)
            print(description)
            print("="*50)


def main():
    """Основная функция CLI"""
    parser = argparse.ArgumentParser(
        description="Генератор описаний Merge Request на основе git diff",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Генерация для текущей ветки с помощью GigaChat
  python mr_generator.py --provider gigachat --repo-path /path/to/your/repo --api-key YOUR_KEY

  # Генерация для конкретной ветки с помощью DeepSeek
  python mr_generator.py --branch feature/new-api --provider deepseek --repo-path /path/to/your/repo --api-key YOUR_KEY

  # Сохранение в файл
  python mr_generator.py --provider gigachat --repo-path /path/to/your/repo --api-key YOUR_KEY --output description.md

  # С дополнительными параметрами
  python mr_generator.py --provider deepseek --repo-path /path/to/your/repo --api-key YOUR_KEY --language en --prompt-type concise

  # Краткое описание на русском
  python mr_generator.py --provider gigachat --repo-path /path/to/your/repo --api-key YOUR_KEY --prompt-type concise

  # Подробное описание на английском
  python mr_generator.py --provider gigachat --repo-path /path/to/your/repo --api-key YOUR_KEY --language en --prompt-type detailed

Переменные окружения:
  GIGACHAT_API_KEY  - API ключ для GigaChat
  DEEPSEEK_API_KEY  - API ключ для DeepSeek
        """
    )
    
    parser.add_argument(
        '--branch', '-b',
        help='Название ветки (по умолчанию текущая ветка)',
        default=None
    )
    
    parser.add_argument(
        '--base-branch',
        help='Базовая ветка для сравнения (определяется автоматически)',
        default=None
    )
    
    parser.add_argument(
        '--provider', '-p',
        choices=['gigachat', 'deepseek'],
        required=True,
        help='Провайдер языковой модели'
    )
    
    parser.add_argument(
        '--api-key', '-k',
        help='API ключ (можно использовать переменные окружения)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Файл для сохранения описания'
    )
    
    parser.add_argument(
        '--language', '-l',
        choices=['ru', 'en'],
        default='ru',
        help='Язык описания (по умолчанию русский)'
    )
    
    parser.add_argument(
        '--prompt-type', '-t',
        choices=['basic', 'detailed', 'concise'],
        default='detailed',
        help='Тип промпта: basic (простой), detailed (подробный), concise (краткий)'
    )
    
    parser.add_argument(
        '--no-technical',
        action='store_true',
        help='Исключить технические детали'
    )
    
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.7,
        help='Температура модели (0.0 - 1.0)'
    )
    
    parser.add_argument(
        '--max-tokens',
        type=int,
        default=1000,
        help='Максимальное количество токенов в ответе'
    )
    
    parser.add_argument(
        '--repo-path', '-r',
        required=True,
        help='Путь к Git репозиторию'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Режим тестирования без реальных API запросов'
    )
    
    args = parser.parse_args()
    
    try:
        # Получаем API ключ
        api_key = args.api_key
        if not api_key:
            env_key = f"{args.provider.upper()}_API_KEY"
            api_key = os.getenv(env_key)
            if not api_key:
                print(f"❌ Ошибка: API ключ не найден. "
                      f"Укажите --api-key или установите переменную окружения {env_key}")
                sys.exit(1)
        
        # Создаем генератор
        generator = MRDescriptionGenerator(args.repo_path)
        
        # Определяем ветку
        branch = args.branch
        if not branch:
            branch = generator.git_helper.get_current_branch()
            print(f"🌿 Используем текущую ветку: {branch}")
        
        # Подготавливаем параметры
        kwargs = {
            'language': args.language,
            'prompt_type': args.prompt_type,
            'include_technical': not args.no_technical,
            'temperature': args.temperature,
            'max_tokens': args.max_tokens
        }
        
        # Проверяем dry-run режим
        if args.dry_run:
            print("🧪 Режим тестирования (dry-run)")
            print("=" * 50)
            
            # Показываем информацию о том, что будет отправлено
            base_branch = args.base_branch or generator.git_helper.get_base_branch(branch)
            diff_content = generator.git_helper.get_diff(branch, base_branch)
            
            print(f"📊 Ветка: {branch}")
            print(f"📊 Базовая ветка: {base_branch}")
            print(f"📊 Провайдер: {args.provider}")
            print(f"📊 Язык: {args.language}")
            print(f"📊 Тип промпта: {args.prompt_type}")
            print(f"📊 Размер diff: {len(diff_content)} символов")
            print(f"📊 Параметры: {kwargs}")
            
            if diff_content.strip():
                print("\n📋 Первые 500 символов diff:")
                print("-" * 50)
                print(diff_content[:500])
                if len(diff_content) > 500:
                    print("...")
                print("-" * 50)
                
                # Симулируем ответ
                mock_description = f"""## Сводка
Тестовое описание MR для ветки {branch}

## Изменения  
- Обнаружены изменения в {len(diff_content)} символов
- Базовая ветка: {base_branch}
- Провайдер: {args.provider}

## Технические заметки
Это тестовое описание сгенерировано в dry-run режиме.
Для получения реального описания запустите без флага --dry-run.

*Параметры генерации: {kwargs}*"""
                
                generator.save_description(mock_description, args.output)
                print("\n✅ Dry-run завершен успешно!")
            else:
                print("⚠️  Изменения между ветками не найдены")
            
            return
        
        # Генерируем описание
        description = generator.generate_description(
            branch=branch,
            provider_name=args.provider,
            api_key=api_key,
            base_branch=args.base_branch,
            **kwargs
        )
        
        # Сохраняем результат
        generator.save_description(description, args.output)
        
        print("✅ Готово!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
