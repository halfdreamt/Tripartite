import pygame
import math

class LocalViewUI:
    def __init__(self, pgdisplay):
        self.pgdisplay = pgdisplay
        self.screen = pgdisplay.screen
        self.font = pgdisplay.font
        self.entityInfo = None

    # Draws the basic UI elements
    def draw_basic_UI(self):

        # Draw game time as days, hours, and minutes
        days = int(self.pgdisplay.world.time / (60 * 24))
        hours = int((self.pgdisplay.world.time / 60) % 24)
        minutes = int(self.pgdisplay.world.time % 60)

        time_text = self.font.render(f"Days: {days} Hours: {hours} Minutes: {minutes}", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))

        #draw cursor position at the screen's bottom
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x, tile_y = self.pgdisplay.returnMapPos(mouse_x, mouse_y)
        mouse_pos = self.font.render(f'X: {tile_x} Y: {tile_y}', True, (255, 255, 255))
        self.screen.blit(mouse_pos, (10, self.screen.get_height() - 40))

    #draw entity info panel if an entity is selected
    def draw_entity_info(self):
        self.entityInfo = self.pgdisplay.entityInfo
        #draw entity ID
        entityIDText = self.font.render(f'Entity ID: {self.entityInfo.get_id()}', True, (255, 255, 255))
        self.screen.blit(entityIDText, (10, 40))

        componentData = self.pgdisplay.entityInfo.get_all_component_data()

        # For each component data, draw a label and the data
        for componentDataKey in componentData:

            # Draw health and thirst bars if entity has health and thirst components
            if componentDataKey == "health" or componentDataKey == "thirst":
                current_health = componentData[componentDataKey]["current"]
                max_health = componentData[componentDataKey]["max"]
                health_bar = pygame.Rect(10, 50 + 30 * list(componentData.keys()).index(componentDataKey) + 20, 200, 20)
                pygame.draw.rect(self.screen, (255, 0, 0), health_bar)
                health_bar = pygame.Rect(10, 50 + 30 * list(componentData.keys()).index(componentDataKey) + 20, 200 * (current_health / max_health), 20)
                pygame.draw.rect(self.screen, (0, 255, 0), health_bar)

            componentDataText = self.font.render(f'{componentDataKey}: {componentData[componentDataKey]}', True, (255, 255, 255))
            self.screen.blit(componentDataText, (10, 60 + 30 * list(componentData.keys()).index(componentDataKey)))

        #highlight entity's path
        path = self.pgdisplay.entityInfo.get_component_data("pathfinding", "path")
        if path:
            for i in range(len(path) - 1):
                pygame.draw.line(self.screen, (255, 0, 0), ((path[i][0] * self.pgdisplay.TILESIZE - self.pgdisplay.camera_x) * self.pgdisplay.zoom_level + self.pgdisplay.TILESIZE * self.pgdisplay.zoom_level / 2, (path[i][1] * self.pgdisplay.TILESIZE - self.pgdisplay.camera_y) * self.pgdisplay.zoom_level + self.pgdisplay.TILESIZE * self.pgdisplay.zoom_level / 2), ((path[i + 1][0] * self.pgdisplay.TILESIZE - self.pgdisplay.camera_x) * self.pgdisplay.zoom_level + self.pgdisplay.TILESIZE * self.pgdisplay.zoom_level / 2, (path[i + 1][1] * self.pgdisplay.TILESIZE - self.pgdisplay.camera_y) * self.pgdisplay.zoom_level + self.pgdisplay.TILESIZE * self.pgdisplay.zoom_level / 2), 5)


    def draw_UI(self):
        self.draw_basic_UI()
        if self.pgdisplay.displayInfo:
            self.draw_entity_info()