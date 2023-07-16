import pygame
from model.world import World
from view.PGDisplay import PGDisplay
from data.dataFactory import dataFactory
from controller.settingsManager import SettingsManager

# Initialize pygame
pygame.init()

# Initialize the settings manager with a file path to the config file (contains the file paths to the master files among other settings)
settings_manager = SettingsManager("rec/config.json")

# Initialize data factory with the master file paths (inserts the master json data into the DB if needed)
data_factory = dataFactory(settings_manager.get_master_file_paths())

# Initialize the world with master data (primarily model data)
world = World(data_factory.get_master_data())

# Initialize the display with map data, reference to world, tile data, display settings (also initializes the event handler)
pgdisplay = PGDisplay(data_factory.get_map_master(), world, data_factory.get_tile_images(), settings_manager.get_display_settings())

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
            world.tick()
            
    # Limit the frame rate
    clock.tick(settings_manager.get_frame_rate())

    # Redraw screen
    pgdisplay.draw_screen()  

pygame.quit()