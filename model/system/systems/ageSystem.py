class ageSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, value=None):
        if component.get_name() == "age":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def get_age(self, entity):
        return entity.get_component_data("age", "age")
    
    def set_age(self, entity, age):
        entity.update_component_data("age", "age", age)

    def update(self):
        for entity in self.entities:
            self.age(entity)

    def age(self, entity):
        self.set_age(entity, self.get_age(entity) + 1)