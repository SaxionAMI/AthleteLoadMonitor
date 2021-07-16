import pymongo

# run command: python create_initial_data.py
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["general"]
mycol = mydb["user"]
mycol.insert_one({"email": "admin@admin.com", "password": "$2b$10$T/XOaX62lSDn95L.b/kvq.rxcew8oKL3H0/FuOFpZU79UkWZcEjlm", "role": 0})
