import json

from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from configs import services, commands
from views.http.responses import BaseResponse
from middleware import TapisServiceAuth


app = FastAPI()

@app.get("/")
def index(request):
    if TapisServiceAuth()(request):
        return {"Service Manager API": "Navigate to /docs or /redoc for API spec"}

    return BaseResponse(401, message="Not Authenticated")


@app.get("/service/{service_name}")
def get_service(service_name: str):
    return {"Service": services[service_name]}


@app.get("/service/{service_name}/components")
def get_service_components(service_name: str):
    return {"Components": services[service_name]}


@app.get("/service/{service_name}/commands")
def get_service_commands(service_name: str):
    cmds = [
        component["commands"] for component in services[service_name]["components"] 
        if component.get("commands", None) != None
    ]
    return vars(BaseResponse(200, result=cmds))


@app.get("/commands")
def get_commands():
    return vars(BaseResponse(200, result=commands))


@app.get("/commands/{command}")
def get_command(command: str):
    cmd = next(filter(lambda cmd: cmd['name'] == command, commands), None)

    if cmd == None:
        return vars(BaseResponse(
            404,
            message="Command not found",
            result=None
        ))
           
    return vars(BaseResponse(200, result=cmd))

