import pygame
from view.PGDisplay import PGDisplay
from controller.PGEvents import PGEvents
from controller.settingsManager import SettingsManager
from model.modelManager import modelManager

# Initialize pygame
pygame.init()

# Initialize the settings manager with a file path to the config file (contains the file paths to the master files among other settings)
settings_manager = SettingsManager("rec/config.json")

# Initialize the model
ModelManager = modelManager(settings_manager)

# Initialize the display
viewManager = PGDisplay(settings_manager, ModelManager)

# Initialize the event handler
controlManager = PGEvents(viewManager)

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
            viewManager.world.tick()
            
    # Limit the frame rate
    clock.tick(settings_manager.get_frame_rate())

    # Redraw screen
    viewManager.draw_screen()  

pygame.quit()