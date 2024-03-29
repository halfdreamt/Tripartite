import pygame
import math
from view.displays.menu import Menu
from view.displays.localView import LocalView
from view.displays.battleView import BattleView
from model.world import World

class PGDisplay:
    def __init__(self, tile_data, display_settings):

        self.displaySettings = display_settings

        self.viewMode = self.displaySettings['defaultMode']

        self.screen = pygame.display.set_mode((self.displaySettings['screenWidth'], self.displaySettings['screenHeight']), pygame.RESIZABLE)

        #load tile images from SQL database
        self.tileImages = tile_data

        # Font settings
        self.font = pygame.font.Font('./rec/fonts/computer_pixel-7.ttf', 36)

        # Initialize event handler and view classes
        self.menu = Menu(self)
        self.localView = LocalView(self)
        self.battleView = BattleView(self)

        # Camera settings
        self.camera_x, self.camera_y, self.zoom_level = 0, 0, 3

        # Time settings
        self.subTick = 0  # Counting frames until next tick
        self.panning = False
        self.curFrame = 0

        self.displayInfo = False

    # Enables and draws an entity information panel
    def handle_entity_info_display(self, entity):
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

    def set_map(self, map):
        self.curMap = map
        self.draw_screen()

    def set_time(self, time):
        self.time = time

    def set_world_data(self, world_data):
        self.curMap = world_data["map"]
        self.time = world_data["time"]
        self.draw_screen()

    # adjusts x and y values based on camera position, zoom level and tile size
    def return_map_pos(self, x, y):
        tile_x = (x // self.zoom_level + self.camera_x) // self.curMap.TILESIZE
        tile_y = (y // self.zoom_level + self.camera_y) // self.curMap.TILESIZE
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
            visible_tile_left = max(0, int(self.camera_x / self.curMap.TILESIZE))
            visible_tile_top = max(0, int(self.camera_y / self.curMap.TILESIZE))
            visible_tile_right = min(self.curMap.MAPWIDTH, visible_tile_left + math.ceil(screen_width / (self.curMap.TILESIZE * self.zoom_level)))
            visible_tile_bottom = min(self.curMap.MAPHEIGHT, visible_tile_top + math.ceil(screen_height / (self.curMap.TILESIZE * self.zoom_level)))
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