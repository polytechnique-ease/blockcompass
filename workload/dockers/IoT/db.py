import __main__ as Simulator

def insertToDB(collection, item):
    Simulator.L.info('insert to db')
    try:
        collection.insert_one(item)
    except Exception as error:
        Simulator.L.error(error)