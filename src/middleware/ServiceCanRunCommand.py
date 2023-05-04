from fastapi import Request

class ServiceCanRunCommand:
    def __init__(self, request: Request, service, command):
        self.request = request
        self.service = service
        self.command = command
        
    def __call__(self, request: Request):
        # TODO determine permissions for command
        request.service_can_run_command = True