import pygame
from model.world import World
from view.PGDisplay import PGDisplay
from data.dataFactory import dataFactory
from controller.settingsManager import SettingsManager

# Initialize pygame
pygame.init()

# Initialize the settings manager with a file path to the config file (contains the file paths to the master files among other settings)
settings_manager = SettingsManager("rec/config.json")

# Initialize the display
pgdisplay = PGDisplay(settings_manager)

# Initialize the clock
clock = pygame.time.Clock()

# Main game loop
while not pgdisplay.pgevents.quit:
    
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pgdisplay.pgevents.quit = True
        else:
            pgdisplay.pgevents.handle_event(event)

    # Game time
    if not pgdisplay.pgevents.game_paused:
        pgdisplay.subTick += 1
        if pgdisplay.subTick >= pgdisplay.pgevents.tick_rate:
            pgdisplay.subTick = 0
            pgdisplay.world.tick()
            
    # Limit the frame rate
    clock.tick(settings_manager.get_frame_rate())

    # Redraw screen
    pgdisplay.draw_screen()  

pygame.quit()