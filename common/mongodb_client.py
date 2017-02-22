from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
DB_NAME = 'real_estate_smart_view'

client = MongoClient('%s:%s' % (MONGO_DB_HOST, MONGO_DB_PORT))

def getDB(db=DB_NAME):
    db = client[db]
    return db

