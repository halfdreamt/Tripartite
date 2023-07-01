import pygame
import json
from model.world import World
from view.PGDisplay import PGDisplay
from data.dataFactory import dataFactory

# Read the config file
file_path = "rec/config.json"
with open(file_path, "r") as json_file:
    data = json.load(json_file)

# Import the config data
SCREENWIDTH = data["SCREENWIDTH"]
SCREENHEIGHT = data["SCREENHEIGHT"]
FRAMERATE = data["FRAMERATE"]
MAPFILE = data["MAPFILE"]
ENTITYFILE = data["ENTITYFILE"]
COMPONENTFILE = data["COMPONENTFILE"]

# Load data files
with open(MAPFILE, 'r') as f:
    map_data = json.load(f)
with open(ENTITYFILE, 'r') as f:
    entity_data = json.load(f)
with open(COMPONENTFILE, 'r') as f:
    component_data = json.load(f)

# Initialize pygame, data factory, world, display, and clock
pygame.init()
dataFactory = dataFactory()
world = World(map_data, entity_data, component_data)
pgdisplay = PGDisplay(map_data, pygame, world, dataFactory, SCREENWIDTH, SCREENHEIGHT)
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
    clock.tick(FRAMERATE)

    # Redraw screen with new camera position/zoom level
    pgdisplay.draw_screen()  

pygame.quit()