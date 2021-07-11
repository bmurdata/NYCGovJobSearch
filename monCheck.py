from os import write
import pymongo
import json
from bson.json_util import dumps
import dbconn as dbsetup

from datetime import datetime,timedelta
def testMongo()-> dict():
    print('Testing connection to Mongo DB')
    searchCollection="jobInfo_Meta"

    try:
        url = dbsetup.monConnection
        client = pymongo.MongoClient(url)
        database = client[dbsetup.db]
        collection = database[searchCollection]
        # "jobNum":{"$regex":str(code),"$options":"-i"}
        result = collection.find({},{"_id":False})
        result = dumps(result)
        print("Processing result")
        print(len(result))
        m=list(result)
        print(len(m))
    except Exception as e:
        result="[{'Error':'Connection failed'"
        print("Error")
        print(e)
    if len(result)==2:
        result="[{'Error':'No Result by that code. Enter numerical value. Example: code=12345'}]"
    return result
def getjob():
    pass

# Test Mongo Connection
# myDict=testMongo()

# print(type(myDict))
# print(len(myDict))
# myDict=json.loads(myDict)

# print(type(myDict))
# print(len(myDict))
# print(myDict[0])
# today=datetime.today().strftime( '%Y-%m-%d')
# print(str(today>myDict[0]['POST UNTIL']))
# print(str(today<myDict[0]['POST UNTIL']))

# # Test if job expired
# for ind,item in enumerate(myDict):
#     if today>item['POST UNTIL']:
#         print("Found an expired: "+item['POST UNTIL'])
#         myDict.pop(ind)
# print(len(myDict))
def clearfromMongo(collecName:str()):
    myLog={"log":"Clearing collection "+collecName,
                "date":str(datetime.now().strftime("%m/%d/%Y")),
                "time":str(datetime.now().strftime("%H:%M:%S")),
                "datetime":str(datetime.now())}
    writeToMongo(myLog,"writeLogs")
    url = dbsetup.monConnection
    client = pymongo.MongoClient(url)
    database = client[dbsetup.db]
    detailcollection = database[collecName]
    detailcollection.delete_many({})

def writeToMongo(jobJson:dict(),collecName:str()):
    url = dbsetup.monConnection
    client = pymongo.MongoClient(url)
    database = client[dbsetup.db]
    collec = database[collecName]
    try:
        collec.insert_one(jobJson)
    except Exception as e:
        myLog={"log":"Failed due to: "+str(e),
                "date":str(datetime.now().strftime("%m/%d/%Y")),
                "time":str(datetime.now().strftime("%H:%M:%S")),
                "datetime":str(datetime.now())}
        writeToMongo(myLog,"writeLogs")
    # print(collec.count_documents({}))
def writeToMongoMany(manyjobJson:dict(),collecName:str()):
    url = dbsetup.monConnection
    client = pymongo.MongoClient(url)
    database = client[dbsetup.db]
    collec = database[collecName]
    try:
        collec.insert_many(manyjobJson)
    except Exception as e:
        myLog={
                "step":"Writing"+len(manyjobJson)+" jobs to "+str(collecName),
                "log":"Failed due to: "+str(e),
                "date":str(datetime.now().strftime("%m/%d/%Y")),
                "time":str(datetime.now().strftime("%H:%M:%S")),
                "datetime":str(datetime.now())}

        writeToMongo(myLog,"writeLogs")
    # print(collec.count_documents({}))
def mongoCompareAgencyandMeta_DB()->list():
    
    print('Testing connection to Mongo DB')
    searchCollection="jobInfo_Meta"
    # Connect to MongoDB
    try:
        url = dbsetup.monConnection
        client = pymongo.MongoClient(url)
        database = client[dbsetup.db]
        detailcollection = database[searchCollection]
        codecollection = database['jobsByCode']
        contentcollection=database['jobInfo_Content']

        details_data= json.loads(dumps(detailcollection.find({},{"_id":False})))
        agency_data=json.loads(dumps(codecollection.find({},{"_id":False})))
        content_data=json.loads(dumps(contentcollection.find({},{"_id":False})))

    except Exception as e:

        myLog={
                "step":"Compare agency to Meta",
                "log":"Failed due to: "+str(e),
                "date":str(datetime.now().strftime("%m/%d/%Y")),
                "time":str(datetime.now().strftime("%H:%M:%S")),
                "datetime":str(datetime.now())}

        writeToMongo(myLog,"writeLogs")
        return result
    

    joblinks=[]
    details_jobNum=[i['jobNum'] for i in details_data]
    agency_jobNum=[i['jobNum'] for i in agency_data]
    content_jobNum=[i['jobNum'] for i in content_data]

    today=datetime.today().strftime( '%Y-%m-%d')
    expired=list()

    # Get all the expired items
    try:

        for ind,item in enumerate(details_data):
            if today>item['POST UNTIL']:
                print("Found an expired: "+item['POST UNTIL'])
                details_data.pop(ind)
                detailcollection.delete_many({'jobNum':item['jobNum']})
                contentcollection.delete_many({'jobNum':item['jobNum']})
                expired.append(item['jobNum'])
            # If the job does not exist in agency data, remove from others
            elif item['jobNum'] not in agency_jobNum:
                detailcollection.delete_many({'jobNum':item['jobNum']})
                contentcollection.delete_many({'jobNum':item['jobNum']})
    except Exception as e:
        print("Error below")
        print(e)
    joblinks=list()
    for job in agency_data:
        jobNum=job['jobNum']
        if jobNum not in details_jobNum:
            joblinks.append([job['link'],job['jobNum']])
    print(len(agency_jobNum))
    return joblinks