"""
TODO
"""

import json
from pathlib import Path
from typing import Type

from cppython_core.schema import ModelT
from pydantic import BaseModel


def read_model_json(path: Path, model: Type[ModelT]) -> ModelT:
    """
    Reading routine
    """

    return model.parse_file(path=path)


def write_model_json(path: Path, model: BaseModel) -> None:
    """
    Writing routine
    """

    serialized = json.loads(model.json(exclude_none=True))
    with open(path, "w", encoding="utf8") as json_file:
        json.dump(serialized, json_file, ensure_ascii=False, indent=2)
