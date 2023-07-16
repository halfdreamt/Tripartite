import sqlite3
import xml.etree.ElementTree as ET
import os
import pygame
import json
import io
from PIL import Image

#This class will be used to manage the database containing game data
#The database will contain the following tables: tile_master, map_data, component_data, entity_data
#The tile_master table will contain the following columns: id, name, image_data
#The coordinate_data table will contain the following columns: id (Primary ID), x (unqiue), y (unique), map_id (foreign key)
#The map_data table will contain the following columns: id (Primary ID), name, width, height
#The entity_data table will contain the following columns: id (Primary ID)
#The component_data table will contain the following columns: id (Primary ID), entity_id (foreign key), component_ID (foreign key from component_master), name, data
#The component_master table will contain the following columns: id (Primary ID), name, data
#The archetype_master table will contain the following columns: id (Primary ID), name, components
#The map_master table will contain the following columns: id (Primary ID), name, width, height, ground, tilesize, collision, sprites
#The effect_master table will contain the following columns: id (Primary ID), name, description, data
#The ability_master table will contain the following columns: id (Primary ID), name, type, description, effects, cost

class dataFactory:
    #initializes the database connection
    def __init__(self, master_file_paths):
        self.master_file_paths = master_file_paths
        self.conn = sqlite3.connect(master_file_paths['DBFILE'])
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.load_master_json_data()

    #creates the tables in the database, if they don't already exist
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tile_master
                     (id INTEGER PRIMARY KEY, name TEXT, image_data BLOB)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS coordinate_data
                        (id INTEGER PRIMARY KEY, x INTEGER, y INTEGER, map_id INTEGER, FOREIGN KEY(map_id) REFERENCES map_data(id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS map_data
                        (id INTEGER PRIMARY KEY, name TEXT, width INTEGER, height INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS entity_data
                        (id INTEGER PRIMARY KEY)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS component_data
                        (id INTEGER PRIMARY KEY, entity_id INTEGER, component_id INTEGER, name TEXT, data TEXT, FOREIGN KEY(entity_id) REFERENCES entity_data(id), FOREIGN KEY(component_id) REFERENCES component_master(id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS component_master
                        (id INTEGER PRIMARY KEY, name TEXT, data TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS archetype_master
                        (id INTEGER PRIMARY KEY, name TEXT, components TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS map_master
                        (id INTEGER PRIMARY KEY, name TEXT, width INTEGER, height INTEGER, ground TEXT, tilesize INTEGER, collision TEXT, sprites TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS effect_master
                        (id INTEGER PRIMARY KEY, name TEXT, description TEXT, data TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ability_master
                        (id INTEGER PRIMARY KEY, name TEXT, type TEXT, description TEXT, effects TEXT, cost INTEGER)''')
        
    #Create a new map in the database
    def create_map(self, name, width, height):
        self.cursor.execute("INSERT INTO map_data (name, width, height) VALUES (?, ?, ?)", (name, width, height))
        self.conn.commit()
        map_id = self.cursor.lastrowid
        #Generate coordinate_data for the map
        for x in range(width):
            for y in range(height):
                self.cursor.execute("INSERT INTO coordinate_data (x, y, map_id) VALUES (?, ?, ?)", (x, y, map_id))
        self.conn.commit()

    #Take blob images data from database and convert it into an array of usable images
    def get_tile_images(self):
        self.cursor.execute("SELECT image_data FROM tile_master")
        images = []
        for row in self.cursor:
            images.append(pygame.image.load(io.BytesIO(row[0])))
        return images
    
    #takes component master data and inserts it into the component_master table
    def insert_component_master_data(self, component_master_data):
        for component in component_master_data['components']:
            name = component['name']
            json_data = json.dumps(component['data'])
            self.cursor.execute("INSERT INTO component_master (name, data) VALUES (?, ?)", (name, json_data))
        self.conn.commit()

    def insert_archetype_master_data(self, archetype_master_data):
        for archetype in archetype_master_data['archetypes']:
            name = archetype['name']
            json_data = json.dumps(archetype['components'])
            self.cursor.execute("INSERT INTO archetype_master (name, components) VALUES (?, ?)", (name, json_data))
        self.conn.commit()

    def insert_effect_master_data(self, effect_master_data):
        for effect in effect_master_data['effects']:
            name = effect['name']
            description = effect['description']
            json_data = json.dumps(effect['data'])
            self.cursor.execute("INSERT INTO effect_master (name, description, data) VALUES (?, ?, ?)", (name, description, json_data))
        self.conn.commit()

    def insert_ability_master_data(self, ability_master_data):
        for ability in ability_master_data['abilities']:
            name = ability['name']
            type = ability['type']
            description = ability['description']
            effects = json.dumps(ability['effects'])
            if 'cost' in ability:
                cost = json.dumps(ability['cost'])
            else:
                cost = -1
            self.cursor.execute("INSERT INTO ability_master (name, type, description, effects, cost) VALUES (?, ?, ?, ?, ?)", (name, type, description, effects, cost))
        self.conn.commit()

    def insert_map_master_data(self, map_master_data):
        name = map_master_data['name']
        width = map_master_data['width']
        height = map_master_data['height']
        tilesize = map_master_data['tilesize']
        ground = map_master_data['ground']
        collision = map_master_data['collision']
        entities = map_master_data['sprites']
        self.cursor.execute("INSERT INTO map_master (name, width, height, ground, tilesize, collision, sprites) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, width, height, ground, tilesize, collision, entities))
        self.save_table_to_file("map_master", "./rec/mapfiles/map_master.json")
        self.conn.commit()
        
    #takes the map_data object and uses it to insert individual tile images into the tile_master table
    def insert_tile_master_data(self, map_data):
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
                    self.cursor.execute("INSERT INTO tile_master (name, image_data) VALUES (?, ?)", (name, image_bytes))
                    self.conn.commit()

    #returns the image data for the tile with the given id
    def get_tile_image(self, tile_id):
        self.cursor.execute("SELECT image_data FROM tile_master WHERE id = ?", (tile_id,))
        return self.cursor.fetchone()[0]
    
    #Inserts master data if the target table is empty
    def insert_master_json_data(self, master_data):
        targetTables = master_data.keys()
        for table in targetTables:
            self.cursor.execute("SELECT * FROM " + table)
            if len(self.cursor.fetchall()) == 0:
                if table == "tile_master":
                    self.insert_tile_master_data(master_data[table])
                elif table == "component_master":
                    self.insert_component_master_data(master_data[table])
                elif table == "archetype_master":
                    self.insert_archetype_master_data(master_data[table])
                elif table == "map_master":
                    self.insert_map_master_data(master_data[table])
                elif table == "effect_master":
                    self.insert_effect_master_data(master_data[table])
                elif table == "ability_master":
                    self.insert_ability_master_data(master_data[table])

    def get_archetypes(self):
        self.cursor.execute("SELECT * FROM archetype_master")
        archetypes = []
        for row in self.cursor:
            archetypes.append({'name': row[1], 'components': json.loads(row[2])})
        return archetypes
    
    def get_component_masters(self):
        self.cursor.execute("SELECT * FROM component_master")
        components = []
        for row in self.cursor:
            components.append({'name': row[1], 'data': json.loads(row[2])})
        return components
    
    def get_map_master(self):
        self.cursor.execute("SELECT * FROM map_master")
        map_data = {}
        layers = {}
        for row in self.cursor:
            map_data['name'] = row[1]
            map_data['width'] = row[2]
            map_data['height'] = row[3]
            layers['ground'] = json.loads(row[4])
            map_data['tilesize'] = row[5]
            layers['collision'] = json.loads(row[6])
            layers['sprites'] = json.loads(row[7])
            map_data['layers'] = [
                {
                    "name": "Tile Layer 1",
                    "data": layers['ground']
                }, {
                    "name": "collision",
                    "data": layers['collision']
                }, {
                    "name": "sprites",
                    "data": layers['sprites']
                }
            ]
        return map_data
    
    def load_master_json_data(self):
        # Load data files
        with open(self.master_file_paths['MAPFILE'], 'r') as f:
            map_data = json.load(f)
        with open(self.master_file_paths['ENTITYFILE'], 'r') as f:
            archetype_data = json.load(f)
        with open(self.master_file_paths['COMPONENTFILE'], 'r') as f:
            component_data = json.load(f)
        with open(self.master_file_paths['EFFECTFILE'], 'r') as f:
            effect_data = json.load(f)
        with open(self.master_file_paths['ABILITYFILE'], 'r') as f:
            ability_data = json.load(f)
        with open(self.master_file_paths['MAPMASTER'], 'r') as f:
            map_master = json.load(f)

        self.master_json_data = {
            "tile_master": map_data,
            "component_master": component_data,
            "archetype_master": archetype_data,
            "map_master": map_master,
            "effect_master": effect_data,
            "ability_master": ability_data,
        }

        self.insert_master_json_data(self.master_json_data)

    def get_master_json_data(self):
        return self.master_json_data
    
    def get_master_data(self):
        component_master_data = self.get_component_masters()
        archetype_master_data = self.get_archetypes()
        map_master_data = self.get_map_master()
        return {
            "component_master": component_master_data,
            "archetype_master": archetype_master_data,
            "map_master": map_master_data,

        }
    
    def save_table_to_file(self, table_name, file_path):
        self.cursor.execute("SELECT * FROM " + table_name)
        column_names = [description[0] for description in self.cursor.description]
        data = self.cursor.fetchall()
        data_with_columns = [dict(zip(column_names, row)) for row in data]
        if len(data_with_columns) == 1:
            data_with_columns = data_with_columns[0]
        with open(file_path, 'w') as f:
            json.dump(data_with_columns, f)

