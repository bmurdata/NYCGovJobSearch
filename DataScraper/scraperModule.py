#Selenium function to scrape the Job Site and put into JSON file
import traceback
import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import datetime 
from datetime import date
import time
import json
import sys
import os
from scrapeargs import gecko_Location,jobLinkTemplate,agency_codes
# Selenium Setup
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

# Setup of browser
def fireFox_setup():
    try:
        browser=webdriver.Firefox(options=options)
        browser.set_page_load_timeout(90)
    except:
        print("Switching to use selpysettings")
        try:
            
            browser = webdriver.Firefox(executable_path=gecko_Location,options=options)
            browser.set_page_load_timeout(90)

        except Exception as e:
            print("FireFox Geckodriver not found. Either add it to PATH or to the geckodrivers folder. Alternatively, edit the scraperModule.py file gecko_Location variable.")
            print(e)
            exit()
    return browser

# Scrape for job information, and links
def selScrape(criteria_Dict,badCareer,jobSource,directJobLink):
    try:
        browser=fireFox_setup()
        print("Browser opened")
    except Exception as e:
        print(e)
        exit()
    allJobs_Dict={}
    for longcat,cat in criteria_Dict.items():
        allJobs_Dict[cat]=list()
        print("Trying to find  "+ longcat)

        try:
            browser.get(jobSource.format(category=cat))
        except:
            print(e)
            badCareer[longcat]=cat
            continue
        try:
            browser.find_element_by_css_selector(".ps_box-more")
            failover=False
        except Exception as e:
            print("No scroll action to take at "+longcat)
            failover=True
        if failover==False:
            # Failsafe to prevent refreshes from lasting too long. Based on the idea that it can load at most 20 results.
            x=0
            while  x<20:
                try:
                    reloader= browser.find_element_by_css_selector(".ps_box-more")
                    browser.execute_script("submitAction_win0(document.win0,'HRS_AGNT_RSLT_I$hdown$0')")
                    time.sleep(1)
                    x=x+1
                    
                except Exception as e:
                    print(e)
                    print("Stopped for "+longcat+" at scroll "+str(x))
                    x=20
        print("Looking for the jobs")
        # List of all the jobs
        fullList=browser.find_elements_by_css_selector("div[title='Search Results List'] li")
        print(len(fullList))
        for job in fullList:
            try:
                # print(job.find_elements_by_css_selector("span"))
                jobElements=job.find_elements_by_css_selector("span")
                jobData={
                    'jobNum': jobElements[3].get_attribute('innerText'),
                    'title':jobElements[1].get_attribute('innerText'),
                    'link':directJobLink.format(jobId=jobElements[3].get_attribute('innerText')),
                    'shortcategory':cat,
                    'longcategory':longcat,
                    'jobAttributes':job.get_attribute('innerText'),#Break it up
                    'Department':jobElements[7].get_attribute('innerText'), # Department
                    'Agency':jobElements[9].get_attribute('innerText'), # Location
                    'Location':jobElements[5].get_attribute('innerText'), # Agency
                    'Posted_Date':datetime.datetime.strptime(jobElements[11].get_attribute('innerText'), "%m/%d/%Y").strftime("%Y-%m-%d") if jobElements[11].get_attribute('innerText') else "Not Listed", # Posted Date
                }
                allJobs_Dict[cat].append(jobData)

            except Exception as e:
                print(e)
                print("Failed at getting job for fullList at "+job.get_attribute('innerText'))
                badCareer[longcat]=cat
    print("All done")
    # print(allJobs_Dict)
    browser.quit()
    return allJobs_Dict
# Writes Json and CSV files
def writeToFiles(jsondata,jsonFile,csvFile):
    
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
                        

# Main entry point. Runs the scrape
def run_scrape(jsonfile,searchCriteria,linkTemplate,jobLinkTemplate,csvfile,writeDB,noOutput):
    badSearch={}
    try:

        firstPass=selScrape(searchCriteria,badSearch,linkTemplate,jobLinkTemplate)
    except Exception as e:
        print("Failed due to "+ str(e))

    stillBad={}

    #Based on what fails, conduct second pass
    if badSearch:
        try:
            browser=fireFox_setup()
            secondPass=selScrape(badSearch,stillBad,linkTemplate,jobLinkTemplate)

        except Exception as e:
            print("Failed due to "+ str(e))
            browser.quit()
    if not badSearch:
        secondPass={}
    print("The following still failed:")

    for x in stillBad:
        print(x)
    # Combine first and second pass dictionaries
    print("First pass has "+str(len(firstPass)))

    print("Second pass has "+str(len(secondPass)))

    for key in secondPass:
        if key in firstPass:
            matches=0
            for item in secondPass[key]:
                if item not in firstPass[key]:
                    firstPass[key].append(item)
                else:
                    matches +=1
            print(key+" had "+str(matches)+" matches")
        else:
            firstPass[key]=secondPass[key]
    print("Combined the passes have "+str(len(firstPass)))

    print("There are "+str(len(firstPass))+ " total categories in firstpass")
    for category in firstPass:
        print(category+ " has "+str(len(firstPass[category])) +" jobs in it")

    print("There are "+str(len(secondPass))+ " total categories in secondpass")
    for category in secondPass:
        print(category+ " has "+str(len(secondPass[category])) +" jobs in it")
    if writeDB==True:
        from checkDB import writeAgencyData
        writeAgencyData(firstPass)
    if noOutput !=True:
        writeToFiles(firstPass,jsonfile,csvfile)

if __name__=='__main__':
    print("Preparing for the worst")
    start_time=time.time()

    dir_path = os.path.dirname(os.path.realpath(__file__))+"/output/"

    currTime=str(time.time()).split(".")[0]

    default_code_file=str(date.today())+"_"+str(currTime)+"By-AgencyCode"

    default_category_file=str(date.today())+"_"+str(currTime)+"By-Category"

    # Agency Codes
    code_linkSrchTemplate="https://a127-jobs.nyc.gov/index_new.html?agency={category}"

    # agency_codesTest={"Police Department": "056","Health or Something":"816"}

    badCareer={}
    jobs=selScrape(agency_codes,badCareer,code_linkSrchTemplate,jobLinkTemplate)

    writeToFiles(jobs,dir_path+default_code_file+".json",dir_path+default_code_file+".csv")
    # print(jobs)
    # Category
    # cat_linkSrchTemplate="https://a127-jobs.nyc.gov/index_new.html?category={category}"

    # careerInterestTest={"Administration and Human Resources":"CAS"}
       
    final_time=round(time.time()-start_time,2)
    print("------")
    print("Time to execute:{time}".format(time=final_time))
    print("------")