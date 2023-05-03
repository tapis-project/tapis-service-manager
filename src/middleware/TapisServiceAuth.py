from fastapi import Request

from tapipy.tapis import Tapis

class TapisServiceAuth:
    def __call__(self, request: Request):
        # do something with the request object
        content_type = request.headers.get('Content-Type')
        print(content_type)

        request.username = "workflows"
        #return {"validated": True, "username": "workflows"}
        
        return request
