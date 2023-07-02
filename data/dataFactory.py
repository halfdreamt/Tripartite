import sqlite3
import xml.etree.ElementTree as ET
import os
import pygame
import io
from PIL import Image

#This class will be used to manage the database containing game data
#The database will contain the following tables: tile_data, map_data, component_data, entity_data
#The tile_data table will contain the following columns: id, name, image_data
#The coordinates table will contain the following columns: id (Primary ID), x (unqiue), y (unique), map_id (foreign key)
#The map_data table will contain the following columns: id (Primary ID), name, width, height
#The entity_data table will contain the following columns: id (Primary ID)
#The component_data table will contain the following columns: id (Primary ID), entity_id (foreign key), name, data

class dataFactory:
    #initializes the database connection
    def __init__(self):
        self.conn = sqlite3.connect('data/gameData.sqlite')
        self.cursor = self.conn.cursor()
        self.createTables()

    #creates the tables in the database, if they don't already exist
    def createTables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tile_data
                     (id INTEGER PRIMARY KEY, name TEXT, image_data BLOB)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS coordinates
                        (id INTEGER PRIMARY KEY, x INTEGER, y INTEGER, map_id INTEGER, FOREIGN KEY(map_id) REFERENCES map_data(id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS map_data
                        (id INTEGER PRIMARY KEY, name TEXT, width INTEGER, height INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS entity_data
                        (id INTEGER PRIMARY KEY)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS component_data
                        (id INTEGER PRIMARY KEY, entity_id INTEGER, name TEXT, data TEXT, FOREIGN KEY(entity_id) REFERENCES entity_data(id))''')
        
    #Create a new map in the database
    def createMap(self, name, width, height):
        self.cursor.execute("INSERT INTO map_data (name, width, height) VALUES (?, ?, ?)", (name, width, height))
        self.conn.commit()
        map_id = self.cursor.lastrowid
        #Generate coordinates for the map
        for x in range(width):
            for y in range(height):
                self.cursor.execute("INSERT INTO coordinates (x, y, map_id) VALUES (?, ?, ?)", (x, y, map_id))
        self.conn.commit()

    #Take blob images data from database and convert it into an array of usable images
    def getTileImages(self):
        self.cursor.execute("SELECT image_data FROM tile_data")
        images = []
        for row in self.cursor:
            images.append(pygame.image.load(io.BytesIO(row[0])))
        return images
        
    #takes the map_data object and uses it to insert individual tile images into the tile_data table
    def insertTileData(self, map_data):
        tilewidth, tileheight = map_data['tilewidth'], map_data['tileheight']

        # Load tilesets
        for tileset in map_data['tilesets']:
            tsx_path = "./rec/mapfiles/" + tileset['source']
            tsx_root = ET.parse(tsx_path).getroot()
            image_path = os.path.join(os.path.dirname(tsx_path), tsx_root.find('image').get('source'))
            full_image = Image.open(image_path)

            tilesetwidth, tilesetheight = full_image.size[0] // tilewidth, full_image.size[1] // tileheight

            # Split the tileset into individual tiles
            for tile_y in range(tilesetheight):
                for tile_x in range(tilesetwidth):
                    # Extract individual tile
                    box = (tile_x*tilewidth, tile_y*tileheight, (tile_x+1)*tilewidth, (tile_y+1)*tileheight)
                    tile_image = full_image.crop(box)

                    # Convert the Pillow Image object to bytes
                    byte_arr = io.BytesIO()
                    tile_image.save(byte_arr, format='PNG')
                    image_bytes = byte_arr.getvalue()

                    name = f'{tileset["source"].split("/")[-1].split(".")[0]}_{tile_y}_{tile_x}'
                    self.cursor.execute("INSERT INTO tile_data (name, image_data) VALUES (?, ?)", (name, image_bytes))
                    self.conn.commit()

    #returns the image data for the tile with the given id
    def getTileImage(self, tile_id):
        self.cursor.execute("SELECT image_data FROM tile_data WHERE id = ?", (tile_id,))
        return self.cursor.fetchone()[0]
    
    #returns all of the tile data from the tile_data table
    def getTileData(self):
        self.cursor.execute("SELECT * FROM tile_data")
        return self.cursor.fetchall()