import datetime 
from datetime import date
import time
import json
import sys
import os
from selCheck import Chrome_setup
import monCheck

# Scrape for job information, and links
def jobScrape(criteria_Dict,badCareer,jobSource,directJobLink):
    try:
        browser=Chrome_setup()
        print("Browser opened")
    except Exception as e:
        print(e)
        exit()
    allJobs_Dict=[]
    for longcat,cat in criteria_Dict.items():
        # allJobs_Dict[cat]=list()
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
                monCheck.writeToMongo(jobData,'test-jobsByCode')
                allJobs_Dict.append(jobData)


            except Exception as e:
                print(e)
                print("Failed at getting job for fullList at "+job.get_attribute('innerText'))
                badCareer[longcat]=cat
    print("All done")
    # print(allJobs_Dict)
    browser.quit()
    return allJobs_Dict

