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
import time
import json
import sys
# Selenium Setup
options = webdriver.FirefoxOptions()
#options.add_argument('-headless')
gecko_Location='./geckodriver.exe'

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
            print(e)
            exit()
    return browser
# Main scraper function
def selScrape(careerInterest,badCareer,linkSrchTest,browser,linkBase):
    jsondata={}
    numItems=len(careerInterest)
    itemcount=0

    for longcat,cat in careerInterest.items():
        try:
            browser.get(linkSrchTest.format(category=cat))
        except TimeoutException as e:
            print("Page took too long to load for "+longcat+". Continuing...")
            
            continue
        

        try:
            print("Trying to open page for "+longcat)
            time.sleep(2)
            iframe = browser.find_element_by_tag_name("iframe")
            browser.switch_to.default_content()
            browser.switch_to.frame(iframe)
            jobcat="jobs_for_" + cat
            jsondata[jobcat]=[]
            try:
                checkNull=browser.find_element_by_id("HRS_SCH_WRK_HRS_CC_NO_RSLT")
                if checkNull.get_attribute('innerText')=="No Results Found":
                    print(longcat+" has no items in it. Skipping.")
                    continue
            except:
                print("Values Found")


            #Keep clicking next until you hit the end of the list.
            numclicks=1
            while True:
                #Get the table
                sys.stdout.write('\r')
                sys.stdout.flush()
                sys.stdout.write("On click: "+str(numclicks))
                sys.stdout.flush()
                tb=browser.find_element_by_class_name("PSLEVEL1GRIDNBO")

                all_anchors=tb.find_elements_by_css_selector("a")
                all_attributes=tb.find_elements_by_css_selector("div.attributes")
                for i in range(0,len(all_anchors)):

                    jobNum=all_anchors[i].get_attribute('innerText')[-6:]
                    title=all_anchors[i].get_attribute('innerText')
                    nlink=linkBase.format(jobId=jobNum)
                    # var jar=[];for (var i=0;i<strarr.length;i++){ console.log(jar.push(strarr[i].split(":")[1].trim()))}
                    fullattributes=all_attributes[i].get_attribute('innerText').split("|")
                    splitattri=[]
                    # Break up the attributes to make JSON object
                    for attribute in fullattributes:
                        splitattri.append(attribute.strip().split(":"))
                    
                    attribute_Value={}

                    for pairs in splitattri:
                        attribute_Value[pairs[0].strip()]=pairs[1].strip()
                    numItems +=1
                    
                    jsondata[jobcat].append({
                            'jobNum': jobNum,
                            'title':title,
                            'link':nlink,
                            'shortcategory':cat,
                            'longcategory':longcat,
                            'jobAttributes':all_attributes[i].get_attribute('innerText'),#Break it up
                            'Department':attribute_Value['Department'] if 'Department' in attribute_Value else "Not Listed", # Department
                            'Agency':attribute_Value['Agency'] if 'Agency' in attribute_Value else "Not Listed", # Location
                            'Location':attribute_Value['Location'] if 'Location' in attribute_Value else "Not Listed", # Agency
                            'Posted_Date':datetime.datetime.strptime(attribute_Value['Posted Date'], "%m/%d/%Y").strftime("%Y-%m-%d") if 'Posted Date' in attribute_Value else "Not Listed", # Posted Date
                        })
                    

                #Find the button to load the next results.
                try:
                    button=browser.find_element_by_name("HRS_AGNT_RSLT_I$hdown$0")
                    #print("Found Button")
                    time.sleep(2)
                    try:
                        button.click()
                    except:
                        print("Failed to click the button. Now to try the browser button")
                        
                        try:
                            button=browser.find_element_by_xpath("//*[@class='PSHYPERLINK' and @class='PTNEXTROW1']")#('PSHYPERLINK PTNEXTROW1')
                            time.sleep(2)
                            button.click()
                        except Exception as e:
                            print(e)
                            print("Failed to click button. Adding to second attempt.")
                            print(" ")
                            badCareer[longcat]=cat

                    #print("Clicked the button")
                    numclicks=numclicks+1
                    time.sleep(2)
                except:
                    print(" ")
                    print("Hit the end of the list for "+ cat +" after "+str(numclicks) + " Clicks")
                    print(cat+" has "+str(len(jsondata[jobcat]))+ " jobs")
                    print(" ")

                    break
                    
        except Exception as e:
            print("I have failed at main try Block at "+cat+". Error message is: "+ str(e))
            badCareer[longcat]=cat
    browser.quit()
    print("There are "+ str(numItems) +" jobs found.")
    return jsondata

def writeJson(jsondata,fileToWrite):
    if jsondata:
        try:
            with open(fileToWrite, "w") as myfile:
                print("Preparing to write file ")
                json.dump(jsondata,myfile,indent=4)
        
        except Exception as e:
            print("Failed to write to file")
            print(str(e))

def jsonToCSV(jsonfile,jobcsv):

    with open(jobcsv,"w",newline='',encoding="utf-8") as initial:
        initial.write("jobNum,title,Link,shortCategory,longCategory,Department,Location,Agency,Posted Date\n")
        
    with open(jsonfile) as ifile:
        data=json.load(ifile)
        num=0
        with open(jobcsv,"a",newline='',encoding="utf-8") as jobs:

            for category in data:
                
                for item in data[category]:
                    new_record="\""+item['jobNum'] +"\",\""+item['title']+"\",\""+item['link']+"\",\""+item['shortcategory']+"\",\""+item['longcategory'] +"\",\""+item['Department']+"\",\""+item['Location']+"\",\""+item['Agency']+"\",\""+item['Posted_Date']+"\"\n"
                    jobs.write(new_record)
                    num += 1

def run_scrape(jsonfile,searchCriteria,linkTemplate,jobLinkTemplate,csvfile):
    badCareer={}
    try:
        browser=fireFox_setup()
        print("Opened Broswer")
        firstPass=selScrape(searchCriteria,badCareer,linkTemplate,browser,jobLinkTemplate)
    except Exception as e:
        print("Failed due to "+ str(e))
        browser.quit()

    stillBad={}

    #Based on what fails, conduct second pass
    if badCareer:
        try:
            browser=fireFox_setup()
            secondPass=selScrape(badCareer,stillBad,linkTemplate,browser,jobLinkTemplate)

        except Exception as e:
            print("Failed due to "+ str(e))
            browser.quit()
    if not badCareer:
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

    writeJson(firstPass,jsonfile)
    jsonToCSV(jsonfile,csvfile)

#Test of scraper module
if __name__=='__main__':
    start_time=time.time()
    joblinkBase="https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId={jobId}&PostingSeq=1&"
    #Agency Codes
    code_linkSrchTemplate="https://a127-jobs.nyc.gov/index_new.html?agency={category}"

    agency_codesTest={"Police Department": "056"}
    #Category
    cat_linkSrchTemplate="https://a127-jobs.nyc.gov/index_new.html?category={category}"

    careerInterestTest={"Administration and Human Resources":"CAS"}


    csvfile="CSV_CAT-3.csv"
    outfile="TODAY_Cat-3.json"
    selScrape(careerInterestTest,cat_linkSrchTemplate,joblinkBase,outfile,csvfile)
    outfile="TODAY_Code-3.json"
    csvfile="CSV_CODE-3.csv"
    selScrape(agency_codesTest,code_linkSrchTemplate,joblinkBase,outfile,csvfile)
             
    final_time=round(time.time()-start_time,2)
    print("------")
    print("Time to execute:{time}".format(time=final_time))
    print("------")