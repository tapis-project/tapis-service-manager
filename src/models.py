from typing import List, Optional
from pydantic import BaseModel

class Command(BaseModel):
    name: str
    scripts: list[str]
    allow: list[str] = None

class Component(BaseModel):
    service: str
    name: str
    path: str = None
    basePath: str = None

class Service(BaseModel):
    name: str 
    basePath: str
    components: list[Component]
    useDefaultCommands: bool = True
    useNameAsPath: bool = True
    allow: list[str] = None
