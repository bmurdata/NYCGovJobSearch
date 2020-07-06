import json

jsonfile="test5.json"
jobcsv="jobscsv2.csv"

with open(jobcsv,"w") as initial:
    initial.write("jobNum,Link,shortCategory,longCategory\n")
with open(jsonfile) as ifile:

    data=json.load(ifile)
    num=0
    with open(jobcsv,"a") as jobs:

        for category in data:
            print("Reading: "+category)
            
            for item in data[category]:
                new_record=item['jobNum'] +","+item['link']+","+item['shortcategory']+",\""+item['longcategory'] +"\"\n"
                jobs.write(new_record)
                num += 1
    print(str(num))