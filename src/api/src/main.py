from fastapi import FastAPI, Request
from fastapi.routing import APIRoute

from helpers import container
from configs.constants import DEFAULT_COMMANDS
from views.http.responses import BaseResponse
from middleware import TapisServiceAuth
from utils import (
    dispatch_middelwares,
    generate_route_summary,
    service_can_run_command
)
from errors import ServerError


app = FastAPI()

@app.get("/services")
def listServices(request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    service_repo = container.load("service_repository")
    services = service_repo.list_services()
    
    return BaseResponse(200, result=[service.dict() for service in services])

@app.get("/services/{service_name}")
def getService(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    service_repo = container.load("service_repository")
    service = service_repo.get_service(service_name)

    if service == None:
        return BaseResponse(404, message=f"NotFound: Service '{service_name}' not found")
    
    return BaseResponse(200, result=service.dict())

@app.get("/services/{service_name}/components")
def listServiceComponents(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    service_repo = container.load("service_repository")
    components = service_repo.list_components(service_name)
    
    return BaseResponse(200, result=[component.dict() for component in components])

@app.get("/services/{service_name}/components/{component_name}")
def getServiceComponents(service_name: str, component_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    service_repo = container.load("service_repository")
    component = service_repo.get_component(service_name, component_name)

    if component == None:
        return BaseResponse(404, message=f"NotFound: Component '{component_name}' not found for service '{service_name}'")
    
    return BaseResponse(200, result=component.dict())

@app.get("/services/{service_name}/commands")
def listServiceCommands(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    service_repo = container.load("service_repository")
    commands = service_repo.list_commands(service_name)

    return BaseResponse(200, result=[command.dict() for command in commands])

@app.get("/services/{service_name}/components/{component_name}/commands")
def listComponentCommands(service_name: str, component_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    service_repo = container.load("service_repository")
    commands = service_repo.list_component_commands(service_name, component_name)

    return BaseResponse(200, result=[command.dict() for command in commands])

@app.get("/commands")
def listCommands(request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    return BaseResponse(200, result=DEFAULT_COMMANDS)

@app.post("/services/{service_name}/commands/{component_name}")
def runCommand(service_name: str, command_name: str, request: Request):
    request = dispatch_middelwares(request,[
        TapisServiceAuth(),
    ])

    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    service_repo = container.load("service_repository")
    service = service_repo.get_service(service_name)

    if not service_can_run_command(request.username, service):
        return BaseResponse(403, message=f"Forbidden: User '{request.username}' cannot run command '{command_name}' for service '{service_name}'.")

    command = service_repo.get_command(service, command_name)

    if command == None:
        return BaseResponse(404, message="Command not found")

    ssh_exec_service = container.load("ssh_exec_service")
           
    try:
        result = ssh_exec_service.run_command(service, command)
    except ServerError as e:
        return BaseResponse(500, message=f"{e}")

    return BaseResponse(200, result=result)

@app.post("/services/{service_name}/components/{component_name}/commands/{command_name}")
def runComponentCommand(
    service_name: str,
    component_name: str,
    command_name: str,
    request: Request
):
    request = dispatch_middelwares(request,[
        TapisServiceAuth()
    ])

    if request.username == None:
        return BaseResponse(401, message="Not authenticated")

    service_repo = container.load("service_repository")
    component = service_repo.get_component(service_name, component_name)

    if not service_can_run_command(request.username, component):
        return BaseResponse(403, message=f"Forbidden: User '{request.username}' cannot run commands for component '{component.name}'' of service '{service_name}'.")
    
    service_repo = container.load("service_repository")
    component = service_repo.get_component(service_name, component_name)

    command = service_repo.get_component_command(
        service_name,
        component.name,
        command_name
    )

    if command == None:
        return BaseResponse(404, message="Command not found")

    ssh_exec_service = container.load("ssh_exec_service")
           
    try:
        result = ssh_exec_service.run_command(component, command)
    except Exception as e:
        return BaseResponse(500, message=f"ServerError: {e}")

    return BaseResponse(200, result=result)


def camel_case_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.summary = generate_route_summary(route.name)
            route.operation_id = route.name

camel_case_operation_ids(app)

