import pygame
from view.PGDisplay import PGDisplay
from controller.PGEvents import PGEvents
from controller.settingsManager import SettingsManager

# Initialize pygame
pygame.init()

# Initialize the settings manager with a file path to the config file (contains the file paths to the master files among other settings)
settings_manager = SettingsManager("rec/config.json")

# Initialize the display
viewManager = PGDisplay(settings_manager)

controlManager = PGEvents(viewManager)

# Initialize the clock
clock = pygame.time.Clock()

# Main game loop
while not controlManager.quit:
    
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            controlManager.quit = True
        else:
            controlManager.handle_event(event)

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