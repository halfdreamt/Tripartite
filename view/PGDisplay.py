import pygame
import os
import math
import xml.etree.ElementTree as ET
from controller.PGEvents import PGEvents

class PGDisplay:
    def __init__(self, map_data, pygame, world, SCREENWIDTH, SCREENHEIGHT):
        # Initialize pygame
        pygame.init()
        self.world = world
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
        
        # Initialize event handler
        self.pgevents = PGEvents(self, pygame, world)

        self.TILESIZE, self.MAPWIDTH, self.MAPHEIGHT = map_data['tilewidth'], map_data['width'], map_data['height']
        self.tilesets, self.tileset_firstgids = [], []

        # Font settings
        self.font = pygame.font.Font('./rec/fonts/computer_pixel-7.ttf', 36)

        # Camera settings
        self.camera_x, self.camera_y, self.zoom_level = 0, 0, 3

        # Time settings
        self.tick_rate = 60  # Update every x frames
        self.subTick = 0  # Counting frames until next tick
        self.game_paused = False  # Game paused flag
        self.panning = False
        self.curFrame = 0

        self.displayInfo = False

        # Draw initial screen
        self.draw_screen()

        for tileset in map_data['tilesets']:
            tsx_path = "./rec/mapfiles/" + tileset['source']
            tsx_root = ET.parse(tsx_path).getroot()
            image_path = os.path.join(os.path.dirname(tsx_path), tsx_root.find('image').get('source'))
            self.tilesets.append(pygame.image.load(image_path).convert_alpha())
            self.tileset_firstgids.append(tileset['firstgid'])

    # Enables and draws an entity information panel
    def handleEntityInfoDisplay(self, entity):
        if entity:
            self.displayInfo = True
            self.entityInfo = entity
            self.draw_screen()
        else:
            self.displayInfo = False
            self.draw_screen()

    # adjusts x and y values based on camera position, zoom level and tile size
    def returnMapPos(self, x, y):
        tile_x = (x // self.zoom_level + self.camera_x) // self.TILESIZE
        tile_y = (y // self.zoom_level + self.camera_y) // self.TILESIZE
        return tile_x, tile_y

    def draw_tiles(self):
        # Calculate darkness based on time of day
        time_minutes = self.world.time + self.curFrame / 60.0
        darkness = 0.5 * (math.cos(math.pi * time_minutes / (12 * 60)) + 1)

        
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        for layer_name, tile_data in self.world.map.layers.items():
            for y in range(self.MAPHEIGHT):
                for x in range(self.MAPWIDTH):
                    tile_id = tile_data[y][x]
                    if tile_id:
                        # Calculate tile position in screen space
                        tile_screen_x = (x * self.TILESIZE - self.camera_x) * self.zoom_level
                        tile_screen_y = (y * self.TILESIZE - self.camera_y) * self.zoom_level

                        # Check if tile is within the visible screen area
                        if tile_screen_x + self.TILESIZE >= 0 and tile_screen_x < screen_width and tile_screen_y + self.TILESIZE >= 0 and tile_screen_y < screen_height:
                            for i in reversed(range(len(self.tileset_firstgids))):
                                if tile_id >= self.tileset_firstgids[i]:
                                    tile_id -= self.tileset_firstgids[i]
                                    tile_x, tile_y = tile_id % (self.tilesets[i].get_width() // self.TILESIZE), tile_id // (self.tilesets[i].get_width() // self.TILESIZE)
                                    tile_image = self.tilesets[i].subsurface(pygame.Rect(tile_x * self.TILESIZE, tile_y * self.TILESIZE, self.TILESIZE, self.TILESIZE))
                                    tile_image = pygame.transform.scale(tile_image, (int(self.TILESIZE*self.zoom_level), int(self.TILESIZE*self.zoom_level)))

                                    # Create a dark overlay with the calculated darkness
                                    overlay = pygame.Surface(tile_image.get_size(), pygame.SRCALPHA)
                                    overlay.fill((0, 0, 0, int(darkness * 200)))

                                    # Apply the overlay to the tile image
                                    tile_image.blit(overlay, (0, 0))

                                    self.screen.blit(tile_image, (tile_screen_x, tile_screen_y))
                                    break

    def draw_screen(self):

        # Fill screen with black
        self.screen.fill((0, 0, 0))

        # Draw tiles
        self.draw_tiles()
        
        # Draw game time as days, hours, and minutes
        days = int(self.world.time / (60 * 24))
        hours = int((self.world.time / 60) % 24)
        minutes = int(self.world.time % 60)

        time_text = self.font.render(f"Days: {days} Hours: {hours} Minutes: {minutes}", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))

        # Draw entity info panel
        if self.displayInfo:
            # Draw name
            entity_name = self.font.render(self.entityInfo.get_component_data("name", "name"), True, (255, 255, 255))
            self.screen.blit(entity_name, (10, 50))

            # Draw entity position
            entity_position = self.font.render(f'X: {self.entityInfo.get_component_data("position", "x")} Y: {self.entityInfo.get_component_data("position", "y")}', True, (255, 255, 255))
            self.screen.blit(entity_position, (10, 80))

            #draw entity needs 
            entity_needs = self.font.render(f'Needs: {self.entityInfo.get_component_data("needs", "needs")}', True, (255, 255, 255))
            self.screen.blit(entity_needs, (10, 110))

            #draw entity pathfinding directions
            entity_pathfinding = self.font.render(f'Pathfinding: {self.entityInfo.get_component_data("pathfinding", "directions")}', True, (255, 255, 255))
            self.screen.blit(entity_pathfinding, (10, 140))

            #drawn wander state
            entity_wander = self.font.render(f'Wander: {self.entityInfo.get_component_data("wander", "active")}', True, (255, 255, 255))
            self.screen.blit(entity_wander, (10, 170))


            if self.entityInfo.has_component("health") and self.entityInfo.has_component("thirst"):
                #draw bar for entity health with label
                current_health = self.entityInfo.get_component_data("health", "current")
                max_health = self.entityInfo.get_component_data("health", "max")
                health_bar = pygame.Rect(10, 200, 200, 20)
                pygame.draw.rect(self.screen, (255, 0, 0), health_bar)
                health_bar = pygame.Rect(10, 200, 200 * (current_health / max_health), 20)
                pygame.draw.rect(self.screen, (0, 255, 0), health_bar)
                entity_health = self.font.render(f'Health: {current_health}/{max_health}', True, (255, 255, 255))
                self.screen.blit(entity_health, (10, 200))

                #draw bar for entity thirst with label
                current_health = self.entityInfo.get_component_data("thirst", "current")
                max_health = self.entityInfo.get_component_data("thirst", "max")
                health_bar = pygame.Rect(10, 230, 200, 20)
                pygame.draw.rect(self.screen, (255, 0, 0), health_bar)
                health_bar = pygame.Rect(10, 230, 200 * (current_health / max_health), 20)
                pygame.draw.rect(self.screen, (0, 0, 255), health_bar)
                entity_health = self.font.render(f'Thirst: {current_health}/{max_health}', True, (255, 255, 255))
                self.screen.blit(entity_health, (10, 230))

                #highlight entity's path
                path = self.entityInfo.get_component_data("pathfinding", "path")
                if path:
                    for i in range(len(path) - 1):
                        pygame.draw.line(self.screen, (255, 0, 0), ((path[i][0] * self.TILESIZE - self.camera_x) * self.zoom_level + self.TILESIZE * self.zoom_level / 2, (path[i][1] * self.TILESIZE - self.camera_y) * self.zoom_level + self.TILESIZE * self.zoom_level / 2), ((path[i + 1][0] * self.TILESIZE - self.camera_x) * self.zoom_level + self.TILESIZE * self.zoom_level / 2, (path[i + 1][1] * self.TILESIZE - self.camera_y) * self.zoom_level + self.TILESIZE * self.zoom_level / 2), 5)

                # Draw entity's age
                entity_age = self.font.render(f'Age: {self.entityInfo.get_component_data("age", "age")}', True, (255, 255, 255))
                self.screen.blit(entity_age, (10, 260))
                
        #draw cursor position at the screen's bottom
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x, tile_y = self.returnMapPos(mouse_x, mouse_y)
        mouse_pos = self.font.render(f'X: {tile_x} Y: {tile_y}', True, (255, 255, 255))
        self.screen.blit(mouse_pos, (10, self.screen.get_height() - 40))

        pygame.display.flip()