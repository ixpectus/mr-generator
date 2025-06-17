"""
Абстрактный базовый класс для языковых моделей
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LLMProvider(ABC):
    """Абстрактный класс для провайдеров языковых моделей"""

    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        self.config = kwargs

    @abstractmethod
    def generate_description(
        self, diff_content: str, branch_name: str, **kwargs
    ) -> str:
        """
        Генерирует описание MR на основе diff содержимого

        Args:
            diff_content: Содержимое git diff
            branch_name: Название ветки
            **kwargs: Дополнительные параметры

        Returns:
            Сгенерированное описание MR
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Возвращает название модели"""
        pass

    def validate_api_key(self) -> bool:
        """Проверяет валидность API ключа"""
        return bool(self.api_key)
