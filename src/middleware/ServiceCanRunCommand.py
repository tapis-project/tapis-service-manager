from fastapi import Request

class ServiceCanRunCommand:
    def __init__(self, service, command):
        self.service = service
        self.command = command
        
    def __call__(self, request: Request,):
        # TODO determine permissions for command
        request.service_can_run_command = True
        
        return request