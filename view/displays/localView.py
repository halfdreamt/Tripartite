import pygame
import math
from view.displays.localViewUI import LocalViewUI

class LocalView:
    def __init__(self, pgdisplay):
        self.pgdisplay = pgdisplay
        self.screen = pgdisplay.screen
        self.font = pgdisplay.font
        self.UI = LocalViewUI(pgdisplay)

    def draw_tiles(self):
        # Calculate darkness based on time of day
        time_minutes = self.pgdisplay.world.time + self.pgdisplay.curFrame / 60.0
        darkness = 0.5 * (math.cos(math.pi * time_minutes / (12 * 60)) + 1)

        TILESIZE = self.pgdisplay.TILESIZE

        screen_width = self.pgdisplay.screen.get_width()
        screen_height = self.pgdisplay.screen.get_height()

        visible_tile_left, visible_tile_top, visible_tile_right, visible_tile_bottom = self.pgdisplay.calculate_visible_tiles(screen_width, screen_height)

        for layer_name, tile_data in self.pgdisplay.world.map.layers.items():
            for y in range(visible_tile_top, visible_tile_bottom):
                for x in range(visible_tile_left, visible_tile_right):
                    tile_id = tile_data[y][x]
                    if tile_id:
                        # Calculate tile position in screen space
                        tile_screen_x = (x * TILESIZE - self.pgdisplay.camera_x) * self.pgdisplay.zoom_level
                        tile_screen_y = (y * TILESIZE - self.pgdisplay.camera_y) * self.pgdisplay.zoom_level

                        for i in reversed(range(len(self.pgdisplay.tileset_firstgids))):
                            if tile_id >= self.pgdisplay.tileset_firstgids[i]:
                                tile_id -= self.pgdisplay.tileset_firstgids[i]
                                tile_x, tile_y = tile_id % (self.pgdisplay.tilesets[i].get_width() // TILESIZE), tile_id // (self.pgdisplay.tilesets[i].get_width() // TILESIZE)
                                tile_image = self.pgdisplay.tilesets[i].subsurface(pygame.Rect(tile_x * TILESIZE, tile_y * TILESIZE, TILESIZE, TILESIZE))
                                tile_image = pygame.transform.scale(tile_image, (int(TILESIZE*self.pgdisplay.zoom_level), int(TILESIZE*self.pgdisplay.zoom_level)))

                                # Create a dark overlay with the calculated darkness
                                overlay = pygame.Surface(tile_image.get_size(), pygame.SRCALPHA)
                                overlay.fill((0, 0, 0, int(darkness * 200)))

                                # Apply the overlay to the tile image
                                tile_image.blit(overlay, (0, 0))

                                self.screen.blit(tile_image, (tile_screen_x, tile_screen_y))

    def draw_local_view(self):
        self.draw_tiles()
        self.UI.draw_UI()