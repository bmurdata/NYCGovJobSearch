import json
import sys

def jsonToCSV(jsonfile,jobcsv):

    with open(jobcsv,"w") as initial:
        initial.write("jobNum,title,Link,shortCategory,longCategory\n")
        
    with open(jsonfile) as ifile:
        data=json.load(ifile)
        num=0
        with open(jobcsv,"a") as jobs:

            for category in data:

                for item in data[category]:
                    new_record="\""+item['jobNum'] +"\",\""+item['title']+"\",\""+item['link']+"\","+item['shortcategory']+",\""+item['longcategory'] +"\"\n"
                    jobs.write(new_record)
                    num += 1
        


jsonfile="July13Run-Code.json"
jobcsv="Jul13-Code.csv"

jsonToCSV(jsonfile,jobcsv)

jsonfile="July13Run-Category.json"
jobcsv="Jul13-Cat.csv"
jsonToCSV(jsonfile,jobcsv)
