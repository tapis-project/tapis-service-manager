import re, os

from fastapi import Request

from models.schema import Scope


def dispatch_middelwares(request: Request, middlewares: list):
    for middleware in middlewares:
        request = middleware(request)

    return request

def resolve_base_path(service: dict, component_name: str = None, scope: Scope = Scope.Service) -> str:
    target = service
    path = target['basePath']
    if scope == Scope.Component:
        return path

    # Get the component service
    target = next(filter(lambda component: component["name"] == component_name))

    # Return parent service basePath + target name if no basePath defined
    if target["basePath"] == None:
        return path + target["name"]

    # Return target basePath
    return target["basePath"]

def generate_route_summary(route_name: str):
    split_name = re.findall(r'[a-zA-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', route_name)
    split_name[0] = split_name[0].capitalize()
    name = ' '.join(split_name)

    return name

def service_can_run_command(self, username, service, command_name):
    if username == service.name: return True

    # TODO Check that username is in service allow list

    return False
