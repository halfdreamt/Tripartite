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
                self.set_age(component.entity, 1)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        for entity in self.entities:
            self.age(entity)

    def set_age(self, entity, age):
        entity.update_component_data("age", "age", age)

    def age(self, entity):
        age = entity.get_component_data("age", "age")
        entity.update_component_data("age", "age", entity.get_component_data("age", "age") + 1)
