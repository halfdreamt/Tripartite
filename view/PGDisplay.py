import pygame
import os
import xml.etree.ElementTree as ET
from controller.PGEvents import PGEvents
from view.displays.menu import Menu
from view.displays.localView import LocalView

class PGDisplay:
    def __init__(self, map_data, pygame, world, dataFactory, SCREENWIDTH, SCREENHEIGHT):

        self.dataFactory = dataFactory
        self.world = world
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)

        # Font settings
        self.font = pygame.font.Font('./rec/fonts/computer_pixel-7.ttf', 36)

        # Initialize event handler and view classes
        self.pgevents = PGEvents(self, pygame, world)
        self.menu = Menu(self)
        self.localView = LocalView(self)

        self.viewMode = "menu"
        self.running = True
    
        self.TILESIZE, self.MAPWIDTH, self.MAPHEIGHT = map_data['tilewidth'], map_data['width'], map_data['height']
        self.tilesets, self.tileset_firstgids = [], []

        # Camera settings
        self.camera_x, self.camera_y, self.zoom_level = 0, 0, 3

        # Time settings
        self.tick_rate = 60  # Update every x frames
        self.subTick = 0  # Counting frames until next tick
        self.game_paused = True  # Game paused flag
        self.panning = False
        self.curFrame = 0

        self.displayInfo = False
       
        # Draw initial screen
        self.draw_screen()

        # Load tilesets
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


    def draw_screen(self):

        # Fill screen with black
        self.screen.fill((0, 0, 0))

        if self.viewMode == "menu":
            self.menu.draw_menu()
        elif self.viewMode == "local":
            self.localView.draw_local_view()
    
        pygame.display.flip()