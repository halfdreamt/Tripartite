import pygame
import xml.etree.ElementTree as ET

class PGEvents:
    def __init__(self, pgdisplay, pygame, world):
        self.pgdisplay = pgdisplay
        self.world = world
        self.pygame = pygame

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Move camera up
                self.pgdisplay.camera_y -= self.world.map.TILESIZE
            elif event.key == pygame.K_s:  # Move camera down
                self.pgdisplay.camera_y += self.world.map.TILESIZE
            elif event.key == pygame.K_a:  # Move camera left
                self.pgdisplay.camera_x -= self.world.map.TILESIZE
            elif event.key == pygame.K_d:  # Move camera right
                self.pgdisplay.camera_x += self.world.map.TILESIZE
            elif event.key == pygame.K_q:  # Zoom out
                self.zoom_level = max(self.pgdisplay.zoom_level - 0.1, 0.1)  # Prevent zoom level from getting too small
            elif event.key == pygame.K_e:  # Zoom in
                self.pgdisplay.zoom_level += 0.1
            elif event.key == pygame.K_1:  # Set game speed to default
                self.pgdisplay.tick_rate = 60
            elif event.key == pygame.K_2:  # Set game speed to x5
                self.pgdisplay.tick_rate = 30
            elif event.key == pygame.K_3:  # Set game speed to x10
                self.pgdisplay.tick_rate = 10
            elif event.key == pygame.K_4:  # Set game speed to x100
                self.pgdisplay.tick_rate = 1
            elif event.key == pygame.K_SPACE: # Toggle pause
                self.pgdisplay.game_paused = not self.pgdisplay.game_paused
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # Middle mouse button
                self.pgdisplay.panning = True
                self.pgdisplay.pan_start_x, self.pgdisplay.pan_start_y = event.pos
            elif event.button == 4:  # Mouse wheel up
                self.pgdisplay.zoom_level += 0.1
            elif event.button == 5:  # Mouse wheel down
                self.pgdisplay.zoom_level = max(self.pgdisplay.zoom_level - 0.1, 0.1)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:  # Middle mouse button
                self.pgdisplay.panning = False
            elif event.button == 1:  # Left mouse button
                x, y = event.pos
                self.handleMouseClick(x, y)
        elif event.type == pygame.MOUSEMOTION:
            if self.pgdisplay.panning:
                x, y = event.pos
                dx = (self.pgdisplay.pan_start_x - x) * self.pgdisplay.zoom_level
                dy = (self.pgdisplay.pan_start_y - y) * self.pgdisplay.zoom_level
                self.pgdisplay.camera_x += dx
                self.pgdisplay.camera_y += dy
                self.pgdisplay.pan_start_x, self.pgdisplay.pan_start_y = x, y

    def handleMouseClick(self, x, y):
        if self.pgdisplay.displayInfo:
            self.pgdisplay.displayInfo = False
        else:
            tile_x = (x // self.pgdisplay.zoom_level + self.pgdisplay.camera_x) // self.pgdisplay.TILESIZE
            tile_y = (y // self.pgdisplay.zoom_level + self.pgdisplay.camera_y) // self.pgdisplay.TILESIZE
            for entity in self.world.entities:
                if entity.physical.xcoord == tile_x and entity.physical.ycoord == tile_y:
                    self.pgdisplay.displayInfo = True
                    self.pgdisplay.enableEntityInfoDisplay(self.world.getEntityInfo(tile_x, tile_y))
                
