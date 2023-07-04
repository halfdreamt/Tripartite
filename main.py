import pygame
from model.world import World
from view.PGDisplay import PGDisplay
from data.dataFactory import dataFactory
from controller.settingsManager import SettingsManager

# Initialize pygame
pygame.init()

# Initialize the settings manager
SettingsManager = SettingsManager("rec/config.json")
masterFilePaths = SettingsManager.get_master_file_paths()
displaySettings = SettingsManager.get_display_settings()

# Initialize data factory and insert master data into database
dataFactory = dataFactory(masterFilePaths)
masterData = dataFactory.get_master_json_data()

#load archetype data and component data from SQL database
archetypeDataDB = dataFactory.get_archetypes()
componentMasterData = dataFactory.get_component_masters()

mapData = masterData["tile_master"]

# initialize the display, gamestate, and clock
world = World(mapData, archetypeDataDB, componentMasterData)
pgdisplay = PGDisplay(mapData, world, dataFactory.getTileImages(), displaySettings)
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