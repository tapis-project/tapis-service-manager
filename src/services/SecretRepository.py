from configs.constants import PLATFORM
from model.schema import Platform
from helpers import KubernetesAPIGateway

class SecretRepository:
    def __init__(
        self,
        platform: Platform,
        kubernetes_api_gateway: KubernetesAPIGateway = None,
        is_local = False
    ):
        self._platform = platform
        self._kubernetes_api_gateway = kubernetes_api_gateway
        self._is_local = is_local
        print("IS LOCAL", is_local)

    def get_secret(self):
        return