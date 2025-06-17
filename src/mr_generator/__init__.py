"""
MR Description Generator

Умный генератор описаний merge request с использованием ИИ моделей.
"""

from .core.git_helper import GitHelper
from .core.base_provider import LLMProvider
from .providers.gigachat_provider import GigaChatProvider
from .providers.deepseek_provider import DeepSeekProvider
from .config import Config

__version__ = "1.0.0"

__all__ = [
    "GitHelper",
    "LLMProvider",
    "GigaChatProvider",
    "DeepSeekProvider",
    "Config",
]
