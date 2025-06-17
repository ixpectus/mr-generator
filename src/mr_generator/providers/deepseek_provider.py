"""
Провайдер для DeepSeek API
"""

import requests
from typing import Dict, Any
from ..core.base_provider import LLMProvider


class DeepSeekProvider(LLMProvider):
    """Провайдер для работы с DeepSeek API"""
    
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.base_url = kwargs.get('base_url', 'https://api.deepseek.com/v1')
        self.model = kwargs.get('model', 'deepseek-chat')
        self.temperature = kwargs.get('temperature', 0.7)
    
    def generate_description(self, diff_content: str, branch_name: str, **kwargs) -> str:
        """Генерирует описание MR с помощью DeepSeek"""
        
        prompt = self._build_prompt(diff_content, branch_name, **kwargs)
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant that generates clear and professional merge request descriptions based on git diffs.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': self.temperature,
            'max_tokens': kwargs.get('max_tokens', 1000),
            'stream': False
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            raise Exception(f"Ошибка генерации с DeepSeek: {e}")
    
    def _build_prompt(self, diff_content: str, branch_name: str, **kwargs) -> str:
        """Строит промпт для генерации описания"""
        
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
    
    def get_model_name(self) -> str:
        """Возвращает название модели"""
        return f"DeepSeek-{self.model}"
