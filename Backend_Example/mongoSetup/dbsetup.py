# Mongo DB connection- populate dbLocal.py file
import dbLocal
db=dbLocal.db
monConnection=dbLocal.monConnection

import pymongo, json
# Insert JSON files into the collection
def insertToMongo(myFile:str(), myCollection:str(),isCodes:bool()=False):
    with open(myFile) as ifile:
        data=json.load(ifile)

    client = pymongo.MongoClient(monConnection)
    database=client[db]
    collec=database[myCollection]

    if isCodes:
        for cat,item in enumerate(data):
            if len(data[item]) > 0:
                print("Inserting the items")
                print(item)
                collec.insert_many(data[item])
    else:
        print("inserting multiple ")
        collec.insert_many(data)



# Jobs by codes- title, link to apply, etc.
codeCollection="jobsByCode"
codeFiles="mongo.json"

# Meta data on jobs-salary, location, title, etc.
metaCollection="jobInfo_Meta"
metaFile="MULTITHREAD_2021-06-271624821696JSON.json"

# Full job posting details
contentCollection="jobInfo_Content"
contentFile="MULTITHREAD_2021-06-271624821696-Details.json"
insertToMongo(codeFiles,codeCollection,True)
insertToMongo(contentFile,contentCollection)
insertToMongo(metaFile,metaCollection)