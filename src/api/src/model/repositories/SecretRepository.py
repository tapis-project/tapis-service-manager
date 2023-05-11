import base64, io

from model import PlatformEnum
from helpers import KubernetesAPIGateway
from errors import ServerError

class SecretRepository:
    def __init__(
        self,
        platform: PlatformEnum,
        kubernetes_api_gateway: KubernetesAPIGateway = None,
        is_local = False
    ):
        self._platform = platform
        self._kubernetes_api_gateway = kubernetes_api_gateway
        self._is_local = is_local

    def get_secret(self, ssh_secret_ref) -> io.StringIO:
        if self._is_local:
            try:
                with open(ssh_secret_ref, 'r') as file:
                    return io.StringIO(file.read())
            except Exception as e:
                raise ServerError(e)
        
        try:
            if self._platform == PlatformEnum.Kubernetes:
                encoded_ssh_key = self._kubernetes_api_gateway.get_secret(ssh_secret_ref)
            elif self._platform == PlatformEnum.DockerCompose:
                encoded_ssh_key = ""
            else:
                raise ServerError(f"Platform '{self._platform}' not implemented")

            decoded_ssh_key = io.StringIO(base64.b64decode(str(encoded_ssh_key)).decode("utf-8"))
        except Exception as e:
            raise ServerError(e)
            
        return decoded_ssh_key
