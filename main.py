import pygame
from model.world import World
from view.PGDisplay import PGDisplay
from data.dataFactory import dataFactory
from controller.settingsManager import SettingsManager

# Initialize pygame
pygame.init()

# Initialize the settings manager
SettingsManager = SettingsManager("rec/config.json")
master_file_paths = SettingsManager.get_master_file_paths()
MASTERDATA = SettingsManager.get_master_data()

# Initialize data factory and insert master data into database
dataFactory = dataFactory(master_file_paths)

#load archetype data and component data from SQL database
archetype_data_DB = dataFactory.getArchetypes()
component_master_data = dataFactory.getComponentMasters()

map_data = MASTERDATA["tile_master"]

# initialize the display, gamestate, and clock
displaySettings = SettingsManager.get_display_settings()
world = World(map_data, archetype_data_DB, component_master_data)
pgdisplay = PGDisplay(map_data, world, dataFactory.getTileImages(), displaySettings)
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
    if not pgdisplay.game_paused:
        pgdisplay.subTick += 1
        if pgdisplay.subTick >= pgdisplay.tick_rate:
            pgdisplay.subTick = 0
            world.tick()
            
    # Limit the frame rate
    clock.tick(displaySettings['FRAMERATE'])

    # Redraw screen
    pgdisplay.draw_screen()  

pygame.quit()