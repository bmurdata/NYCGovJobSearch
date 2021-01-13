
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
import os
import scraperModule
# Where files should be placed
dir_path = os.path.dirname(os.path.realpath(__file__))+"/output/"
defaultfname=str(date.today())+str(time.time()).split(".")[0]
parser = argparse.ArgumentParser(description="Multithread implementation of the job link scraper.")
parser.add_argument("--joblinkfile", help="JSON file to get links from.")
parser.add_argument("-pc","--threadnum", type=int,help="How many parallel processes to spawn. Default is cpu count.",default=cpu_count())
parser.add_argument("-ofile","--outfile",help="Output file names",default=defaultfname)
args = parser.parse_args()
# print(sys.argv[1:])
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
    
# Write JSON to files
def write_json(jobJson,job_detail,job_json,job_details_json):
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
        traceback.print_exc()

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

# Scrape the joblinks. Designed to work with multithreading
def scrape_multi_arr(jobllinks):
    try:
        print("This thread has: "+str(len(jobllinks))+" items to run.")
        start__runtime=time.time()
        browser=scraperModule.fireFox_setup()
        print("Creating session with site")
        # browser.get("https://a127-jobs.nyc.gov/")

        # time.sleep(1)
        print("Getting the Job Link")
        jobJson=[]
        job_detail=[]
        numclicks=0
        for link in jobllinks:
            browser.get(link[0])
            # time.sleep(1)
            numclicks +=1
            # Get the job meta data- pay, title classification, etc Values[0] has agency name, Labels[2] has first value
            try:
                jobMeta_values=browser.find_elements_by_css_selector("div.ps_box-group.psc_layout.psc_column-2 .ps_box-value")
                jobMeta_labels=browser.find_elements_by_css_selector("div.ps_box-group.psc_layout.psc_column-2 .ps_box-label")
                jobMeta={jobMeta_labels[i].get_attribute('innerText'):jobMeta_values[i].get_attribute('innerText') for i in range(2,len(jobMeta_labels))}
            except Exception as e:
                print("Failed for unknown reasons")
                jobMeta_values=[]
                jobMeta_labels=[]
                jobMeta={}
            try:
                agency_title=jobMeta_values[0].get_attribute('innerText')
            except:
                print("No agency name found")
                agency_title="Not Found"
            try:
                jobLabels=browser.find_elements_by_css_selector("div.ps_box-group.hrs_cg_groupbox_field_label_back .ps_header-group")
                jobContent=browser.find_elements_by_css_selector("div.ps_box-group.hrs_cg_groupbox_field_label_back .ps_content-group")
                # print(jobContent[0].get_attribute('innerText'))
                print("There are some number of labels. That number is "+str(len(jobLabels)))
                print("There are some number of Content. That number is "+str(len(jobContent)))
                jobDescrip={jobLabels[i].get_attribute('innerText'):jobContent[i].get_attribute('innerText') for i in range(len(jobLabels))}
                print("Sems to work! Dictionary of length: "+str(len(jobDescrip)))
            except Exception as e:
                print(e)
                print("Nothing to add")
                
            jobDescrip['jobNum']=link[1]
            jobDescrip['jobLink']=link[0]
            
            jobDescription = {label: jobDescrip.get(label,"Not listed") for label in myLabels.details_order}
            #jobDescription['jobNum']=link[1]
            job_detail.append(jobDescription)
            current_job={'HiringAgency':agency_title,'jobLink':link[0],'jobNum':link[1]}
            # Write to the cmd line. Comment out in production
            if len(jobMeta)>0:
                sys.stdout.write('\r')
                sys.stdout.flush()
                sys.stdout.write("On click: "+str(numclicks))
                sys.stdout.flush()
            if len(jobMeta)==0:
                for i in myLabels.labels:
                    if i=="Job ID" or i=="# of Positions":
                        current_job[i]="0"
                    elif i=="POSTING DATE" or i=="POST UNTIL":
                        current_job[i]="3020-12-12"
                    else:
                        current_job[i]="Not Found"
            else:
                for i in jobMeta.keys():
                    r=re.compile(".[0-9]/.[0-9]/.*")
                    if r.match(jobMeta[i]):
                        current_job[i] = datetime.strptime(jobMeta[i], "%m/%d/%Y").strftime("%Y-%m-%d") if jobMeta[i] and jobMeta[i] is not "\u00a0" else "Not Listed"
                    elif jobMeta[i]=="Until Filled":
                        current_job[i]="3020-01-01"
                    else:
                        current_job[i] =jobMeta[i] if jobMeta[i] and jobMeta[i] is not "\u00a0" else "Not Listed"
                        
            jobJson.append(current_job)

    except Exception as e:
        print("Not really sure why things fell apart. Keep trying ")
        print(e)
        traceback.print_exc()

        browser.quit()
    browser.quit()
    my_runtime=round(time.time()-start__runtime,2)

    return jobJson,job_detail,my_runtime

if __name__== "__main__":

    start=time.time()
    jobFile=args.joblinkfile
    numprocesses=args.threadnum
    print("You will have: "+str(numprocesses)+" parallel threads.")
    base=args.outfile
    #run_multi_scrape(start,jobFile,base)
    start_time=time.time()
    baseFile=dir_path+"MULTITHREAD_"+base
    jsonout=baseFile+"JSON.json"
    csvout=baseFile+"CSV.csv"

    #jobFile="TEST_2.json"
    jobFile="TODAY_test4.json"
    joblinks_raw=pulljoblinks(jobFile)
    print(str(len(joblinks_raw)))
    joblinks=numpy.array_split(numpy.array(joblinks_raw),numprocesses)

    job_details_csv=baseFile+"-Details.csv"
    job_details_json=baseFile+"-Details.json"
    num_workers = int(numprocesses)
    with Pool(num_workers) as p:
        results_tuple=p.map(scrape_multi_arr,joblinks,1)
    jobs=[]
    details=[]
    alltimes=[]
    for results in results_tuple:
        jobs=jobs+results[0]
        details=details+results[1]
        alltimes.append(results[2])
    try:
        write_json(jobs,details,jsonout,job_details_json)
    except Exception as e:
        print("Failed due to "+str(e))
        traceback.print_exc()
    
    start__runtime=time.time()
    writeJobtoCsv(jsonout,csvout)
    writeJobtoCsv(job_details_json,job_details_csv)
    my_runtime=round(time.time()-start__runtime,2)
    print("Time to execute writing to file was "+str(my_runtime))
    print("------")
    for scrape_runtime in alltimes:
        print("Time to execute search:{time}".format(time=scrape_runtime))

    final_time=round(time.time()-start_time,2)
    print("Final time to execute:{time}".format(time=final_time))
    print("------")