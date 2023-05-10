from model import PlatformEnum
from helpers import KubernetesAPIGateway

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
        print("IS LOCAL", is_local)

    def get_secret(self):
        return