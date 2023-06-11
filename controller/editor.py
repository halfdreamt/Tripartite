import pygame

class editor:
    def __init__(self, world, pgdisplay):
        self.world = world
        self.pgdisplay = pgdisplay
        self.font = pgdisplay.font

    # check if the given map location has an entity - if so, call entity editor function, if not, call world editor function
    def handleRightMouseClick(self, entity):
        if entity:
            self.pgdisplay.handleEntityEditor(entity)
        else:
            self.handleWorldEditor()

    # creates a surface with a list of components and their values, and allows the user to edit them
    def handleEntityEditor(self, entity):
        component_data = entity.get_all_component_data()
        component_data_keys = list(component_data.keys())
        component_data_values = list(component_data.values())
        component_data_surface = pygame.Surface((300, 30 * len(component_data_keys)))
        component_data_surface.fill((0, 0, 0))
        for i in range(len(component_data_keys)):
            component_data_text = self.font.render(f'{component_data_keys[i]}: {component_data_values[i]}', True, (255, 255, 255))
            component_data_surface.blit(component_data_text, (10, 30 * i))
        self.pgdisplay.screen.blit(component_data_surface, (self.pgdisplay.screen.get_width() - 300, 0))


    # handle world editor
    def handleWorldEditor(self):
        pass

