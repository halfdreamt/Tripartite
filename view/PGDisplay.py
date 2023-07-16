import pygame
import math
from controller.PGEvents import PGEvents
from view.displays.menu import Menu
from view.displays.localView import LocalView
from view.displays.battleView import BattleView
from model.world import World
from data.dataFactory import dataFactory

class PGDisplay:
    def __init__(self, settings_manager):

        self.settings_manager = settings_manager

        # Initialize data factory with the master file paths (inserts the master json data into the DB if needed)
        self.data_factory = dataFactory(settings_manager.get_master_file_paths())

        self.displaySettings = settings_manager.get_display_settings()

        # Initialize the world with master data (primarily model data)
        self.world = World(self.data_factory.get_master_data())

        self.screen = pygame.display.set_mode((self.displaySettings['screenWidth'], self.displaySettings['screenHeight']), pygame.RESIZABLE)

        #load tile images from SQL database
        self.tileImages = self.data_factory.get_tile_images()

        # Font settings
        self.font = pygame.font.Font('./rec/fonts/computer_pixel-7.ttf', 36)

        # Initialize event handler and view classes
        self.pgevents = PGEvents(self)
        self.menu = Menu(self)
        self.localView = LocalView(self)
        self.battleView = BattleView(self)

        self.viewMode = "menu"
    
        self.tilesets, self.tileset_firstgids = [], []

        # Camera settings
        self.camera_x, self.camera_y, self.zoom_level = 0, 0, 3

        # Time settings
        self.subTick = 0  # Counting frames until next tick
        self.panning = False
        self.curFrame = 0

        self.displayInfo = False
       
        # Draw initial screen
        self.draw_screen()

    # Enables and draws an entity information panel
    def handle_entity_info_display(self, x, y):
        entity = self.world.entity_manager.get_entity_at(x, y)
        if entity:
            self.displayInfo = True
            self.entityInfo = entity
            self.draw_screen()
        else:
            self.displayInfo = False
            self.draw_screen()

    def reset_display(self):
        self.camera_x, self.camera_y = 0, 0
        self.zoom_level = 3
        self.displayInfo = False
        self.viewMode = "local"
        self.draw_screen()

    # adjusts x and y values based on camera position, zoom level and tile size
    def return_map_pos(self, x, y):
        tile_x = (x // self.zoom_level + self.camera_x) // self.world.map.TILESIZE
        tile_y = (y // self.zoom_level + self.camera_y) // self.world.map.TILESIZE
        return tile_x, tile_y
    
        # Calculate the map tile coordinates of the visible screen area
    def calculate_visible_tiles(self, screen_width, screen_height):
        if self.viewMode == "battle":
            visible_tile_left = max(0, int(self.camera_x / self.world.battle_map.TILESIZE))
            visible_tile_top = max(0, int(self.camera_y / self.world.battle_map.TILESIZE))
            visible_tile_right = min(self.world.battle_map.MAPWIDTH, visible_tile_left + math.ceil(screen_width / (self.world.battle_map.TILESIZE * self.zoom_level)))
            visible_tile_bottom = min(self.world.battle_map.MAPHEIGHT, visible_tile_top + math.ceil(screen_height / (self.world.battle_map.TILESIZE * self.zoom_level)))
            return visible_tile_left, visible_tile_top, visible_tile_right, visible_tile_bottom
        elif self.viewMode == "local":
            visible_tile_left = max(0, int(self.camera_x / self.world.map.TILESIZE))
            visible_tile_top = max(0, int(self.camera_y / self.world.map.TILESIZE))
            visible_tile_right = min(self.world.map.MAPWIDTH, visible_tile_left + math.ceil(screen_width / (self.world.map.TILESIZE * self.zoom_level)))
            visible_tile_bottom = min(self.world.map.MAPHEIGHT, visible_tile_top + math.ceil(screen_height / (self.world.map.TILESIZE * self.zoom_level)))
            return visible_tile_left, visible_tile_top, visible_tile_right, visible_tile_bottom

    def draw_screen(self):

        # Fill screen with black
        self.screen.fill((0, 0, 0))

        if self.viewMode == "menu":
            self.menu.draw_menu()
        elif self.viewMode == "local":
            self.localView.draw_local_view()
        elif self.viewMode == "battle":
            self.battleView.draw_local_view()
    
        pygame.display.flip()