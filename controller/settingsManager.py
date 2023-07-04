import json

class SettingsManager:
    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.load_settings_data()
        self.load_master_data()

    def load_settings_data(self):
        with open(self.settings_path, "r") as json_file:
            data = json.load(json_file)

        # Import the config data
        self.SCREENWIDTH = data["SCREENWIDTH"]
        self.SCREENHEIGHT = data["SCREENHEIGHT"]
        self.FRAMERATE = data["FRAMERATE"]
        self.MAPFILE = data["MAPFILE"]
        self.ENTITYFILE = data["ENTITYFILE"]
        self.COMPONENTFILE = data["COMPONENTFILE"]
        self.DBFILE = data["DBFILE"]

    def load_master_data(self):
        # Load data files
        with open(self.MAPFILE, 'r') as f:
            map_data = json.load(f)
        with open(self.ENTITYFILE, 'r') as f:
            archetype_data = json.load(f)
        with open(self.COMPONENTFILE, 'r') as f:
            component_data = json.load(f)

        self.MASTERDATA = {
            "tile_master": map_data,
            "component_master": component_data,
            "archetype_master": archetype_data
        }

    def get_display_settings(self):
        display_data = {
            "SCREENWIDTH": self.SCREENWIDTH,
            "SCREENHEIGHT": self.SCREENHEIGHT,
            "FRAMERATE": self.FRAMERATE
        }
        return display_data
    
    def get_db_file(self):
        return self.DBFILE
    
    def get_master_data(self):
        return self.MASTERDATA
    
    def get_master_file_paths(self):
        return {
            "MAPFILE": self.MAPFILE,
            "ENTITYFILE": self.ENTITYFILE,
            "COMPONENTFILE": self.COMPONENTFILE,
            "DBFILE": self.DBFILE
        }

    