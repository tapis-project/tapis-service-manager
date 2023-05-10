from kubernetes import config, client


class KubernetesAPIGateway:
    def __init__(self):
        config.load_incluster_config()
        self._client = client.CoreV1Api()

    def get_client(self):
        return self._client()