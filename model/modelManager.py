from data.dataFactory import dataFactory
from model.world import World

class modelManager:
    def __init__(self, settings_manager):

        self.settings_manager = settings_manager

        # Initialize data factory with the master file paths (inserts the master json data into the DB if needed)
        self.data_factory = dataFactory(settings_manager.get_master_file_paths())

        # Initialize the world with master data (primarily model data)
        self.world = World(self.data_factory.get_master_data())