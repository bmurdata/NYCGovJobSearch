#import datetime 
from datetime import date, datetime
import time
import json
import sys
import os, traceback,re
from selCheck import Chrome_setup
import monCheck

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
        # print(len(fullList))
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
                    'Posted_Date':datetime.strptime(jobElements[11].get_attribute('innerText'), "%m/%d/%Y").strftime("%Y-%m-%d") if jobElements[11].get_attribute('innerText') else "Not Listed", # Posted Date
                }
                monCheck.writeToMongo(jobData,'jobsByCode')
                # allJobs_Dict.append(jobData)


            except Exception as e:
                print(e)
                print("Failed at getting job for fullList at "+job.get_attribute('innerText'))
                badCareer[longcat]=cat
    print("All done")
    # print(allJobs_Dict)
    browser.quit()
    # return allJobs_Dict

# Scrape the joblinks. Designed to work with multithreading
def scrape_multi_arr(jobllinks:list()):
    try:
        print("This thread has: "+str(len(jobllinks))+" items to run.")
        start__runtime=time.time()
        browser=Chrome_setup()
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
                # print("There are some number of labels. That number is "+str(len(jobLabels)))
                # print("There are some number of Content. That number is "+str(len(jobContent)))
                jobDescrip={jobLabels[i].get_attribute('innerText'):jobContent[i].get_attribute('innerText') for i in range(len(jobLabels))}
                # print("Sems to work! Dictionary of length: "+str(len(jobDescrip)))
            except Exception as e:
                print(e)
                print("Nothing to add")
                
            jobDescrip['jobNum']=link[1]
            jobDescrip['jobLink']=link[0]
            
            jobDescription = {label: jobDescrip.get(label,"Not listed") for label in myLabels.details_order}
            #jobDescription['jobNum']=link[1]
            job_detail.append(jobDescription)
            monCheck.writeToMongo(jobDescription,'jobInfo_Content')
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
            monCheck.writeToMongo(current_job,'jobInfo_Meta')
    except Exception as e:
        print("Not really sure why things fell apart. Keep trying ")
        print(e)
        traceback.print_exc()

        browser.quit()
    browser.quit()
    my_runtime=round(time.time()-start__runtime,2)

    return jobJson,job_detail,my_runtime

