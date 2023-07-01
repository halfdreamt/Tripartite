import sqlite3

#This class will be used to manage the database containing game data
#The database will contain the following tables: tile_data, map_data, component_data, entity_data
#The tile_data table will contain the following columns: id, name, image_data

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
        
    #takes an array of file paths, tile heights, and tile widths, and adds them to the database