import json

class SettingsManager:
    def __init__(self, settingsPath):
        self.settingsPath = settingsPath
        self.load_settings_data()

    def load_settings_data(self):
        with open(self.settingsPath, "r") as json_file:
            data = json.load(json_file)

        # Import the config data
        self.screenWidth = data["SCREENWIDTH"]
        self.screenHeight = data["SCREENHEIGHT"]
        self.framerate = data["FRAMERATE"]
        self.mapFile = data["MAPFILE"]
        self.entityFile = data["ENTITYFILE"]
        self.componentFile = data["COMPONENTFILE"]
        self.dbFile = data["DBFILE"]

    def get_display_settings(self):
        displayData = {
            "screenWidth": self.screenWidth,
            "screenHeight": self.screenHeight,
            "framerate": self.framerate
        }
        return displayData
    
    def get_db_file(self):
        return self.dbFile
    
    def get_master_file_paths(self):
        return {
            "MAPFILE": self.mapFile,
            "ENTITYFILE": self.entityFile,
            "COMPONENTFILE": self.componentFile,
            "DBFILE": self.dbFile
        }

    