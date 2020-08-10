import scraperModule
import traceback
import csv
#Location of Geck Driver
import time
import json
from multiprocessing import Pool
from multiprocessing import cpu_count
import argparse
import sys
from datetime import datetime
from datetime import date
import numpy
import argparse
import re
parser = argparse.ArgumentParser(description="Multithread implementation of the job link scraper.")
parser.add_argument("--joblinkfile", help="JSON file to get links from.")

args = parser.parse_args()

class myLabels:

    labels=["Job_ID",
    "Num_of_Positions",
    "Business_Title",
    "Title_Code_No",
    "Level",
    "Civil_Service_Title",
    "Title_Classification",
    "Job_Category",
    "Proposed_Salary_Range",
    "Career_Level",
    "Work_Location",
    "Division_Work_Unit",
    "Posted",
    "Post_Until"]
def find_job_details(jobpage):
    try:
        job_details={}
        job_details_array=jobpage.find_elements_by_xpath("//span[starts-with(@id,'HRS_SCH_PSTDSC_DESCR')]")
        job_descriptor=job_details_array[::2]
        job_info=job_details_array[1::2]
        for i in range(0,len(job_descriptor)):
            job_details[job_descriptor[i].get_attribute('innerText')]=job_info[i].get_attribute('innerText')
    except:
        job_details={"none":"none"}
        print("Failed")
    return job_details
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
        traceback.print_exc()
        traceback.print_exception()
# Scrape the joblinks
def scrape_multi_arr(jobllinks):
    try:
        print("This thread has: "+str(len(jobllinks))+" items to run.")
        start__runtime=time.time()
        browser=scraperModule.fireFox_setup()
        print("Creating session with site")
        browser.get("https://a127-jobs.nyc.gov/")

        time.sleep(1)
        print("Getting the Job Link")
        jobJson=[]
        job_detail=[]
        numclicks=0
        for link in jobllinks:
            browser.get(link[0])
            numclicks +=1
            dispData=browser.find_elements_by_class_name("PSEDITBOX_DISPONLY")
            try:
                agency_title=browser.find_element_by_id("HRS_BS_UNT_HR_I_DESCR").get_attribute('innerText')
            except:
                agency_title="Not Found"

            dispData.pop(0)
            details=find_job_details(browser)
            details['jobNum']=link[1]
            job_detail.append(details)
            current_job={'HiringAgency':agency_title,'jobLink':link[0],'jobNum':link[1]}
            if len(dispData)>0:
                sys.stdout.write('\r')
                sys.stdout.flush()
                sys.stdout.write("On click: "+str(numclicks))
                sys.stdout.flush()
            for i in range(0,len(dispData)):
                r=re.compile(".[0-9]/.[0-9]/.*")
                
                if r.match(dispData[i].get_attribute('innerText')):
                    print("Date found")
                    current_job[myLabels.labels[i]] = datetime.strptime(dispData[i].get_attribute('innerText'), "%m/%d/%Y").strftime("%Y-%m-%d") if dispData[i].get_attribute('innerText') and dispData[i].get_attribute('innerText') is not "\u00a0" else "Not Listed"
                elif dispData[i].get_attribute('innerText')=="Until Filled":
                    current_job[myLabels.labels[i]]="3020-01-01"

                else:
                    current_job[myLabels.labels[i]] =dispData[i].get_attribute('innerText') if dispData[i].get_attribute('innerText') and dispData[i].get_attribute('innerText') is not "\u00a0" else "Not Listed"
                    
            jobJson.append(current_job)

    except Exception as e:
        print(" ")
        print(e)
        traceback.print_exc()

        browser.quit()
    browser.quit()
    my_runtime=round(time.time()-start__runtime,2)

    return jobJson,job_detail,my_runtime

