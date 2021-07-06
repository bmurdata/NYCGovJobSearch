# Write JSON and CSV Files from JSON/ dict
import json, csv, numpy, sys

# Writes Json and CSV files for job info
class myLabels:
    labels=[
        "Job ID",
        "Business Title",
        "Civil Service Title",
        "Title Classification",
        "Job Category",
        "Career Level",
        "Work Location",
        "Division/Work Unit",
        "# of Positions",
        "Title Code No",
        "Level",
        "Proposed Salary Range",
        "POSTING DATE",
        "POST UNTIL"]

    details_order=['Job Description',
        'Minimum Qual Requirements',
        'Preferred Skills',
        'Additional Information',
        'To Apply',
        'Hours/Shift',
        'Work Location',
        'Residency Requirement',
        'Recruitment Contact',
        'jobNum']
def writeJobBasics(jsondata,jsonFile,csvFile):
    
    if jsondata:
        # Write JSON to the JSON file
        try:
            with open(jsonFile, "w") as myfile:
                print("Preparing to write file ")
                json.dump(jsondata,myfile,indent=4)
        
        except Exception as e:
            print("Failed to write to file")
            print(str(e))

        # Write JSON data to CSV

        with open(csvFile,"w",newline='',encoding="utf-8") as initial:
            initial.write("JobID,Title,Link,shortCategory,longCategory,Department,Location,Agency,Posted Date\n")
            
        with open(csvFile,"a",newline='',encoding="utf-8") as jobs:

            for category in jsondata:
                for item in jsondata[category]:
                    new_record="\""+item['jobNum'] +"\",\""+item['title']+"\",\""+item['link']+"\",\""+item['shortcategory']+"\",\""+item['longcategory'] +"\",\""+item['Department']+"\",\""+item['Location']+"\",\""+item['Agency']+"\",\""+item['Posted_Date']+"\"\n"
                    jobs.write(new_record)

# Write JSON to files
def write_jsonDetailsandInfo(jobJson,job_detail,job_json,job_details_json):
    try:
        with open(job_json, "w") as jsout:
                json.dump(jobJson,jsout,indent=4)  
        sorted_job_details=[]
        for job in job_detail:
            for detail in myLabels.details_order:
                if not detail in job:
                    job[detail]="Not Found"
            #Sort the dictionary by keys
            
            sorted_job=dict(sorted(job.items()))
            sorted_job_details.append(sorted_job)
        
        with open(job_details_json, "w") as detailsout:
            json.dump(sorted_job_details,detailsout,indent=4)
        
    except Exception as e:
        print(e)

# Write Job JSON file to CSV
def writeJobtoCsv(jsonfile,jobcsv):
    try:
        with open(jsonfile) as ifile:
            data=json.load(ifile)
            maxkeys=0
            keydict=[]
            for jobkeys in data:
                if maxkeys< len(jobkeys.keys()):
                    maxkeys=len(jobkeys.keys())
                    keydict=jobkeys.keys()
            if len(keydict)==0:
                print("Error occured, no keys in dict.")
                sys.exit(1)

            header=keydict#myLabels.labels#data[0].keys()
         
            with open(jobcsv,"w",newline='',encoding="utf-8") as ofile:
                csv_write=csv.writer(ofile)
                csv_write.writerow(header)
                for job in data:
                    csv_write.writerow(job.values())
    except Exception as e:
        print(e)
        # traceback.print_exc()
        # traceback.print_exception()