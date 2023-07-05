import pygame
from model.world import World
from view.PGDisplay import PGDisplay
from data.dataFactory import dataFactory
from controller.settingsManager import SettingsManager

# Initialize pygame
pygame.init()

# Initialize the settings manager with a file path to the config file, which contains the file paths to the master files among other settings
settings_manager = SettingsManager("rec/config.json")

# Get the master data file paths and display settings from the settings manager (master data is for first time setup)
masterFilePaths = settings_manager.get_master_file_paths()
displaySettings = settings_manager.get_display_settings()

# Initialize data factory with the master file paths, which inserts the master json data into the DB 
data_factory = dataFactory(masterFilePaths)

# Load master from SQL database for world
masterData = data_factory.get_master_data()

# Initialize the world (primarily model data)
world = World(masterData)

# Initialize the display, which also initializes the event handler
pgdisplay = PGDisplay(masterData['map_master'], world, data_factory.get_tile_images(), displaySettings)

# Initialize the clock
clock = pygame.time.Clock()

# Main game loop
while pgdisplay.running:
    
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pgdisplay.running = False
        else:
            pgdisplay.pgevents.handle_event(event)

    # Game time
    if not pgdisplay.pgevents.game_paused:
        pgdisplay.subTick += 1
        if pgdisplay.subTick >= pgdisplay.tick_rate:
            pgdisplay.subTick = 0
            world.tick()
            
    # Limit the frame rate
    clock.tick(displaySettings['framerate'])

    # Redraw screen
    pgdisplay.draw_screen()  

pygame.quit()