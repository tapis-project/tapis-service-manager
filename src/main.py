import json
from typing import Annotated
from configs.services import Commands, Services

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()


@app.get("/")
def index():
    return {"Service Manager API": "Navigate to /docs or /redoc for API spec"}


@app.get("/service/{service_name}")
def get_service(service_name: str):
    return {"Service": Services[service_name]}


@app.get("/service/{service_name}/components")
def get_service_components(service_name: str):
    return {"Components": Services[service_name]}


@app.get("/service/{service_name}/commands")
def get_service_commands(service_name: str):
    commands = [
        component["commands"] for component in Services[service_name]["components"] 
        if component.get("commands", None) != None
    ]
    return {f"Commands for {service_name}": commands}


@app.get("/commands")
def get_commands():
    return {"Commands": Commands}


@app.get("/commands/{command}")
def get_command(command: str):
    commands = {cmd["name"]: cmd for cmd in Commands}
    return {"Command": commands[command]}

