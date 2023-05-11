import base64, time

import paramiko

from model.ServiceModel import ServiceModel
from model.CommandModel import CommandModel
from model.repositories import SecretRepository
from errors import ServerError
from configs.constants import SSH_TIMEOUT

# TODO replace all BaseResponse returns with Exceptions particular to the failure
# that occurs and catch them in the calling class(controllers in this case)
class SSHExecService:
    def __init__(self, secret_repository: SecretRepository):
        self._secret_repo = secret_repository
        
    def run_command(
        self,
        service: ServiceModel,
        command: CommandModel
    ):
        try:
            private_key = self._secret_repo.get_secret(service.ssh_secret_ref)
        except Exception as e:
            raise ServerError(e)
        
        for _ in range(30):
            try:
                ssh = paramiko.client.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                ssh_key = paramiko.RSAKey.from_private_key(private_key)
                ssh.connect(hostname=service.host, username=service.user, pkey=ssh_key, timeout=60)
                break
            except paramiko.SSHException as e:
                time.sleep(1)
            except Exception as e:
                raise ServerError(e)
        try:
            for script in command.scripts:
                script = "./" + script
                _, stdout, stderr = ssh.exec_command(f"cd {service.base_path} && {script}", timeout=int(SSH_TIMEOUT))
        except paramiko.SSHException as e:
            ssh.close()
            raise ServerError(f"Error from ssh: {e.message}")

        error = str(stderr.read().decode('utf-8'))
        if len(error) > 0:
            raise ServerError(f"Error from ssh stderr: {error}")
        
        result = str(stdout.read().decode('utf-8'))

        ssh.close()

        return result