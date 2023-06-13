import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIScrollingContainer, UIPanel
import os
import math
import xml.etree.ElementTree as ET
from controller.PGEvents import PGEvents

class PGDisplay:
    def __init__(self, map_data, pygame, world, SCREENWIDTH, SCREENHEIGHT):
        # Initialize pygame
        self.world = world
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)

        # Font settings
        self.font = pygame.font.Font('./rec/fonts/computer_pixel-7.ttf', 36)
        
        # Initialize event handler
        self.pgevents = PGEvents(self, pygame, world)

        self.TILESIZE, self.MAPWIDTH, self.MAPHEIGHT = map_data['tilewidth'], map_data['width'], map_data['height']
        self.tilesets, self.tileset_firstgids = [], []

        self.sidebarEnabled = False

        # Camera settings
        self.camera_x, self.camera_y, self.zoom_level = 0, 0, 3

        # Time settings
        self.tick_rate = 60  # Update every x frames
        self.subTick = 0  # Counting frames until next tick
        self.game_paused = False  # Game paused flag
        self.panning = False
        self.curFrame = 0

        self.displayInfo = False

        self.manager = pygame_gui.UIManager((SCREENWIDTH, SCREENHEIGHT))
        self.sidebar_width = 300
        self.button_height = int(50*0.75)  # reduced button height by 25%
        self.button_count = 5
        self.sidebar_height = self.button_height * self.button_count
        self.sidebar = pygame.Rect(0, 0, self.sidebar_width, self.sidebar_height)
        self.sidebar_surface = pygame.Surface((self.sidebar_width, self.sidebar_height))
        self.sidebar_surface.fill((0, 0, 0))
       
        # Draw initial screen
        self.draw_screen()


        # Load tilesets
        for tileset in map_data['tilesets']:
            tsx_path = "./rec/mapfiles/" + tileset['source']
            tsx_root = ET.parse(tsx_path).getroot()
            image_path = os.path.join(os.path.dirname(tsx_path), tsx_root.find('image').get('source'))
            self.tilesets.append(pygame.image.load(image_path).convert_alpha())
            self.tileset_firstgids.append(tileset['firstgid'])

    def draw_tile_sidebar(self, manager, tilesets, rows, tile_size, sidebar_width):
        sidebar_height = rows * tile_size

        # Create a panel for the sidebar
        sidebar_rect = pygame.Rect((0, 0), (sidebar_width, sidebar_height))
        sidebar_panel = UIPanel(relative_rect=sidebar_rect, manager=manager)

        # Create a scrolling container inside the panel
        container_rect = pygame.Rect((0, 0), (sidebar_width, sidebar_height))
        sidebar_container = UIScrollingContainer(relative_rect=container_rect,
                                                manager=manager,
                                                container=sidebar_panel)

        # Create a button for each tile in the tilesets
        buttons = []
        for i, tileset in enumerate(tilesets):
            button_rect = pygame.Rect((0, i * tile_size), (tile_size, tile_size))
            button = UIButton(relative_rect=button_rect,
                            text='',
                            manager=manager,
                            container=sidebar_container,
                            object_id='#tileset_button_' + str(i))
            buttons.append(button)

            # Load the image onto the button
            button.set_image(tileset)
            button.set_dimensions((tile_size, tile_size))

        return sidebar_panel, sidebar_container, buttons

# Usage:
# manager = pygame_gui.UIManager((window_width, window_height))
# draw_sidebar(manager, self.tilesets, rows, tile_size, sidebar_width)

    def draw_sidebar(self):
        if self.sidebarEnabled:
            self.sidebar_surface.fill((0, 0, 0))
            self.manager.update(self.curFrame / 60.0)
            self.manager.draw_ui(self.sidebar_surface)
            self.screen.blit(self.sidebar_surface, (0, 0))  # blit at position (0, 0)

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

                                    
    #draw editor UI (display an array of options when right clicking, depending on the selected entity or empty space)
    def draw_editor_UI(self):
        pass

    # Draws the basic UI elements
    def draw_basic_UI(self):

        # Draw game time as days, hours, and minutes
        days = int(self.world.time / (60 * 24))
        hours = int((self.world.time / 60) % 24)
        minutes = int(self.world.time % 60)

        time_text = self.font.render(f"Days: {days} Hours: {hours} Minutes: {minutes}", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))

        # Draw entity info panel
        if self.displayInfo:

            #draw entity ID

            entityIDText = self.font.render(f'Entity ID: {self.entityInfo.get_id()}', True, (255, 255, 255))
            self.screen.blit(entityIDText, (10, 40))

            componentData = self.entityInfo.get_all_component_data()

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
            path = self.entityInfo.get_component_data("pathfinding", "path")
            if path:
                for i in range(len(path) - 1):
                    pygame.draw.line(self.screen, (255, 0, 0), ((path[i][0] * self.TILESIZE - self.camera_x) * self.zoom_level + self.TILESIZE * self.zoom_level / 2, (path[i][1] * self.TILESIZE - self.camera_y) * self.zoom_level + self.TILESIZE * self.zoom_level / 2), ((path[i + 1][0] * self.TILESIZE - self.camera_x) * self.zoom_level + self.TILESIZE * self.zoom_level / 2, (path[i + 1][1] * self.TILESIZE - self.camera_y) * self.zoom_level + self.TILESIZE * self.zoom_level / 2), 5)


        #draw cursor position at the screen's bottom
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x, tile_y = self.returnMapPos(mouse_x, mouse_y)
        mouse_pos = self.font.render(f'X: {tile_x} Y: {tile_y}', True, (255, 255, 255))
        self.screen.blit(mouse_pos, (10, self.screen.get_height() - 40))

    def draw_screen(self):

        # Fill screen with black
        self.screen.fill((0, 0, 0))

        # Draw tiles
        self.draw_tiles()
        
        # Draw UI
        self.draw_basic_UI() 

        # Draw sidebar
        self.draw_sidebar()

        self.draw_tile_sidebar(self.manager, self.tilesets, 5, self.TILESIZE, self.sidebar_width)

        pygame.display.flip()