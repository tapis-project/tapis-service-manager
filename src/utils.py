import re

from fastapi import Request


def dispatch_middelwares(request: Request, middlewares: list):
    for middleware in middlewares:
        request = middleware(request)

    return request

def generate_route_summary(route_name: str):
    split_name = re.findall(r'[a-zA-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', route_name)
    split_name[0] = split_name[0].capitalize()
    name = ' '.join(split_name)

    return name