def test_file_json_write(jobJson,job_detail,job_json,job_details_json):
    try:
        with open(job_json, "w") as jsout:
                json.dump(jobJson,jsout,indent=4)

        details_order=["Job Description",
        "Minimum Qual Requirements",
        "Preferred Skills",
        "Additional Information",
        "To Apply",
        "Hours/Shift",
        "Work Location",
        "Residency Requirement",
        "Recruitment Contact",
        "jobNum"]
        sorted_job_details=[]
        for job in job_detail:
            for detail in details_order:
                if not detail in job:
                    job[detail]="Not Found"
            #Sort the dictionary by keys
            
            sorted_job=dict(sorted(job.items()))
            sorted_job_details.append(sorted_job)
        
        with open(job_details_json, "w") as detailsout:
            json.dump(sorted_job_details,detailsout,indent=4)
        
    except Exception as e:
        traceback.print_exc()

# Pull jobs into JSON file.
def pulljoblinks(jobfile):
    joblinks=[]

    with open(jobfile,"r") as datafile:
        data=json.load(datafile)
        for category in data:
            for item in data[category]:
                joblinks.append([item['link'],item['jobNum']])

    print("There are :"+str(len(joblinks)))
    return joblinks

# Run in jobCheck when multithread is set
def run_multi_scrape(program_start_runtime,jobFile,basefilename):

    baseFile="MULTITHREAD_"+basefilename
    jsonout=baseFile+"JSON.json"
    csvout=baseFile+"CSV.csv"

    joblinks_raw=pulljoblinks(jobFile)
    print(str(len(joblinks_raw)))
    joblinks=numpy.array_split(numpy.array(joblinks_raw),10)

    job_details_csv=baseFile+"-Details.csv"
    job_details_json=baseFile+"-Details.json"
    try:
        with Pool(10) as p:
            results_tuple=p.map(scrape_multi_arr,joblinks,1)
    except:
        traceback.print_exc
        sys.exit(1)
    jobs=[]
    details=[]
    alltimes=[]
    for results in results_tuple:
        jobs=jobs+results[0]
        details=details+results[1]
        alltimes.append(results[2])
    try:
        test_file_json_write(jobs,details,jsonout,job_details_json)
    except Exception as e:
        print("Failed due to "+str(e))
        traceback.print_exc()

    writeJobtoCsv(jsonout,csvout)
    writeJobtoCsv(job_details_json,job_details_csv)
    
    print("------")
    for scrape_runtime in alltimes:
        print("Time to execute search:{time}".format(time=scrape_runtime))

    final_time=round(time.time()-program_start_runtime,2)
    print("Final time to execute:{time}".format(time=final_time))
    print("------")

if __name__== "__main__":

    start=time.time()
    jobFile=args.joblinkfile
    base=str(date.today())+str(time.time()).split(".")[0]
    #run_multi_scrape(start,jobFile,base)
    start_time=time.time()
    baseFile="MULTITHREAD_"+str(date.today())+str(time.time()).split(".")[0]
    jsonout=baseFile+"JSON.json"
    csvout=baseFile+"CSV.csv"

    #jobFile="TEST_2.json"
    joblinks_raw=pulljoblinks(jobFile)
    print(str(len(joblinks_raw)))
    joblinks=numpy.array_split(numpy.array(joblinks_raw),10)

    job_details_csv=baseFile+"-Details.csv"
    job_details_json=baseFile+"-Details.json"
    num_workers = cpu_count()
    with Pool(10) as p:
        results_tuple=p.map(scrape_multi_arr,joblinks,1)
    jobs=[]
    details=[]
    alltimes=[]
    for results in results_tuple:
        jobs=jobs+results[0]
        details=details+results[1]
        alltimes.append(results[2])
    try:
        test_file_json_write(jobs,details,jsonout,job_details_json)
    except Exception as e:
        print("Failed due to "+str(e))
        traceback.print_exc()

    writeJobtoCsv(jsonout,csvout)
    writeJobtoCsv(job_details_json,job_details_csv)
    
    print("------")
    for scrape_runtime in alltimes:
        print("Time to execute search:{time}".format(time=scrape_runtime))

    final_time=round(time.time()-start_time,2)
    print("Final time to execute:{time}".format(time=final_time))
    print("------")