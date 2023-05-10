import base64, time

import paramiko

from model.ServiceModel import ServiceModel
from model.CommandModel import CommandModel
from model.repositories import SecretRepository
from errors import ServerError

# TODO replace all BaseResponse returns with Exceptions particular to the failure
# that occurs and catch them in the calling class(controllers in this case)
class SSHExecService:
    def __init__(self, secret_repository: SecretRepository):
        self._secret_repo = secret_repository
        
    def ssh_exec(
        self,
        service: ServiceModel,
        command: CommandModel
    ):

        # TODO get kubernetes secret from API
        private_key = self._secret_repo.get_sercret(service.secret_key_ref)
        if private_key == None:
            raise ServerError(f"Missing private key for Linux user {service.user}")
        
        for _ in range(30):
            try:
                ssh = paramiko.client.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                private_key_string = base64.b64decode(str(CREDENTIALS_SECRET_REF)).decode("utf-8")
                private_key = paramiko.RSAKey.from_private_key(io.StringIO(private_key_string))
                ssh.connect(hostname=service.host, username=service.user, pkey=private_key, timeout=60)
                break
            except paramiko.SSHException as e:
                print(e)
                time.sleep(1)
            except Exception as e:
                return vars(BaseResponse(500, message=f"Server Error: {e}"))
        try:
            for script in command.scripts:
                script = "./" + script
                print(f"cd {service.base_path} && {script}")
                _, stdout, stderr = ssh.exec_command(f"cd {service.base_path} && {script}", timeout=10)
        except paramiko.SSHException as e:
            return vars(BaseResponse(500, message=f"Server Error: ssh exception - {e.message}"))

        # if len(stderr) > 0:
        #     return vars(BaseResponse(500, message=f"Server Error: error running command - {stderr}"))
        
        result = str(stdout.read().decode('utf-8'))

        ssh.close()

        return result