import json

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
    def __init__(self, filename, component_manager):
        self.entities = []
        self.archetypes = self.load_archetypes(filename)
        self.component_manager = component_manager

    def load_archetypes(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return data['entities']

    def create_entity(self, archetype_name):
        archetype = next((a for a in self.archetypes if a['type'] == archetype_name), None)
        if archetype is not None:
            entity = Entity(len(self.entities))
            for component_id in archetype['components']:
                component = self.component_manager.create_component(entity, component_id)
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
