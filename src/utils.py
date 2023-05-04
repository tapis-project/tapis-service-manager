import re, enum

from fastapi import Request

from models import Scope


def dispatch_middelwares(request: Request, middlewares: list):
    for middleware in middlewares:
        request = middleware(request)

    return request

def resolve_base_path(service: dict, component: str = None, scope: Scope = Scope.Service) -> str:
    target = service
    if scope == Scope.Component:
        for comp in service["components"]:
            target = comp if comp["name"] == component else ""
            break
    
    path = service['basePath'] + '/' + target['name'] if service['useNameAsPath'] else service['basePath'] + '/' + target['path']
    return path

def generate_route_summary(route_name: str):
    split_name = re.findall(r'[a-zA-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', route_name)
    split_name[0] = split_name[0].capitalize()
    name = ' '.join(split_name)

    return name