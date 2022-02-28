import pymongo

from database import Database


class MongoDB(Database):
    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.collection = self.get_database()

    def get_database(self):
        client = pymongo.MongoClient(self.connection_string
                                     , replicaSet='rs0')
        collection = client.benchmarker.resource
        return collection



    def inset_to_database(self,item):
        self.collection.insert_one(item)


