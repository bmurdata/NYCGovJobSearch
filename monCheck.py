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
myDict=testMongo()

print(type(myDict))
print(len(myDict))
myDict=json.loads(myDict)

print(type(myDict))
print(len(myDict))
print(myDict[0])
today=datetime.today().strftime( '%Y-%m-%d')
print(str(today>myDict[0]['POST UNTIL']))
print(str(today<myDict[0]['POST UNTIL']))

# Test if job expired
for ind,item in enumerate(myDict):
    if today>item['POST UNTIL']:
        print("Found an expired: "+item['POST UNTIL'])
        myDict.pop(ind)
print(len(myDict))
