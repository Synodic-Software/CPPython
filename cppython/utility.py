"""Utility specific to managing projects
"""

import json
from pathlib import Path
from typing import Any

from cppython_core.schema import ModelT
from pydantic import BaseModel


def read_model_json(path: Path, model: type[ModelT]) -> ModelT:
    """Reading routine. Only keeps Model data

    Args:
        path: _description_
        model: _description_

    Returns:
        _description_
    """

    return model.parse_file(path=path)


def read_json(path: Path) -> Any:
    """Reading routine

    Args:
        path: _description_

    Returns:
        _description_
    """

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_model_json(path: Path, model: BaseModel) -> None:
    """Writing routine. Only writes model data

    Args:
        path: _description_
        model: _description_
    """

    serialized = json.loads(model.json(exclude_none=True))
    with open(path, "w", encoding="utf8") as file:
        json.dump(serialized, file, ensure_ascii=False, indent=4)


def write_json(path: Path, data: Any) -> None:
    """Writing routine

    Args:
        path: _description_
        data: _description_
    """

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
