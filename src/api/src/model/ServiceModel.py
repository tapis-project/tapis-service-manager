import os

from typing import List
from pydantic import BaseModel, root_validator
from dotenv import load_dotenv

from configs.constants import DEFAULT_COMMANDS, SSH_HOST, SSH_USER, SSH_SECRET_REF
from .CommandModel import CommandModel


load_dotenv()

class ServiceModel(BaseModel):
    name: str
    host: str = SSH_HOST
    user: str = SSH_USER
    ssh_secret_ref: str = SSH_SECRET_REF
    base_path: str
    components: List["ServiceModel"] = []
    use_default_commands: bool = True
    allow: List[str] = []
    is_component: bool = False
    commands: List[CommandModel] = []

    @root_validator(pre=True, allow_reuse=True)
    def pre_prepare_model(cls, values):
        # Set the is_component flag if not set(will only be set to True
        # when components of a service are instantiated)
        is_component = values.get("is_component", False)
        values["is_component"] = is_component

        # Manually validate name and base path as this validator runs before
        # the values are transformed into a pydantic model
        service_name = values.get("name", None)
        if service_name == None:
            raise ValueError("Schema Error: No name provided for service")

        service_base_path = values.get("base_path", None)
        if service_base_path == None:
            raise ValueError("Schema Error: No base_path provided for service")

        values["host"] = values.get("host", SSH_HOST)
        values["user"] = values.get("user", SSH_USER)

        # Set use default commands to True if not set
        if values.get("use_default_commands", True) == True:
            values["commands"] = values.get("commands", []) + DEFAULT_COMMANDS

        # Populate the service allow list with that parent service name. If the
        # service being instantiated is a component, do not add the service(component)
        # name to the allow list
        allow_list = values.get("allow", [service_name])
        if service_name not in allow_list and not is_component:
            allow_list.append(service_name)

        for component in values.get("components", []):
            # Sets all component service's is_component prop to True
            # When the component services are instantiated, they will also
            # run the validation logic above.
            component["is_component"] = True
            
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
            
            # Get the allow list specified on the component. Default to list
            # will only parent service name
            component["allow"] = component.get("allow", allow_list)
            
            # Add parent service name to component allow list if not 
            service_name not in component["allow"] and component["allow"].append(service_name)

            # Inherit the parent services ssh host and ssh user
            component["host"] = component.get("host", values.get("host"))
            component["user"] = component.get("user", values.get("user"))
        
        return values