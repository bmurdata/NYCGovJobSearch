#Selenium function to scrape the Job Site and put into JSON file

import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#Location of Geck Driver
import selpysettings
import time
import json
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

#Setup of browser
def fireFox_setup():
    try:
        browser=webdriver.Firefox(options=options)
    except:
        print("Switching to use selpysettings")
        try:
            browser = webdriver.Firefox(executable_path=selpysettings.gecko_Location,options=options)    
        except Exception as e:
            print(e)
            exit()
    return browser

def selScrape(careerInterest,badCareer,linkSrchTest,fileToWrite,browser,linkBase):
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
                    title=link.get_attribute('innerText')

                    nlink=linkBase.format(jobId=jobNum)

                    jsondata[jobcat].append({
                        'jobNum': jobNum,
                        'title':title,
                        'link':nlink,
                        'shortcategory':cat,
                        'longcategory':longcat
                    })
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
                            print("Failed to click button. Adding to second attempt.")
                            badCareer[longcat]=cat

                    print("Clicked the button")
                    numclicks=numclicks+1
                    time.sleep(2)
                except:
                    print("Hit the end of the list for "+ cat +" after "+str(numclicks) + " Clicks")
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