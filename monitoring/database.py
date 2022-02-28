from abc import ABC, abstractmethod


class Database(ABC):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    @abstractmethod
    def get_database(self):
        pass

    @abstractmethod
    def inset_to_database(self,item):
        pass


