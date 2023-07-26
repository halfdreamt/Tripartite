import pygame
from view.PGDisplay import PGDisplay
from controller.PGEvents import PGEvents
from controller.settingsManager import SettingsManager
from model.modelManager import modelManager
from data.dataFactory import dataFactory

# Initialize pygame
pygame.init()

# Initialize the settings manager with a file path to the config file (contains the file paths to the master files among other settings)
settings_manager = SettingsManager("rec/config.json")
master_file_paths = settings_manager.get_master_file_paths()
display_settings = settings_manager.get_display_settings()

# Initialize data factory with the master file paths (inserts the master json data into the DB if needed)
data_factory = dataFactory(master_file_paths)
master_data = data_factory.get_master_data()
tile_data = data_factory.get_tile_images()

# Initialize the model
ModelManager = modelManager(master_data)

initial_map = ModelManager.get_map()
initial_time = ModelManager.get_time()

# Initialize the display
viewManager = PGDisplay(tile_data, display_settings, initial_map, initial_time)

# Initialize the event handler
controlManager = PGEvents(viewManager, ModelManager)

# Initialize the clock
clock = pygame.time.Clock()

# Main game loop
while not controlManager.quit:
    
    # Input processing
    for input in pygame.event.get():
        if input.type == pygame.QUIT:
            controlManager.quit = True
        else:
            controlManager.handle_input(input)

    # Game time
    if not controlManager.game_paused:
        viewManager.subTick += 1
        if viewManager.subTick >= controlManager.tick_rate:
            viewManager.subTick = 0
            ModelManager.tick()
            
    # Limit the frame rate
    clock.tick(settings_manager.get_frame_rate())

    viewManager.set_time(ModelManager.get_time())

    # Redraw screen
    viewManager.set_map(ModelManager.get_map())

pygame.quit()