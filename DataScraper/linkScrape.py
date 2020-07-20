import scraperModule
import traceback
import csv
#Location of Geck Driver
import time
import json

import argparse
import sys
from datetime import date
test_joblink=[
"https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=376405&PostingSeq=1&",
"https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=441207&PostingSeq=1&",
"https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=432041&PostingSeq=1&"]

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
            header=data[0].keys()
         
            with open(jobcsv,"w",newline='') as ofile:
                csv_write=csv.writer(ofile)
                csv_write.writerow(header)
                for job in data:
                    csv_write.writerow(job.values())
    except Exception as e:
        print(e)
        traceback.print_exc()
        traceback.print_exception()
# Scrape the joblinks
def jobLinkScrape(jobllinks,labels,jsonoutfile,details_filename):
    try:
        job_details_csv=details_filename +"-Details.csv"
        job_details_json=details_filename +"-Details.json"

        browser=scraperModule.fireFox_setup()
        print("Creating session with site")
        browser.get("https://a127-jobs.nyc.gov/")

        time.sleep(1)
        print("Getting the Job Link")
        jobJson=[]
        job_detail_json=[]
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
            job_detail_json.append(details)
            current_job={'HiringAgency':agency_title,'jobLink':link[0],'jobNum':link[1]}
            if len(dispData)>0:
                sys.stdout.write('\r')
                sys.stdout.flush()
                sys.stdout.write("On click: "+str(numclicks))
                sys.stdout.flush()
                
            for i in range(0,len(dispData)):
                current_job[labels[i]] = dispData[i].get_attribute('innerText') if dispData[i].get_attribute('innerText') is not "\u00a0" else "Not Listed"
            
            jobJson.append(current_job)

        with open(jsonoutfile, "w") as jsout:
            json.dump(jobJson,jsout,indent=4)
        try:
            with open(job_details_json, "w") as detailsout:
                json.dump(job_detail_json,detailsout,indent=4)
            print("Dumping Details to CSV")
            writeJobtoCsv(job_details_json,job_details_csv)
        except Exception as e:
            traceback.print_exc()

    except Exception as e:
        print(" ")
        print(e)
        traceback.print_exc()

        browser.quit()
    browser.quit()
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

if __name__== "__main__":
    jsonout=str(date.today())+str(time.time()).split(".")[0]+"JSON.json"
    csvout=str(date.today())+str(time.time()).split(".")[0]+"CSV.csv"
    # jobFile="AgencyJson.json"
    jobFile="TEST.json"
    joblinks=pulljoblinks(jobFile)
    print(str(len(joblinks)))
    detailsF="dinner"
    jobLinkScrape(joblinks,labels,jsonout,detailsF)

    writeJobtoCsv(jsonout,csvout)