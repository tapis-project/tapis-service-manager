import io, re, time
from pprint import pprint

import paramiko

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute

from models.schema import Scope
from models import ServiceRepository as ServiceRepo
from configs.constants import USER, HOST, CREDENTIALS_SECRET_REF, DEFAULT_COMMANDS
from views.http.responses import BaseResponse
from middleware import TapisServiceAuth
from utils import (
    dispatch_middelwares,
    generate_route_summary,
    resolve_base_path,
    service_can_run_command
)



app = FastAPI()

@app.get("/services")
def listServices(request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    services = ServiceRepo.list_services()
    
    return vars(BaseResponse(200, result=[service.dict() for service in services]))

@app.get("/services/{service_name}")
def getService(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    service = ServiceRepo.get_service(service_name)
    
    return vars(BaseResponse(200, result=service.dict()))

@app.get("/services/{service_name}/components")
def listServiceComponents(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    components = ServiceRepo.list_components(service_name)
    
    return vars(BaseResponse(200, result=[component.dict() for component in components]))

@app.get("/services/{service_name}/commands")
def listServiceCommands(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    commands = ServiceRepo.list_commands(service_name)

    return vars(BaseResponse(200, result=[command.dict() for command in commands]))

@app.get("/services/{service_name}/components/{component_name}/commands")
def listComponentCommands(service_name: str, component_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    commands = ServiceRepo.list_component_commands(service_name, component_name)

    return vars(BaseResponse(200, result=[command.dict() for command in commands]))

@app.get("/commands")
def listCommands(request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    return vars(BaseResponse(200, result=DEFAULT_COMMANDS))

#######
# NOT TESTED YET #
#######
@app.post("/services/{service_name}/commands/{component_name}")
def runCommand(service_name: str, command_name: str, request: Request):
    request = dispatch_middelwares(request,[
        TapisServiceAuth(),
    ])

    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    # if not request.service_can_run_command:
    #     return vars(BaseResponse(403, message=f"Forbidden: User '{request.username}' cannot run command '{command_name}' for service '{service_name}'."))

    cmd = next(filter(lambda cmd: cmd['name'] == command_name, DEFAULT_COMMANDS), None)

    if cmd == None:
        return vars(BaseResponse(400, message="Bad Request"))
           
    # TODO get kubernetes secret from API
    private_key = ""
    if private_key == None:
        return vars(BaseResponse(500, message=f"Server Error: Missing private key for Linux user {USER}"))
    
    path = resolve_base_path(services[service], scope=Scope.Service)

    for _ in range(30):
        try:
            ssh = paramiko.client.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key(io.StringIO(CREDENTIALS_SECRET_REF))
            ssh.connect(hostname=HOST, username=USER, pkey=private_key, timeout=60)
            break
        except paramiko.SSHException as e:
            time.sleep(1)
        except Exception as e:
            return vars(BaseResponse(500, message=f"Server Error: {e.message}"))
    try:
        for script in cmd["scripts"]:
            script = "./" + script
            _, stdout, stderr = ssh.exec_command(f"cd {path} && {script}", timeout=10)
    except paramiko.SSHException as e:
        return vars(BaseResponse(500, message=f"Server Error: ssh exception - {e.message}"))

    if len(stderr) > 0:
        return vars(BaseResponse(500, message=f"Server Error: error running command - {stderr}"))
    
    result = str(stdout.read().decode('utf-8'))

    ssh.close()
    return vars(BaseResponse(200, result=result))

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
        return vars(BaseResponse(401, message="Not authenticated"))

    # if not service_can_run_command(service_name, command_name):
    #     return vars(BaseResponse(403, message=f"Forbidden: User '{request.username}' cannot run command '{component_name}' for service '{service_name}'."))
    
    component = ServiceRepo.get_component(service_name, component_name)

    command = ServiceRepo.get_component_command(
        service_name,
        component.name,
        command_name
    )

    if command == None:
        return vars(BaseResponse(404, message="Command not found"))
           
    # TODO get kubernetes secret from API
    private_key = ""
    if private_key == None:
        return vars(BaseResponse(500, message=f"Server Error: Missing private key for Linux user {USER}"))

    # for _ in range(30):
    #     try:
    #         ssh = paramiko.client.SSHClient()
    #         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #         private_key = paramiko.RSAKey.from_private_key(io.StringIO(CREDENTIALS_SECRET_REF))
    #         ssh.connect(hostname=HOST, username=USER, pkey=private_key, timeout=60)
    #         break
    #     except paramiko.SSHException as e:
    #         time.sleep(1)
    #     except Exception as e:
    #         return vars(BaseResponse(500, message=f"Server Error: {e.message}"))
    try:
        for script in command.scripts:
            script = "./" + script
            print(f"cd {component.base_path} && {script}")
            # _, stdout, stderr = ssh.exec_command(f"cd {component.base_path} && {script}", timeout=10)
    except paramiko.SSHException as e:
        return vars(BaseResponse(500, message=f"Server Error: ssh exception - {e.message}"))

    # if len(stderr) > 0:
    #     return vars(BaseResponse(500, message=f"Server Error: error running command - {stderr}"))
    
    # result = str(stdout.read().decode('utf-8'))

    # ssh.close()
    return vars(BaseResponse(200, result={}))


def camel_case_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.summary = generate_route_summary(route.name)
            route.operation_id = route.name

camel_case_operation_ids(app)

