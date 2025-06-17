"""
Тесты для основного CLI интерфейса
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mr_generator.cli import main
from mr_generator.core.git_helper import GitHelper


class TestCLI:
    """Тесты для CLI интерфейса"""

    def test_import_cli(self):
        """Тест импорта CLI модуля"""
        from mr_generator.cli import main

        assert callable(main)

    @patch("sys.argv", ["mr-gen", "--help"])
    def test_help_option(self):
        """Тест опции --help"""
        with pytest.raises(SystemExit) as exc_info:
            main()
        # argparse вызывает SystemExit(0) для --help
        assert exc_info.value.code == 0

    def test_git_helper_import(self):
        """Тест импорта GitHelper"""
        git_helper = GitHelper("/tmp")
        assert git_helper.repo_path == "/tmp"


class TestProviders:
    """Тесты для провайдеров"""

    def test_provider_imports(self):
        """Тест импорта провайдеров"""
        from mr_generator.providers.gigachat_provider import GigaChatProvider
        from mr_generator.providers.deepseek_provider import DeepSeekProvider

        assert GigaChatProvider is not None
        assert DeepSeekProvider is not None

    def test_base_provider_import(self):
        """Тест импорта базового провайдера"""
        from mr_generator.core.base_provider import LLMProvider

        assert LLMProvider is not None


class TestConfig:
    """Тесты для конфигурации"""

    def test_config_import(self):
        """Тест импорта конфигурации"""
        from mr_generator.config import Config

        assert Config is not None

    def test_config_methods(self):
        """Тест методов конфигурации"""
        from mr_generator.config import Config

        # Тест получения конфигурации провайдера
        config = Config.get_provider_config("deepseek")
        assert isinstance(config, dict)

        # Тест получения шаблона промпта
        template = Config.get_prompt_template("basic_ru")
        assert isinstance(template, str)
        assert "branch_name" in template

        # Тест получения максимального размера diff
        max_size = Config.get_max_diff_size()
        assert isinstance(max_size, int)
        assert max_size > 0
