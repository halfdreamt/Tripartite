import pygame

class Menu:
    def __init__(self, pgdisplay):
        self.pgdisplay = pgdisplay
        self.screen = pgdisplay.screen
        self.font = pgdisplay.font
        self.continue_button = None
        self.new_town_button = None
        self.settings_button = None
        self.quit_button = None

    # Draw initial game menu, currently with options for town mode, or battle mode, in the center of the screen
    def draw_menu(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Draw continue button
        self.continue_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 - 250, 200, 100)
        pygame.draw.rect(self.screen, (255, 255, 255), self.continue_button)
        continue_text = self.font.render("Continue", True, (0, 0, 0))
        self.screen.blit(continue_text, (screen_width / 2 - continue_text.get_width() / 2, screen_height / 2 - 200 - continue_text.get_height() / 2))

        # Draw new town button
        self.new_town_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 - 100, 200, 100)
        pygame.draw.rect(self.screen, (255, 255, 255), self.new_town_button)
        new_town_text = self.font.render("New Town", True, (0, 0, 0))
        self.screen.blit(new_town_text, (screen_width / 2 - new_town_text.get_width() / 2, screen_height / 2  - 50 - new_town_text.get_height() / 2))

        # Draw settings button
        self.settings_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 50, 200, 100)
        pygame.draw.rect(self.screen, (255, 255, 255), self.settings_button)
        settings_text = self.font.render("Settings", True, (0, 0, 0))
        self.screen.blit(settings_text, (screen_width / 2 - settings_text.get_width() / 2, screen_height / 2 + 100 - settings_text.get_height() / 2))

        # Draw quit button
        self.quit_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 200, 200, 100)
        pygame.draw.rect(self.screen, (255, 255, 255), self.quit_button)
        quit_text = self.font.render("Quit", True, (0, 0, 0))
        self.screen.blit(quit_text, (screen_width / 2 - quit_text.get_width() / 2, screen_height / 2 + 250 - quit_text.get_height() / 2))