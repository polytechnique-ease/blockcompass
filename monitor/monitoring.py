from abc import ABC, abstractmethod


class Monitoring(ABC):
    def __init__(self, database):
        self.database = database

    def database_insertion(self, data):
        self.database.inset_to_database(data)



    @abstractmethod
    def get_measurements(self):
        pass
