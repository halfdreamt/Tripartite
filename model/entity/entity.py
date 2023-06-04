import json
from model.component.physical_component import physical_component
from model.component.mental_component import mental_component
from model.component.spiritual_component import spiritual_component

class Entity:
    def __init__(self, sprite, x, y, world, type):
        # load settings from JSON file
        with open('rec/entity_settings.json', 'r') as file:
            settings = json.load(file)

        strSprite = str(sprite)

        if strSprite not in settings:
            raise Exception(f"No settings found for sprite {strSprite}")

        entity_settings = settings[strSprite]

        # set local data and references 
        self.world = world
        self.type = entity_settings["type"]
        self.name = entity_settings["name"]
        alive = entity_settings["alive"]
        health = entity_settings["health"]
        thirst = entity_settings.get("thirst")

        if self.type == "spiritual" or self.type == "mental" or self.type == "physical":
            self.physical = physical_component(sprite, x, y, self, alive, health, thirst)
            if self.type == "mental" or self.type == "spiritual":
                self.mental = mental_component(self)
                if self.type == "spiritual":
                    self.spiritual = spiritual_component(self)

    # Iterates through all components and updates them, equal to one step through the game loop
    def update(self):
        if self.type == "spiritual" or self.type == "mental" or self.type == "physical":
            self.physical.physical_system.update()
            if self.type == "mental" or self.type == "spiritual":
                self.mental.mental_system.update()
                
