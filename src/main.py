import io, re, time

import paramiko

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute

from models import Scope
from configs import services, commands
from configs.constants import USER, HOST, CREDENTIALS_SECRET_REF
from views.http.responses import BaseResponse
from middleware import TapisServiceAuth, ServiceCanRunCommand
from utils import dispatch_middelwares, generate_route_summary, resolve_base_path


app = FastAPI()

@app.get("/services")
def listServices(request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))
    
    return vars(BaseResponse(200, result=services))

@app.get("/services/{service_name}")
def getService(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))
    
    return vars(BaseResponse(200, result=services[service_name]))

@app.get("/services/{service_name}/components")
def listServiceComponents(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))
    
    return {"Components": services[service_name]}

@app.get("/services/{service_name}/commands")
def listServiceCommands(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    cmds = [
        component["commands"] for component in services[service_name]["components"] 
        if component.get("commands", None) != None
    ]
    return vars(BaseResponse(200, result=cmds))

@app.get("/commands")
def listCommands(request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    return vars(BaseResponse(200, result=commands))

#######
# NOT TESTED YET #
#######
@app.post("/services/{service}/commands/{command}")
def runCommand(service: str, command: str, request: Request):
    request = dispatch_middelwares(request,[
        TapisServiceAuth(),
        ServiceCanRunCommand(service, command)
    ])

    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    if not request.service_can_run_command:
        return vars(BaseResponse(403, message=f"Forbidden: User '{request.username}' cannot run command '{command}' for service '{service}'."))

    cmd = next(filter(lambda cmd: cmd['name'] == command, commands), None)

    if cmd == None:
        return vars(BaseResponse(400, message="Bad Request"))
           
    # TODO get kubernetes secret from API
    private_key = ""
    if private_key == None:
        return vars(BaseResponse(500, message=f"Server Error: Missing private key for Linux user {USER}"))
    
    path = resolve_base_path(services[service], scope=Scope.Service)

    for i in range(30):
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
            _stdin, stdout, stderr = ssh.exec_command(f"cd {path} && {script}", timeout=10)
    except paramiko.SSHException as e:
        return vars(BaseResponse(500, message=f"Server Error: ssh exception - {e.message}"))

    if len(stderr) > 0:
        return vars(BaseResponse(500, message=f"Server Error: error running command - {stderr}"))
    
    result = str(stdout.read().decode('utf-8'))

    ssh.close()
    return vars(BaseResponse(200, result=result))

@app.post("/services/{service}/components/{component}/commands/{command}")
def runComponentCommand(service: str, component: str, command: str, request: Request):
    request = dispatch_middelwares(request,[
        TapisServiceAuth(),
        ServiceCanRunCommand(service, command)
    ])

    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    if not request.service_can_run_command:
        return vars(BaseResponse(403, message=f"Forbidden: User '{request.username}' cannot run command '{command}' for service '{service}'."))

    cmd = next(filter(lambda cmd: cmd['name'] == command, commands), None)

    if cmd == None:
        return vars(BaseResponse(400, message="Bad Request"))
           
    # TODO get kubernetes secret from API
    private_key = ""
    if private_key == None:
        return vars(BaseResponse(500, message=f"Server Error: Missing private key for Linux user {USER}"))
    
    path = resolve_base_path(services[service], component=component, scope=Scope.Component)

    for i in range(30):
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
            _stdin, stdout, stderr = ssh.exec_command(f"cd {path} && {script}", timeout=10)
    except paramiko.SSHException as e:
        return vars(BaseResponse(500, message=f"Server Error: ssh exception - {e.message}"))

    if len(stderr) > 0:
        return vars(BaseResponse(500, message=f"Server Error: error running command - {stderr}"))
    
    result = str(stdout.read().decode('utf-8'))

    ssh.close()
    return vars(BaseResponse(200, result=result))


def camel_case_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.summary = generate_route_summary(route.name)
            route.operation_id = route.name

camel_case_operation_ids(app)

