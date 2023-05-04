from fastapi import FastAPI, Request

from configs import services, commands
from views.http.responses import BaseResponse
from middleware import TapisServiceAuth, ServiceCanRunCommand
from utils import dispatch_middelwares 


app = FastAPI()

@app.get("/")
def index():
    return vars(BaseResponse(200, result="Welcome to the Service Manager API. Navigate to /docs or /redoc for API spec"))

@app.get("/services")
def get_services(request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))
    
    return vars(BaseResponse(200, result=services))

@app.get("/services/{service_name}")
def get_service(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))
    
    return vars(BaseResponse(200, result=services[service_name]))

@app.get("/services/{service_name}/components")
def get_service_components(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))
    
    return {"Components": services[service_name]}

@app.get("/services/{service_name}/commands")
def get_service_commands(service_name: str, request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    cmds = [
        component["commands"] for component in services[service_name]["components"] 
        if component.get("commands", None) != None
    ]
    return vars(BaseResponse(200, result=cmds))

@app.get("/commands")
def get_commands(request: Request):
    request = TapisServiceAuth()(request)
    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    return vars(BaseResponse(200, result=commands))

@app.post("services/{service}/commands/{command}")
def get_command(service: str, command: str, request: Request):
    request = dispatch_middelwares([
        TapisServiceAuth(request),
        ServiceCanRunCommand(request, service, command)
    ])

    if request.username == None:
        return vars(BaseResponse(401, message="Not authenticated"))

    if not request.service_can_run_command:
        return vars(BaseResponse(403, message=f"Forbidden: User '{request.username}' cannot run command '{command}' for service '{service}'."))

    cmd = next(filter(lambda cmd: cmd['name'] == command, commands), None)

    if cmd == None:
        return vars(BaseResponse(400, message="Bad Request"))
           
    return vars(BaseResponse(200, result=cmd))

# @app.get("/commands/{command}")
# def get_command(command: str, request: Request):
#     request = TapisServiceAuth()(request)
#     if request.username == None:
#         return vars(BaseResponse(401, message="Not authenticated"))

#     cmd = next(filter(lambda cmd: cmd['name'] == command, commands), None)

#     if cmd == None:
#         return vars(BaseResponse(
#             404,
#             message="Command not found",
#             result=None
#         ))
           
#     return vars(BaseResponse(200, result=cmd))

