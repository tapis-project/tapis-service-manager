from functools import partial

from configs.constants import PLATFORM, IS_LOCAL
from model.repositories import ServiceRepository, SecretRepository
from model.services import SSHExecService
from model import PlatformEnum
from helpers import KubernetesAPIGateway


class IOCContainer:
    def __init__(self):
        self._configurations = {}
        self._cache = {}

    def register(self, key, handler: callable, as_singleton=True):
        self._configurations[key] = {
            "handler": handler,
            "as_singleton": as_singleton
        }

    # NOTE *args and **kwargs not really implemented in handlers, but good
    # to leave it for extensibility. Perhaps in the future, we may want the object
    # loading to be configurable.
    def load(self, key, *args, **kwargs):
        if key in self._cache:
            return self._cache[key]
        
        configuration = self._configurations.get(key, None)
        if configuration == None:
            raise Exception(f"No service registered with key {key}")

        obj = configuration["handler"](*args, **kwargs)
        if configuration["as_singleton"]:
            self._cache[key] = obj 
            
        return obj


# Container registration handlers
def reg_secret_repository(
    container: IOCContainer,
    platform: PlatformEnum,
    is_local: bool
):
    kubernetes_gateway_api = None
    if platform == PlatformEnum.Kubernetes:
        kubernetes_gateway_api = container.load("kubernetes-api-gateway")
   
    return SecretRepository(
        platform,
        kubernetes_api_gateway=kubernetes_gateway_api,
        is_local=is_local
    )

container = IOCContainer()

# Service registration
container.register("service_repository",
    lambda: ServiceRepository,
)

container.register("kubernetes_api_gateway",
    lambda: KubernetesAPIGateway(),
    as_singleton=True
)

container.register("secret_repository",
    partial(reg_secret_repository, container, PLATFORM, IS_LOCAL)
)

container.register("ssh_exec_service",
    lambda: SSHExecService(
        container.load("secret_repository")
    )
)




