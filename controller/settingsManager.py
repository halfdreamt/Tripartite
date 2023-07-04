import json

class SettingsManager:
    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.load_settings_data()

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

    def get_display_settings(self):
        display_data = {
            "SCREENWIDTH": self.SCREENWIDTH,
            "SCREENHEIGHT": self.SCREENHEIGHT,
            "FRAMERATE": self.FRAMERATE
        }
        return display_data
    
    def get_db_file(self):
        return self.DBFILE
    
    def get_master_file_paths(self):
        return {
            "MAPFILE": self.MAPFILE,
            "ENTITYFILE": self.ENTITYFILE,
            "COMPONENTFILE": self.COMPONENTFILE,
            "DBFILE": self.DBFILE
        }

    