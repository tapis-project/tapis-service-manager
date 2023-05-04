from fastapi import Request


def dispatch_middelwares(request: Request, middlewares: list):
    for middleware in middlewares:
        request = middleware(request)

    return request