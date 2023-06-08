class Entity:
    def __init__(self, id):
        self.id = id
        self.components = {}

    def add_component(self, component):
        self.components[type(component).__name__] = component

    def remove_component(self, component_name):
        if component_name in self.components:
            del self.components[component_name]

    def update_component_data(self, component_name, key, new_value):
        if component_name in self.components:
            self.components[component_name].update_data(key, new_value)


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
                component_data = component['data']
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

    def get_entity(self, index):
        return self.entities[index]

    def get_all_entities(self):
        return self.entities

    def remove_entity(self, index):
        del self.entities[index]
