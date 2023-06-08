import json

class Component:
    def __init__(self, entity, name, systems, data):
        self.entity = entity
        self.name = name
        self.systems = systems
        self.data = data

    def update_data(self, key, new_value):
        if key in self.data:
            self.data[key] = new_value
            self.notify_systems()
        else:
            raise KeyError(f"No such key: {key} in data for this component")

    def get_data(self, key):
        return self.data.get(key, None)

    def get_name(self):
        return self.name

    def notify_systems(self):
        for system in self.systems:
            system.component_updated(self)
            

class ComponentManager:
    def __init__(self, filename, systems):
        self.component_types = self.load_component_types(filename)
        self.systems = systems

    def load_component_types(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return data['components']

    def create_component(self, entity, id, data=None):
        component_type = next((c for c in self.component_types if c['id'] == id), None)
        if component_type is not None:
            if data is None:
                data = component_type['data']
            component = Component(entity, component_type['name'], self.systems, data)
            return component
        else:
            raise ValueError(f"No component type found with id {id}")
