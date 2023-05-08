import enum, os

from typing import List
from pydantic import BaseModel, root_validator

from configs.constants import DEFAULT_COMMANDS


class Scope(enum.Enum):
    Service = "service"
    Component = "component"
    
class Command(BaseModel):
    name: str
    scripts: List[str]

class Service(BaseModel):
    name: str
    base_path: str
    components: List["Service"] = []
    use_default_commands: bool = True
    allow: List[str] = []
    is_component: bool = False
    commands: List[Command] = []

    @root_validator(pre=True, allow_reuse=True)
    def pre_prepare_model(cls, values):
        # Manually validate name and base path as this validator runs before
        # the values are transformed into a pydantic model
        service_name = values.get("name", None)
        if service_name == None:
            raise ValueError("Schema Error: No name provided for service")

        service_base_path = values.get("base_path", None)
        if service_base_path == None:
            raise ValueError("Schema Error: No base_path provided for service")

        # Set use default commands to True if not set
        if values.get("use_default_commands", True) == True:
            values["commands"] = values.get("commands", []) + DEFAULT_COMMANDS

        # Populate the service allow list with that parent service name
        allow_list = values.get("allow", [service_name])
        if service_name not in allow_list:
            allow_list.append(service_name)

        for component in values.get("components", []):
            component["is_component"] = True # TODO is this needed?
            
            # Manually validate component name as this validator runs before
            # the values are transformed into a pydantic model
            component_name = component.get("name", None)
            if component_name == None:
                raise ValueError("Schema Error: No name provided for component")

            # Component inherits the parent base path if no base path is set. Base
            # path is constructed using parent base path and component name
            parent_base_path = service_base_path
            if component.get("base_path", None) == None:
                component["base_path"] = os.path.join(parent_base_path, component["name"])
            
            # Populate the component allow list with that parent service name
            component_allow_list = component.get("allow", [service_name])
            if service_name not in component_allow_list:
                component_allow_list.append(service_name)

            component["allow"] = component_allow_list
        
        return values

    # @root_validator(allow_reuse=True)
    # def post_prepare_commands(cls, values):
    #     return values
        


class Component(Service):
    base_path: str = None
    is_component: bool = True

# Service.update_forward_refs()