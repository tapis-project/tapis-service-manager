from typing import Union, List

from fastapi.responses import JSONResponse

from utils import CallableStaticClass


class BaseResponse(CallableStaticClass):
    @staticmethod
    def __call__(
        _,
        status: int, /,
        message: str = None,
        result: Union[dict, List[dict], str] = None,
        metadata: dict = {}
    ):
        # Conform to the tapis response object schema
        status = status if status else 200
        success = True if status in range(200, 300) else False
        message = str(message) if message != None else ("Success" if status in range(200, 300) else "Failure")
        result = result
        metadata = metadata
        version = "0.1.0"

        return JSONResponse(content={
            "status": status,
            "success": success,
            "message": message,
            "result": result,
            "metadata": metadata,
            "version": version
        })