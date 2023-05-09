from functools import partial

from configs.constants import PLATFORM, IS_LOCAL
from .ServiceRepository import ServiceRepository
from .SecretRepository import SecretRepository
from helpers import KubernetesAPIGateway
from model.schema import Platform


class IOCContainer:
    def __init__(self):
        self._services = {}
        self._cache = {}

    def register(self, key, handler: callable, as_singleton=True):
        self._services[key] = {
            "handler": handler,
            "as_singleton": as_singleton
        }

    def load(self, key, *args, **kwargs):
        if key in self._cache:
            return self._cache[key]


        if key in self._services:
            service = self._services[key]["handler"](*args, **kwargs)
            if self._services[key]["as_singleton"]:
                self._cache[key] = service 
            
            return service 

        raise Exception(f"No service registered with key {key}")

# Container registration callables
def reg_secret_repository(
    container: IOCContainer,
    platform: Platform,
    is_local: bool
):
    kubernetes_gateway_api = None
    if platform == Platform.Kubernetes:
        kubernetes_gateway_api = container.load("kubernetes-api-gateway")
   
    return SecretRepository(
        platform,
        kubernetes_api_gateway=kubernetes_gateway_api,
        is_local=is_local
    )

container = IOCContainer()

# Service registration
container.register("service-repository",
    lambda: ServiceRepository,
)

container.register("kubernetes-api-gateway",
    lambda: KubernetesAPIGateway(),
    as_singleton=True
)

container.register("secret-repository",
    partial(reg_secret_repository, container, PLATFORM, IS_LOCAL)
)




