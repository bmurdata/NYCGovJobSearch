import time 

start_time=time.time()

import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import requests
import time
#Custom Selenium Python settings for the FireFox Gecko Driver.
import selpysettings
import json

linkBase="https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId={jobId}&PostingSeq=1&"

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
#Selenium function to scrape the Job Site and put into JSON file
def selScrape(careerInterest,badCareer,linkSrchTest,fileToWrite):
    jsondata={}
    myjson=fileToWrite
    for longcat,cat in careerInterest.items():
        print(cat)
        browser.get(linkSrchTest.format(category=cat))

        try:
            print("Trying to open page for "+longcat)
            page=browser.page_source
            time.sleep(2)
            iframe = browser.find_element_by_tag_name("iframe")
            browser.switch_to.default_content()
            browser.switch_to.frame(iframe)
            jobcat="jobs_for_" + cat
            jsondata[jobcat]=[]
            #Keep clicking next until you hit the end of the list.
            numclicks=1
            while True:
                #Get the table 
                tb=browser.find_element_by_class_name("PSLEVEL1GRIDNBO")
                #Get all the links in the table
                all_anchors=tb.find_elements_by_tag_name("a")
                #Update the links in the table, and database

                for link in all_anchors:
                    jobNum=link.get_attribute('innerText')[-6:]

                    nlink=linkBase.format(jobId=jobNum)

                    jsondata[jobcat].append({
                        'jobNum': jobNum,
                        'link':nlink,
                        'shortcategory':cat,
                        'longcategory':longcat
                    })
                    #toDB(nlink,cat,longcat,jobNum)          
                print('Writing the table again')
                try:
                    button=browser.find_element_by_name("HRS_AGNT_RSLT_I$hdown$0")
                    print("Found Button")
                    time.sleep(2)
                    try:
                        button.click()
                    except:
                        print("Failed to click the button. Now to try the browser button")
                        
                        try:
                            button=browser.find_element_by_xpath("//*[@class='PSHYPERLINK' and @class='PTNEXTROW1']")#('PSHYPERLINK PTNEXTROW1')
                            print("About to click the browser button")
                            time.sleep(2)
                            button.click()
                            print("This time it worked. Huzzah!")
                        except Exception as e:
                            print(e)
                            print("Failed to click button. Will try again on next round.")
                            badCareer[longcat]=cat
                            '''with open(jsfile,"a") as jsfile:
                                print("Dumping the data to "+ jsfile)
                                json.dump(jsondata,jsfile)
                                '''
                    print("Clicked the button")
                    numclicks=numclicks+1
                    time.sleep(2)
                except:
                    print("Hit the end of the list for "+ cat +" after "+str(numclicks) + " Clicks")
                    '''with open(jsfile,"a") as jsfile:
                        print("Dumping collected tables to jsonfile")
                        json.dump(jsondata,jsfile)
                        print("Dump complete")
                        '''
                    break
        except Exception as e:
            print("I have failed at main try Block at "+cat+". Error message is: "+ str(e))

            badCareer[longcat]=cat
    if jsondata:
        try:  
            with open(myjson,"a") as myfile:
                print("Preparing to write file ")
                json.dump(jsondata,myfile)
        except Exception as e:
            print("Failed to dump the json")
            print(str(e))
    
    print("There are "+str(len(jsondata))+ " total categories")
    for category in jsondata:
        print(category+ " has "+str(len(jsondata[category])) +" jobs in it")
    
linkSrchTest="https://a127-jobs.nyc.gov/index_new.html?category={category}"

careerInterest={"Administration and Human Resources":"CAS",
                "Communications and Intergovernmental Affairs":"CIG",
                "Constituent Services and Community Programs":"CBS",
                "Engineering, Architecture and Planning":"EAP",
                "Finance, Accounting and Procurement":"FAP",
                "Health":"HLT",
                "Technology, Data and Innovation":"ITT",
                "Legal Affairs":"LEG",
                "Policy, Research and Analysis":"POA",
                "Public Safety, Inspections and Enforcement":"PSI",
                "Social Services":"SOC"
                }
badCareer={}


try:
    browser=webdriver.Firefox(options=options)
except:
    print("Switching to use selpysettings")
    try:
         browser = webdriver.Firefox(executable_path=selpysettings.gecko_Location,options=options)
    except Exception as e:
        print(e)
        exit()

   
print("Opened the Browser")
jsonfile="test6.json"
selScrape(careerInterest,badCareer,linkSrchTest,jsonfile)
stillBad={}
try:
    selScrape(badCareer,stillBad,linkSrchTest,jsonfile)
except:
    browser.quit()
print("The following still failed:")
for x in stillBad:
    print(x)
final_time=round(time.time()-start_time,2)
print("------")
print("Time to execute:{time}".format(time=final_time))
print("------")

browser.quit()