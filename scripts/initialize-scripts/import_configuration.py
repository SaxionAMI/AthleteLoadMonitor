import sys
import json
import pymongo

# run command: python import_configuration.py <path/file_name.json> <database_name>
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[sys.argv[2]]
mycol = mydb["file_import_configuration"]
with open(f'{sys.argv[1]}') as f:
    data = json.load(f)
    mycol.insert_many(data)
    print("success")
