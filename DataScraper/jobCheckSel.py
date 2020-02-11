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
import pyodbc
#Custom Selenium Python settings for the FireFox Gecko Driver.
import selpysettings
import dbtest
from dbtest import toDB
options = webdriver.FirefoxOptions()
#options.add_argument('-headless')
from dbtest import linkBase
tablefile="attempt_one.html"
ofile3=open(tablefile,"a")

def selScrape(careerInterest,badCareer,linkSrchTest,htmlFile):

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
            #Div added to make it collapsible in VS Code
            htmlFile.write("<br><div class="+cat+"><br>")
            htmlFile.write("<h1> START OF CATEGORY "+longcat +"</h1>")

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
                    newlink="arguments[0].setAttribute('href','{linky}')".format(linky=nlink)
                    browser.execute_script(newlink, link)
                    toDB(nlink,cat,longcat,jobNum)

                htmlFile.write('<br><h1> New Table to check</h1>')
                print('Writing the table again')
                htmlFile.write(tb.get_attribute('outerHTML'))

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

                    print("Clicked the button")
                    numclicks=numclicks+1
                    time.sleep(2)
                except:
                    print("Hit the end of the list for "+ cat +" after "+str(numclicks) + " Clicks")

                    htmlFile.write("<h1> END OF CATEGORY "+longcat +"</h1>")
                    htmlFile.write("<br></div>")
                    break
        except Exception as e:
            print("I have failed at main try Block at "+cat+". Error message is: "+ str(e))
            badCareer[longcat]=cat


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

selScrape(careerInterest,badCareer,linkSrchTest,ofile3)
stillBad={}
tablefile="attempt_two.html"
badjobCheck=open(tablefile,"a")
selScrape(badCareer,stillBad,linkSrchTest,badjobCheck)
print("The following still failed")
for x in stillBad:
    print(x)

browser.quit()