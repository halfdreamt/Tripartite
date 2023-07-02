import pygame
import os
import math
import xml.etree.ElementTree as ET
from controller.PGEvents import PGEvents
from view.displays.menu import Menu
from view.displays.localView import LocalView

class PGDisplay:
    def __init__(self, map_data, pygame, world, dataFactory, SCREENWIDTH, SCREENHEIGHT):

        self.dataFactory = dataFactory
        self.world = world
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)

        #load tile images from SQL database
        self.tileImages = self.dataFactory.getTileImages()

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
    
        # Calculate the map tile coordinates of the visible screen area
    def calculate_visible_tiles(self, screen_width, screen_height):
        visible_tile_left = max(0, int(self.camera_x / self.TILESIZE))
        visible_tile_top = max(0, int(self.camera_y / self.TILESIZE))
        visible_tile_right = min(self.MAPWIDTH, visible_tile_left + math.ceil(screen_width / (self.TILESIZE * self.zoom_level)))
        visible_tile_bottom = min(self.MAPHEIGHT, visible_tile_top + math.ceil(screen_height / (self.TILESIZE * self.zoom_level)))
        return visible_tile_left, visible_tile_top, visible_tile_right, visible_tile_bottom

    def draw_screen(self):

        # Fill screen with black
        self.screen.fill((0, 0, 0))

        if self.viewMode == "menu":
            self.menu.draw_menu()
        elif self.viewMode == "local":
            self.localView.draw_local_view()
    
        pygame.display.flip()