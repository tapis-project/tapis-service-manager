def dispatch_middelwares(middlewares: list):
    for middleware in middlewares:
        request = middleware(request)

    return request