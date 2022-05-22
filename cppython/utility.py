"""
TODO
"""

import json
from pathlib import Path
from typing import Any, Type

from cppython_core.schema import ModelT
from pydantic import BaseModel


def read_model_json(path: Path, model: Type[ModelT]) -> ModelT:
    """
    Reading routine. Only keeps Model data
    """

    return model.parse_file(path=path)


def read_json(path: Path) -> Any:
    """
    Reading routine
    """

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_model_json(path: Path, model: BaseModel) -> None:
    """
    Writing routine. Only writes model data
    """

    serialized = json.loads(model.json(exclude_none=True))
    with open(path, "w", encoding="utf8") as file:
        json.dump(serialized, file, ensure_ascii=False, indent=4)


def write_json(path: Path, data: Any) -> None:
    """
    Writing routine
    """

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
