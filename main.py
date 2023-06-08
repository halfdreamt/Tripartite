import pygame
import json
from model.world import World
from view.PGDisplay import PGDisplay


# Initialize pygame
pygame.init()

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

# Load map data
with open(MAPFILE, 'r') as f:
    map_data = json.load(f)

# Load entity data
with open(ENTITYFILE, 'r') as f:
    entity_data = json.load(f)

# Load component data
with open(COMPONENTFILE, 'r') as f:
    component_data = json.load(f)

# Initialize world
world = World(map_data, entity_data, component_data)

# Initialize display
pgdisplay = PGDisplay(map_data, pygame, world, SCREENWIDTH, SCREENHEIGHT)


# Initialize clock for FPS control
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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