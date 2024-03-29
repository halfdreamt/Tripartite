class Component:
    def __init__(self, entity, name, data, system_manager):
        self.entity = entity
        self.name = name
        self.system_manager = system_manager
        self.data = data
        self.notify_systems("create")

    def update_data(self, key, new_value):
        if key in self.data:
            old_value = self.data[key]
            self.data[key] = new_value
            self.notify_systems("update", key, old_value, new_value)
        else:
            raise KeyError(f"No such key: {key} in data for this component")

    def get_data(self, key):
        return self.data.get(key, None)

    def get_name(self):
        return self.name
    
    def get_all_data(self):
        return self.data

    def notify_systems(self, updateType, key=None, oldValue=None, newValue=None):
        self.system_manager.component_updated(self, updateType, key, oldValue, newValue)
            

class ComponentManager:
    def __init__(self, component_master_data, system_manager):
        self.component_masters = component_master_data
        self.system_manager = system_manager
        
    def create_component(self, entity, name, data=None):
        component_type = next((c for c in self.component_masters if c['name'] == name), None)
        if component_type != None:
            if data is None:
                data = component_type['data']
            component = Component(entity, component_type['name'], data, self.system_manager)
            return component
        else:
            raise ValueError(f"No component type found with id {id}")
