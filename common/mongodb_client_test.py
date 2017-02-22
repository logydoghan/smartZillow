import mongodb_client

db = mongodb_client.getDB()

db.test.insert({"test123" : "123"})

print list(db.test.find({"test123": "123"}))

