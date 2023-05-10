from .ServiceModel import ServiceModel


class ComponentModel(ServiceModel):
    base_path: str = None
    is_component: bool = True