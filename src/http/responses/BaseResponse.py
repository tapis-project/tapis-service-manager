from pydantic import BaseModel
from typing import Union, List


class BaseResponse(BaseModel):
    def __init__(self,
        status: int,
        message: str,
        result: Union[dict, List[dict], str] = None,
        metadata: dict = {}
    ):
        # Conform to the tapis response object schema
        self.status = status if status else 200
        self.success = True if status in range(200, 300) else False
        self.message = str(message) if message else ("Success" if status in range(200, 300) else "Failure")
        self.result = result
        self.metadata = metadata
        self.version = "0.1.0"

    def __iter__(self): return self