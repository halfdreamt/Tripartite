import pygame
import math
from view.displays.localViewUI import LocalViewUI

class LocalView:
    def __init__(self, pgdisplay):
        self.pgdisplay = pgdisplay
        self.screen = pgdisplay.screen
        self.font = pgdisplay.font
        self.UI = LocalViewUI(pgdisplay)
        self.tileImages = self.pgdisplay.tileImages

    def draw_tiles(self):
        TILESIZE = self.pgdisplay.curMap.TILESIZE
        ZOOMLEVEL = self.pgdisplay.zoom_level
        camera_x = self.pgdisplay.camera_x
        camera_y = self.pgdisplay.camera_y

        screen_width = self.pgdisplay.screen.get_width()
        screen_height = self.pgdisplay.screen.get_height()

        visible_tile_left, visible_tile_top, visible_tile_right, visible_tile_bottom = self.pgdisplay.calculate_visible_tiles(screen_width, screen_height)

        for layer_name, tile_data in self.pgdisplay.curMap.layers.items(): 
            for y in range(visible_tile_top, visible_tile_bottom):
                for x in range(visible_tile_left, visible_tile_right):
                    tile_id = tile_data[y][x] - 1 
                    # Calculate tile position in screen space
                    tile_screen_x = (x * TILESIZE - camera_x) * ZOOMLEVEL
                    tile_screen_y = (y * TILESIZE - camera_y) * ZOOMLEVEL

                    tile_image = self.tileImages[tile_id]
                    tile_image = pygame.transform.scale(tile_image, (int(TILESIZE*ZOOMLEVEL), int(TILESIZE*ZOOMLEVEL)))

                    self.screen.blit(tile_image, (tile_screen_x, tile_screen_y))

        self.draw_darkness(screen_height, screen_width)

    def draw_darkness(self, screen_height, screen_width):

        # Calculate darkness based on time of day
        time_minutes = self.pgdisplay.world.time + self.pgdisplay.curFrame / 60.0
        darkness = 0.5 * (math.cos(math.pi * time_minutes / (12 * 60)) + 1)

        # Create a dark overlay with the calculated darkness and apply it to the entire screen
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(darkness * 200)))
        self.screen.blit(overlay, (0, 0))

    def draw_local_view(self):
        self.draw_tiles()
        self.UI.draw_UI()
