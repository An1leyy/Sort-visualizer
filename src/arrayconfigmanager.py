"""
json - работа с json файлами.
os - управление системными командами.
"""

import json
import os

class ArrayConfigManager:
    """Управляет настройками генерации массива из JSON файла."""

    def __init__(self, config_path="array_config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """Загружает конфигурацию из JSON файла."""

        if not os.path.exists(self.config_path):
            return None

        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
            return config
        except FileNotFoundError as e:
            print(f"Error loading config: {e}. Using constants from constants.py")
            return None

    def get_generation_params(self):
        """
        Возвращает параметры генерации массива.
        Если нет JSON файла возвращает None.
        """

        if self.config is None:
            return None

        return {
            "min_length": self.config.get("min_length", 10),
            "max_length": self.config.get("max_length", 35),
            "min_element": self.config.get("min_element", -250),
            "max_element": self.config.get("max_element", 250)
        }

    def validate_params(self, params):
        """Проверяет корректность параметров."""

        if not params:
            return False

        if params["min_length"] < 1:
            params["min_length"] = 1
        if params["max_length"] > 50:
            params["max_length"] = 50
        if params["min_length"] > params["max_length"]:
            params["min_length"], params["max_length"] = params["max_length"], params["min_length"]

        if params["min_element"] > params["max_element"]:
            params["min_element"], params["max_element"] =\
                params["max_element"], params["min_element"]

        return True
