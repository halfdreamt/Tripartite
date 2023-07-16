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
        self.entityFile = data["ENTITYFILE"]
        self.componentFile = data["COMPONENTFILE"]
        self.dbFile = data["DBFILE"]
        self.effectFile = data["EFFECTFILE"]
        self.abilityFile = data["ABILITYFILE"]
        self.mapMaster = data["MAPMASTER"]
        self.tileMaster = data["TILEMASTER"]
        self.defaultMode = data["DEFAULT_MODE"]

    def get_display_settings(self):
        displayData = {
            "screenWidth": self.screenWidth,
            "screenHeight": self.screenHeight,
            "framerate": self.framerate,
            "defaultMode": self.defaultMode
        }
        return displayData
    
    def get_db_file(self):
        return self.dbFile
    
    def get_master_file_paths(self):
        return {
            "ENTITYFILE": self.entityFile,
            "COMPONENTFILE": self.componentFile,
            "DBFILE": self.dbFile,
            "EFFECTFILE": self.effectFile,
            "ABILITYFILE": self.abilityFile,
            "MAPMASTER": self.mapMaster,
            "TILEMASTER": self.tileMaster
        }
    
    def get_frame_rate(self):
        return self.framerate

    