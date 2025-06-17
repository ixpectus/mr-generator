"""
Провайдер для GigaChat API
"""

import json
import requests
import uuid
from typing import Dict, Any
from ..core.base_provider import LLMProvider


class GigaChatProvider(LLMProvider):
    """Провайдер для работы с GigaChat API"""
    
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.base_url = kwargs.get('base_url', 'https://gigachat.devices.sberbank.ru/api/v1')
        self.model = kwargs.get('model', 'GigaChat')
        self.temperature = kwargs.get('temperature', 0.7)
        self.access_token = None
    
    def _get_access_token(self) -> str:
        """Получает access token для GigaChat"""
        if self.access_token:
            return self.access_token
            
        # Новый URL согласно документации
        auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),  # Уникальный идентификатор запроса
            'Authorization': f'Basic {self.api_key}'
        }
        
        data = {'scope': 'GIGACHAT_API_PERS'}
        
        try:
            response = requests.post(auth_url, headers=headers, data=data, verify=False, timeout=30)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
            return self.access_token
        except Exception as e:
            raise Exception(f"Ошибка получения токена GigaChat: {e}")
    
    def generate_description(self, diff_content: str, branch_name: str, **kwargs) -> str:
        """Генерирует описание MR с помощью GigaChat"""
        
        prompt = self._build_prompt(diff_content, branch_name, **kwargs)
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self._get_access_token()}'
        }
        
        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': self.temperature,
            'max_tokens': kwargs.get('max_tokens', 1000)
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, verify=False)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            raise Exception(f"Ошибка генерации с GigaChat: {e}")
    
    def _build_prompt(self, diff_content: str, branch_name: str, **kwargs) -> str:
        """Строит улучшенный промпт для генерации описания"""
        
        changed_files = kwargs.get('changed_files', [])
        commit_messages = kwargs.get('commit_messages', [])
        
        # Определяем тип MR
        mr_type = self._detect_mr_type(changed_files, commit_messages)
        
        print(f"🎯 Определен тип MR: {mr_type}")
        
        # Возвращаем специализированный промпт
        return self._get_specialized_prompt(mr_type, diff_content, branch_name, **kwargs)
        
    def _detect_mr_type(self, changed_files: list, commit_messages: list) -> str:
        """Определяет тип MR для выбора подходящего промпта"""
        
        # Анализ по файлам
        has_ci = any(('.github' in f or 'ci' in f.lower() or 'docker' in f.lower() or 
                     'makefile' in f.lower() or '.yml' in f or '.yaml' in f) for f in changed_files)
        has_tests = any(('test' in f.lower() or 'spec' in f.lower()) for f in changed_files)
        has_docs = any(('readme' in f.lower() or '.md' in f.lower()) for f in changed_files)
        has_config = any(('config' in f.lower() or '.json' in f or '.toml' in f or 
                         '.env' in f or 'requirements' in f) for f in changed_files)
        
        # Анализ по коммитам  
        commits_text = ' '.join(commit_messages).lower()
        is_fix = any(word in commits_text for word in ['fix', 'bug', 'исправ', 'bagfix', 'hotfix'])
        is_feat = any(word in commits_text for word in ['feat', 'add', 'new', 'добав', 'feature'])
        is_refactor = any(word in commits_text for word in ['refactor', 'clean', 'рефактор', 'restructure'])
        is_docs = any(word in commits_text for word in ['docs', 'documentation', 'readme', 'документ'])
        
        # Определяем тип с приоритетами
        if has_ci or 'docker' in commits_text or 'deploy' in commits_text:
            return 'infrastructure'
        elif is_fix and not is_feat:
            return 'bugfix'
        elif is_refactor and not is_feat:
            return 'refactor'
        elif has_docs and is_docs and len(changed_files) <= 5:
            return 'docs'
        elif is_feat or 'new' in commits_text:
            return 'feature'
        else:
            return 'default'
    
    def _get_specialized_prompt(self, mr_type: str, diff_content: str, branch_name: str, **kwargs) -> str:
        """Возвращает специализированный промпт в зависимости от типа MR"""
        
        language = kwargs.get('language', 'ru')
        prompt_type = kwargs.get('prompt_type', 'detailed')
        
        # Импортируем шаблоны из config
        from ..config import PROMPT_TEMPLATES
        
        # Определяем ключ шаблона
        template_key = f"{prompt_type}_{language}"
        
        if template_key not in PROMPT_TEMPLATES:
            # Fallback к базовому шаблону
            template_key = f"basic_{language}"
        
        template = PROMPT_TEMPLATES[template_key]
        
        # Подготавливаем данные для шаблона
        changed_files = kwargs.get('changed_files', [])
        commit_messages = kwargs.get('commit_messages', [])
        repo_name = kwargs.get('repo_name', 'Unknown')
        
        # Форматируем шаблон
        try:
            return template.format(
                branch_name=branch_name,
                diff_content=diff_content,
                repo_name=repo_name,
                changed_files_count=len(changed_files),
                commits_count=len(commit_messages)
            )
        except KeyError as e:
            # Если в шаблоне не хватает параметров, используем базовый формат
            return template.format(
                branch_name=branch_name,
                diff_content=diff_content
            )
    
    def _get_russian_prompt(self, mr_type: str, diff_content: str, branch_name: str, **kwargs) -> str:
        """Специализированные русские промпты"""
        
        include_technical = kwargs.get('include_technical', True)
        changed_files = kwargs.get('changed_files', [])
        commit_messages = kwargs.get('commit_messages', [])
        
        # Базовая информация
        context_info = []
        if changed_files:
            context_info.append(f"Файлов: {len(changed_files)}")
        if commit_messages:
            context_info.append(f"Коммитов: {len(commit_messages)}")
        
        context = " | ".join(context_info)
        
        if mr_type == 'feature':
            return f"""Проанализируй добавление новой функциональности в ветке '{branch_name}'.

Контекст: {context}

ТРЕБОВАНИЯ:
- Опиши КОНКРЕТНО какой функционал добавлен
- Перечисли новые API/методы/компоненты
- Укажи реальные названия файлов и классов
- БЕЗ общих фраз типа "расширена функциональность"

ФОРМАТ:
## Новая функциональность
[Конкретное описание что именно добавлено]

## Ключевые компоненты
[Новые классы/методы/файлы с кратким описанием]

{"## Технические детали" if include_technical else ""}
{"[API endpoints, схемы БД, зависимости]" if include_technical else ""}

## Тестирование
[Как протестировать новый функционал]

Git diff:
```
{diff_content}
```

Создай описание для новой фичи:"""

        elif mr_type == 'bugfix':
            return f"""Проанализируй исправление бага в ветке '{branch_name}'.

Контекст: {context}

ТРЕБОВАНИЯ:
- Опиши КОНКРЕТНО какой баг исправлен
- Укажи файлы/методы где была проблема
- Объясни как именно исправлено
- Укажи возможные side effects

ФОРМАТ:
## Исправленная проблема
[Конкретное описание бага]

## Изменения в коде
[Файлы и методы с описанием фиксов]

{"## Техническая причина" if include_technical else ""}
{"[Root cause и детали исправления]" if include_technical else ""}

## Проверка
[Как убедиться что баг исправлен]

Git diff:
```
{diff_content}
```

Создай описание багфикса:"""

        elif mr_type == 'refactor':
            return f"""Проанализируй рефакторинг кода в ветке '{branch_name}'.

Контекст: {context}

ТРЕБОВАНИЯ:
- Опиши КОНКРЕТНО что переработано
- Укажи улучшения архитектуры/производительности
- Перечисли breaking changes если есть
- Избегай общих фраз про "улучшение качества"

ФОРМАТ:
## Рефакторинг
[Конкретные изменения структуры/архитектуры]

## Улучшения
[Производительность, читаемость, maintainability]

{"## Breaking changes" if include_technical else ""}
{"[Что может сломаться, изменения API]" if include_technical else ""}

## Миграция
[Что нужно обновить при внедрении]

Git diff:
```
{diff_content}
```

Создай описание рефакторинга:"""

        elif mr_type == 'infrastructure':
            return f"""Проанализируй изменения инфраструктуры в ветке '{branch_name}'.

Контекст: {context}

ТРЕБОВАНИЯ:
- Опиши КОНКРЕТНЫЕ изменения в CI/CD/конфигах
- Укажи новые/измененные скрипты и файлы
- Объясни влияние на deployment
- Перечисли новые зависимости

ФОРМАТ:
## Инфраструктурные изменения
[Конкретные изменения конфигов/скриптов/Docker]

## CI/CD
[Изменения в пайплайнах/actions]

{"## Deployment" if include_technical else ""}
{"[Влияние на развертывание и окружения]" if include_technical else ""}

## Зависимости
[Новые/обновленные пакеты/сервисы]

Git diff:
```
{diff_content}
```

Создай описание инфраструктурных изменений:"""

        else:  # default
            return self._get_default_russian_prompt(diff_content, branch_name, **kwargs)
    
    def _get_default_russian_prompt(self, diff_content: str, branch_name: str, **kwargs) -> str:
        """Улучшенный базовый русский промпт"""
        
        include_technical = kwargs.get('include_technical', True)
        changed_files = kwargs.get('changed_files', [])
        commit_messages = kwargs.get('commit_messages', [])
        
        # Анализируем типы файлов
        file_types = set()
        for file in changed_files[:20]:
            if '.' in file:
                ext = file.split('.')[-1].lower()
                file_types.add(ext)
        
        context_info = []
        if changed_files:
            context_info.append(f"Файлов: {len(changed_files)}")
        if file_types:
            context_info.append(f"Типы: {', '.join(sorted(file_types))}")
        if commit_messages:
            context_info.append(f"Коммитов: {len(commit_messages)}")
        
        context = " | ".join(context_info)
        
        return f"""Проанализируй git diff из ветки '{branch_name}' и создай КОНКРЕТНОЕ описание merge request.

Контекст: {context}

ТРЕБОВАНИЯ:
- Используй конкретные технические термины, не общие фразы
- Перечисли реально измененные файлы/компоненты  
- Упомяни конкретный добавленный/измененный функционал
- БЕЗ "воды" типа "комплексный", "надежный", "улучшенный"
- Начинай сразу с того, что сделано, без "Данный MR добавляет..."

ФОРМАТ:
## Что изменено
[Конкретный список изменений]

## Ключевые файлы
[Важные файлы с кратким описанием изменений]

{"## Технические детали" if include_technical else ""}
{"[Детали реализации, breaking changes, зависимости]" if include_technical else ""}

## Тестирование
[Что нужно протестировать]

Git diff:
```
{diff_content}
```

Создай КОНКРЕТНОЕ описание:"""

    def _get_english_prompt(self, mr_type: str, diff_content: str, branch_name: str, **kwargs) -> str:
        """Английские промпты (базовая реализация)"""
        # Можно добавить английские варианты аналогично русским
        return self._get_default_russian_prompt(diff_content, branch_name, **kwargs)
    
    def get_model_name(self) -> str:
        """Возвращает название модели"""
        return f"GigaChat-{self.model}"
