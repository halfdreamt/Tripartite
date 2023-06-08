class Entity:
    def __init__(self, id):
        self.id = id
        self.components = {}

    def add_component(self, component):
        component_name = component.get_name()
        self.components[component_name] = component

    def remove_component(self, component_name):
        if component_name in self.components:
            self.components[component_name].notify_systems("delete")
            del self.components[component_name]

    def update_component_data(self, component_name, key, new_value):
        if component_name in self.components:
            self.components[component_name].update_data(key, new_value)

    def get_component_data(self, component_name, key):
        if component_name in self.components:
            return self.components[component_name].get_data(key)

class EntityManager:
    def __init__(self, entity_data, component_manager):
        self.entities = []
        self.archetypes = entity_data['archetypes']
        self.component_manager = component_manager

    #TODO: find a better way to overrride, less hardcoded
    # Creates an entity from an archetype
    def create_entity(self, archetype_name, spriteID, x, y):
        archetype = next((a for a in self.archetypes if a['name'] == archetype_name), None)
        if archetype is not None:
            entity = Entity(len(self.entities))
            for component in archetype['components']:
                component_name = component['name']
                component_data = component['data'].copy()  # create a copy here
                if component_name == 'position':
                    component_data['x'] = x
                    component_data['y'] = y
                elif component_name == 'render':
                    component_data['spriteID'] = spriteID
                component = self.component_manager.create_component(entity, component_name, component_data)
                entity.add_component(component)
            self.entities.append(entity)
            return entity
        else:
            raise ValueError(f"No archetype found with name {archetype_name}")
        
    #returns an entity at a given position, or returns false
    def get_entity_at(self, x, y):
        for entity in self.entities:
            if entity.get_component_data('position', 'x') == x and entity.get_component_data('position', 'y') == y:
                return entity
        return False

    def get_entity(self, index):
        return self.entities[index]

    def return_entities(self):
        return self.entities

    def remove_entity(self, index):
        del self.entities[index]
