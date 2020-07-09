import json
import sys
jsonfile="SECOND-job-by-code.json"
jobcsv="jobsByCode2.csv"

with open(jobcsv,"w") as initial:
    initial.write("jobNum,title,Link,shortCategory,longCategory\n")
with open(jsonfile) as ifile:

    data=json.load(ifile)
    num=0
    with open(jobcsv,"a") as jobs:

        for category in data:
            print("Reading: "+category)
            
            for item in data[category]:
                new_record="\""+item['jobNum'] +"\",\""+item['title']+"\",\""+item['link']+"\","+item['shortcategory']+",\""+item['longcategory'] +"\"\n"
                jobs.write(new_record)
                num += 1
    print(str(num))