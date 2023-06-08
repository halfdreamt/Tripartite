class Component:
    def __init__(self, entity, name, data, system_manager):
        self.entity = entity
        self.name = name
        self.system_manager = system_manager
        self.data = data
        self.notify_systems("create")

    def update_data(self, key, new_value):
        if key in self.data:
            self.data[key] = new_value
            self.notify_systems("update")
        else:
            raise KeyError(f"No such key: {key} in data for this component")

    def get_data(self, key):
        return self.data.get(key, None)

    def get_name(self):
        return self.name

    def notify_systems(self, updateType):
        self.system_manager.component_updated(self, updateType)
            

class ComponentManager:
    def __init__(self, component_data, system_manager):
        self.component_types = component_data['components']
        self.system_manager = system_manager
        
    def create_component(self, entity, name, data=None):
        component_type = next((c for c in self.component_types if c['name'] == name), None)
        if component_type is not None:
            if data is None:
                data = component_type['data']
            component = Component(entity, component_type['name'], data, self.system_manager)
            return component
        else:
            raise ValueError(f"No component type found with id {id}")
