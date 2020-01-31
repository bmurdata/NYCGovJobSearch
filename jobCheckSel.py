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

options = webdriver.FirefoxOptions()
#options.add_argument('-headless')

tablefile="tableSourceFinal.html"
ofile3=open(tablefile,"a")


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

 #['CAS','CIG','CBS','EAP','FAP','HLT','ITT','LEG','MOP','POA','PSI','SOC']
careerInterest={"Administration and Human Resources":"CAS","Social Services":"SOC"}
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

for longcat,cat in careerInterest.items():
    print(cat)
    browser.get(linkSrchTest.format(category=cat))

    try:
        print("Trying to open page for "+cat)
        page=browser.page_source
        #ofile2.write(page)
        iframe = browser.find_element_by_tag_name("iframe")
        browser.switch_to.default_content()
        browser.switch_to.frame(iframe)
        ofile3.write("<h1> START OF CATEGORY "+longcat +"</h1>")

        #Keep clicking next until you hit the end of the list.
        numclicks=1
        while True:
            #print("Going through the list")
            tb=browser.find_element_by_class_name("PSLEVEL1GRIDNBO")
            tb=tb.get_attribute('outerHTML')
        
            ofile3.write(tb)
            try:
                button=browser.find_element_by_name("HRS_AGNT_RSLT_I$hdown$0")
                print("Found Button")
                time.sleep(2)
                try:
                    button.click()
                except:
                    print("Failed to click the button. Now to try the browser button")
                    button=browser.find_element_by_class_name('PSHYPERLINK PTNEXTROW1')
                    try:
                        button.click()
                    except Exception as e:
                        print(e)
                        print("Somethng weired happen")

                print("Clicked the button")
                numclicks=numclicks+1
                time.sleep(2)
            except:
                print("Hit the end of the list for "+ cat +" after "+str(numclicks) + " Clicks")
                ofile3.write("<h1> END OF CATEGORY "+longcat +"</h1>")
                break
    except Exception as e:
        print("I have failed at main try Block at "+cat+". Error message is: "+ str(e))
        
browser.quit()