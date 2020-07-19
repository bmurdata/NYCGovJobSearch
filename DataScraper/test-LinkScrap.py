import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import traceback
import csv
#Location of Geck Driver
import time
import json

import argparse

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
#Python Selenium Settings
gecko_Location='C:/Users/dtman/git/Private_NYCGovJob/NYCGovJobSearch/geckodriver.exe'

def fireFox_setup():
    try:
        browser=webdriver.Firefox(options=options)
    except:
        print("Switching to use selpysettings")
        try:
            browser = webdriver.Firefox(executable_path=gecko_Location,options=options)    
        except Exception as e:
            print(e)
            exit()
    return browser


joblink=[
"https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=376405&PostingSeq=1&",
"https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=441207&PostingSeq=1&",
"https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=432041&PostingSeq=1&"]

labels=["Job_ID",
"Num_of_Positions",
"Business_Title",
"Civil_Service_Title",
"Title_Code_No",
"Level",
"Title_Classification",
"Job_Category",
"Proposed_Salary_Range",
"Career_Level",
"Work_Location",
"Division_Work_Unit",
"Posted",
"Post_Until"]
def writeJobtoCsv(jsonfile,jobcsv):
    try:
        with open(jsonfile) as ifile:
            data=json.load(ifile)
            header=data[0].keys()
            num=0
            with open(jobcsv,"w",newline='') as ofile:
                csv_write=csv.writer(ofile)
                csv_write.writerow(header)
                for job in data:
                    num +=1
                    csv_write.writerow(job.values())
            print(str(num))
    except Exception as e:
        print(e)
        traceback.print_exc()
        traceback.print_exception()


def test_jobLinksScrape(joblink,labels,jsonoutfile):
    browser=fireFox_setup()
    try: 
        print("Getting Main Link")
        browser.get("https://a127-jobs.nyc.gov/")

        time.sleep(1)
        print("Getting the Job Link")
        browser.get(joblink)

        with open("jobLinkHTML.html","w") as mfile:
            mfile.write(browser.page_source)
        jsondata={}

        json3={}
        json3['Class for SPan']=[]

        dispData=browser.find_elements_by_class_name("PSEDITBOX_DISPONLY")
        print(len(dispData))
        dispData.pop(0)
        print(len(dispData))
        for i in range(0,len(dispData)):
            print(str(i))
            json3['Class for SPan'].append(
                [dispData[i].get_attribute("class"),labels[i],
                dispData[i].get_attribute('innerText')])

        

    except Exception as e:
        print(e)
        browser.quit()
    browser.quit()

def jobLinkScrape(jobllinks,labels,jsonoutfile,csvoutfile):
    try:
        browser=fireFox_setup()
        print("Creating session with site")
        browser.get("https://a127-jobs.nyc.gov/")

        time.sleep(1)
        print("Getting the Job Link")
        jobJson=[]
        numclicks=0
        for link in jobllinks:
            browser.get(link)
            numclicks +=1
            dispData=browser.find_elements_by_class_name("PSEDITBOX_DISPONLY")
            try:
                agency_title=browser.find_element_by_id("HRS_BS_UNT_HR_I_DESCR").get_attribute('innerText')
            except:
                agency_title="Not Found"

            dispData.pop(0)


            current_job={'HiringAgency':agency_title,'jobLink':link}
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
        

    except Exception as e:
        print(" ")
        print(e)
        traceback.print_exc()

        browser.quit()
    browser.quit()


if __name__== "__main__":
    jsonout="job_json.json"
    csvout="job_csv.csv"

    jobFile="TODAY.json"
    joblinks=[]
    with open(jobFile,"r") as datafile:
        data=json.load(datafile)
        for category in data:
            for item in data[category]:
                joblinks.append(item['link'])

    print(str(len(joblinks)))
    jobLinkScrape(joblinks,labels,jsonout,csvout)

    writeJobtoCsv(jsonout,csvout)