from typing import List

from pydantic import BaseModel


class CommandModel(BaseModel):
    name: str
    scripts: List[str]