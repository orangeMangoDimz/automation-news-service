from pathlib import Path
from dotenv import load_dotenv
from pydantic import ValidationError
from utils.constant import API_KEY_NOT_FOUND
from typing import List
from utils.type_hint import EnvType
import os


class LoadSettings:
    @staticmethod
    def get_env() -> List[EnvType]:
        dotenv_path = Path(".env")
        load_dotenv(dotenv_path=dotenv_path)

        list_env: List[EnvType] = [
            {
                "key": "GEMINI_API_KEY",
                "value": "",
                "err_msg": API_KEY_NOT_FOUND,
            },
        ]

        for env in list_env:
            value: str | None = os.getenv(env.get("key"))
            if value is None:
                raise ValidationError(env.get("err_msg"))
            env["value"] = value

        return list_env
