from fastapi import Request

from tapipy.tapis import Tapis

class TapisServiceAuth:
    def __init__(self, request: Request):
        self.request = request

    def __call__(self):
        # do something with the request object
        content_type = self.request.headers.get('Content-Type')
        print(content_type)

        self.request.username = "workflows"
        #return {"validated": True, "username": "workflows"}
        
        return self.request
