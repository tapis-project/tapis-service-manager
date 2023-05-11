from model import ServiceModel
from model.data import services

class ServiceRepository:
    @classmethod
    def list_services(_):
        models = []
        for service in services:
            models.append(ServiceModel(**service))

        return models

    @classmethod
    def get_service(_, service_name):
        service_models = ServiceRepository.list_services()
        model = next(filter(lambda service: service.name == service_name, service_models), None)
        
        return model

    @classmethod
    def get_component(_, service_name, component_name):
        service = ServiceRepository.get_service(service_name)
        component = next(
            filter(
                lambda component: component.name == component_name,
                service.components
            ),
            None
        )
        
        return component

    @classmethod
    def list_components(_, service_name):
        model = ServiceRepository.get_service(service_name)
        
        return model.components

    @classmethod
    def list_commands(_, service_name):
        model = ServiceRepository.get_service(service_name)
        
        return model.commands

    @classmethod
    def get_command(_, service, command_name):
        command = next(
            filter(lambda command: command.name == command_name, service.commands),
            None
        )
        
        return command

    @classmethod
    def list_component_commands(_, service_name, component_name):
        component = ServiceRepository.get_component(service_name, component_name)
        
        return component.commands

    @classmethod
    def get_component_command(_, service_name, component_name, command_name):
        component = ServiceRepository.get_component(service_name, component_name)
        command = next(
            filter(lambda command: command.name == command_name, component.commands),
            None
        )
        
        return command