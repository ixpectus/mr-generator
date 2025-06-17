"""
Утилиты для работы с Git репозиториями
"""

import subprocess
import os
from typing import Optional, Tuple


class GitHelper:
    """Помощник для работы с Git командами"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def get_current_branch(self) -> str:
        """Получает название текущей ветки"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка получения текущей ветки: {e}")

    def get_base_branch(self, branch: str) -> str:
        """
        Определяет базовую ветку (обычно main/master) от которой была создана ветка
        """
        # Сначала попробуем найти общий commit с main
        for base in ["main", "master", "develop"]:
            try:
                result = subprocess.run(
                    ["git", "merge-base", branch, base],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                if result.returncode == 0:
                    return base
            except subprocess.CalledProcessError:
                continue

        # Если не найдено, используем master по умолчанию
        return "master"

    def get_diff(self, branch: str, base_branch: Optional[str] = None) -> str:
        """
        Получает diff между веткой и базовой веткой

        Args:
            branch: Название ветки для сравнения
            base_branch: Базовая ветка (если не указана, определяется автоматически)

        Returns:
            Содержимое git diff
        """
        if not base_branch:
            base_branch = self.get_base_branch(branch)

        try:
            # Получаем merge-base для точного сравнения
            merge_base_result = subprocess.run(
                ["git", "merge-base", base_branch, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            merge_base = merge_base_result.stdout.strip()

            # Получаем diff от merge-base до branch
            diff_result = subprocess.run(
                ["git", "diff", merge_base, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            return diff_result.stdout

        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка получения diff: {e}")

    def get_commit_messages(
        self, branch: str, base_branch: Optional[str] = None
    ) -> list:
        """
        Получает сообщения коммитов в ветке

        Args:
            branch: Название ветки
            base_branch: Базовая ветка

        Returns:
            Список сообщений коммитов
        """
        if not base_branch:
            base_branch = self.get_base_branch(branch)

        try:
            result = subprocess.run(
                ["git", "log", f"{base_branch}..{branch}", "--pretty=format:%s"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            return [line.strip() for line in result.stdout.split("\n") if line.strip()]

        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка получения коммитов: {e}")

    def get_changed_files(self, branch: str, base_branch: Optional[str] = None) -> list:
        """
        Получает список измененных файлов

        Args:
            branch: Название ветки
            base_branch: Базовая ветка

        Returns:
            Список измененных файлов
        """
        if not base_branch:
            base_branch = self.get_base_branch(branch)

        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{base_branch}...{branch}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

            return [line.strip() for line in result.stdout.split("\n") if line.strip()]

        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка получения измененных файлов: {e}")

    def is_git_repo(self) -> bool:
        """Проверяет, является ли директория Git репозиторием"""
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def get_repo_info(self) -> dict:
        """Получает общую информацию о репозитории"""
        if not self.is_git_repo():
            raise Exception("Директория не является Git репозиторием")

        info = {}

        try:
            # Название репозитория
            remote_result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            if remote_result.returncode == 0:
                remote_url = remote_result.stdout.strip()
                info["remote_url"] = remote_url

                # Извлекаем название репозитория из URL
                if remote_url.endswith(".git"):
                    remote_url = remote_url[:-4]
                repo_name = remote_url.split("/")[-1]
                info["repo_name"] = repo_name

            # Текущая ветка
            info["current_branch"] = self.get_current_branch()

            # Последний коммит
            last_commit_result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%H %s"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            if last_commit_result.returncode == 0:
                info["last_commit"] = last_commit_result.stdout.strip()

        except Exception as e:
            info["error"] = str(e)

        return info
