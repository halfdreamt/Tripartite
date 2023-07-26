import pygame

class PGEvents:
    def __init__(self, pgdisplay):
        self.pgdisplay = pgdisplay
        self.game_paused = True
        self.quit = False
        self.tick_rate = 60

    def handle_input(self, input):
        if input.type == pygame.KEYDOWN:
            if input.key == pygame.K_w:  # Move camera up
                self.pgdisplay.camera_y -= self.pgdisplay.curMap.TILESIZE
            elif input.key == pygame.K_s:  # Move camera down
                self.pgdisplay.camera_y += self.pgdisplay.curMap.TILESIZE
            elif input.key == pygame.K_a:  # Move camera left
                self.pgdisplay.camera_x -= self.pgdisplay.curMap.TILESIZE
            elif input.key == pygame.K_d:  # Move camera right
                self.pgdisplay.camera_x += self.pgdisplay.curMap.TILESIZE
            elif input.key == pygame.K_q:  # Zoom out
                self.zoom_level = max(self.pgdisplay.zoom_level - 0.1, 0.1)  # Prinput zoom level from getting too small
            elif input.key == pygame.K_e:  # Zoom in
                self.pgdisplay.zoom_level += 0.1
            elif input.key == pygame.K_1:  # Set game speed to default
                self.tick_rate = 60
            elif input.key == pygame.K_2:  # Set game speed to x2
                self.tick_rate = 30
            elif input.key == pygame.K_3:  # Set game speed to x10
                self.tick_rate = 6
            elif input.key == pygame.K_4:  # Set game speed to x60
                self.tick_rate = 1
            elif input.key == pygame.K_SPACE: # Toggle pause
                self.game_paused = not self.game_paused
            elif input.key == pygame.K_ESCAPE: # Toggle menu
                if self.pgdisplay.viewMode == "menu":
                    self.pgdisplay.viewMode = "local"
                    self.game_paused = False
                elif self.pgdisplay.viewMode == "local":
                    self.pgdisplay.viewMode = "menu"
                    self.game_paused = True
                elif self.pgdisplay.viewMode == "battle":
                    self.pgdisplay.viewMode = "menu"
                    self.game_paused = True
                self.pgdisplay.draw_screen()
                
        elif input.type == pygame.MOUSEBUTTONDOWN:
            if input.button == 2:  # Middle mouse button
                self.pgdisplay.panning = True
                self.pgdisplay.pan_start_x, self.pgdisplay.pan_start_y = input.pos
            elif input.button == 4:  # Mouse wheel up
                self.pgdisplay.zoom_level += 0.1
            elif input.button == 5:  # Mouse wheel down
                self.pgdisplay.zoom_level = max(self.pgdisplay.zoom_level - 0.1, 0.1)
        elif input.type == pygame.MOUSEBUTTONUP:
            if input.button == 2:  # Middle mouse button
                self.pgdisplay.panning = False
            elif input.button == 1:  # Left mouse button
                x, y = input.pos
                self.handle_left_mouse_click(x, y)
        elif input.type == pygame.MOUSEMOTION:
            if self.pgdisplay.panning:
                x, y = input.pos
                dx = (self.pgdisplay.pan_start_x - x) * self.pgdisplay.zoom_level
                dy = (self.pgdisplay.pan_start_y - y) * self.pgdisplay.zoom_level
                self.pgdisplay.camera_x += dx
                self.pgdisplay.camera_y += dy
                self.pgdisplay.pan_start_x, self.pgdisplay.pan_start_y = x, y

    def handle_left_mouse_click(self, x, y):
        new_x, new_y = self.pgdisplay.return_map_pos(x, y)
        if self.pgdisplay.viewMode == "menu":
            if self.pgdisplay.menu.continue_button.collidepoint(x, y):
                self.pgdisplay.viewMode = "local"
                self.game_paused = False
                self.pgdisplay.draw_screen()
            elif self.pgdisplay.menu.quit_button.collidepoint(x, y):
                self.quit = True
            elif self.pgdisplay.menu.new_town_button.collidepoint(x, y):
                self.reset_game()
            elif self.pgdisplay.menu.battle_button.collidepoint(x, y):
                self.pgdisplay.viewMode = "battle"
                self.pgdisplay.draw_screen()
        elif self.pgdisplay.viewMode == "local":
            self.pgdisplay.handle_entity_info_display(new_x, new_y)

    def reset_game(self):
        self.game_paused = True
        self.tick_rate = 60
        self.pgdisplay.world.reset_world()
        self.pgdisplay.reset_display()

    def load_battle_map(self):
        self.game_paused = True
        self.tick_rate = 60
        self.pgdisplay.world.initialize_battle_map()
        self.pgdisplay.reset_display()