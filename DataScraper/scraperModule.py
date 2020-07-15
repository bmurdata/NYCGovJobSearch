#Selenium function to scrape the Job Site and put into JSON file
import traceback
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

def selScrape(careerInterest,badCareer,linkSrchTest,browser,linkBase):
    jsondata={}
    for longcat,cat in careerInterest.items():
        print(cat)
        browser.get(linkSrchTest.format(category=cat))

        try:
            print("Trying to open page for "+longcat)
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
                #all_anchors=tb.find_elements_by_tag_name("a")
                #Get all the links in the table
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
                            'Posted_Date':attribute_Value['Posted Date'] if 'Posted Date' in attribute_Value else "Not Listed", # Posted Date
                        })

                # for link in all_anchors:
                #     jobNum=link.get_attribute('innerText')[-6:]
                #     title=link.get_attribute('innerText')

                #     nlink=linkBase.format(jobId=jobNum)

                #     jsondata[jobcat].append({
                #         'jobNum': jobNum,
                #         'title':title,
                #         'link':nlink,
                #         'shortcategory':cat,
                #         'longcategory':longcat
                #     })
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
                            badCareer[longcat]=cat

                    #print("Clicked the button")
                    numclicks=numclicks+1
                    time.sleep(2)
                except:
                    print("Hit the end of the list for "+ cat +" after "+str(numclicks) + " Clicks")
                    print(cat+" has "+str(len(jsondata[jobcat]))+ " jobs")
                    break
                    
        except Exception as e:
            print("I have failed at main try Block at "+cat+". Error message is: "+ str(e))

            badCareer[longcat]=cat
    
    
    # print("There are "+str(len(jsondata))+ " total categories")
    # for category in jsondata:
    #     print(category+ " has "+str(len(jsondata[category])) +" jobs in it")
    browser.quit()

    return jsondata

def writeJson(jsondata,fileToWrite):
    if jsondata:
        try:
            with open(fileToWrite, "w") as myfile:
                print("Preparing to write file ")
                json.dump(jsondata,myfile)
        
        except Exception as e:
            print("Failed to write to file")
            print(str(e))

def jsonToCSV(jsonfile,jobcsv):

    with open(jobcsv,"w") as initial:
        initial.write("jobNum,title,Link,shortCategory,longCategory,Department,Location,Agency,Posted Date\n")
        
    with open(jsonfile) as ifile:
        data=json.load(ifile)
        num=0
        with open(jobcsv,"a") as jobs:

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




def testScrape(careerInterest,linkSrchTest,linkBase,outfile,csvfile):
    jsondata={}
    browser=fireFox_setup()

    for longcat,cat in careerInterest.items():
        print(cat)
        browser.get(linkSrchTest.format(category=cat))
        print(linkSrchTest.format(category=cat))
        try:
            print("Trying to open page for "+longcat)
            time.sleep(2)
            iframe = browser.find_element_by_tag_name("iframe")
            browser.switch_to.default_content()
            browser.switch_to.frame(iframe)
            jobcat="jobs_for_" + cat
            jsondata[jobcat]=[]
            #Keep clicking next until you hit the end of the list.
            numclicks=1
            while True:
                print("Trying here")
                #Get the table 
                tb=browser.find_element_by_class_name("PSLEVEL1GRIDNBO")
                #Get all the links in the table
                all_anchors=tb.find_elements_by_css_selector("a")
                all_attributes=tb.find_elements_by_css_selector("div.attributes")
                for i in range(0,len(all_anchors)):
                    print("Going through the thing")
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
                    print(str(jobNum)+" "+ title)
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
                            'Posted_Date':attribute_Value['Posted Date'] if 'Posted Date' in attribute_Value else "Not Listed", # Posted Date
                        })
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

                    numclicks=numclicks+1
                    time.sleep(2)
                except:
                    print("Hit the end of the list for "+ cat +" after "+str(numclicks) + " Clicks")
                    print(cat+" has "+str(len(jsondata[jobcat]))+ " jobs")
                    break
                    
        except Exception as e:
            print("I have failed at main try Block at "+cat+". Error message is: "+ str(e))
            traceback.print_exc()
            browser.quit()
    
    with open(outfile,"w") as jfile:
        json.dump(jsondata,jfile)

    jsonToCSV(outfile,csvfile)
    browser.quit()

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
    testScrape(careerInterestTest,cat_linkSrchTemplate,joblinkBase,outfile,csvfile)
    outfile="TODAY_Code-3.json"
    csvfile="CSV_CODE-3.csv"
    testScrape(agency_codesTest,code_linkSrchTemplate,joblinkBase,outfile,csvfile)
    all_attributes=[ "Department: Leased HSG-BX client Services | Location: BRONX | Agency: NYC HOUSING AUTHORITY | Posted Date: 07/10/2020",
                    "Department: Executive Management | Location: BROOKLYN | Agency: NYC EMPLOYEES RETIREMENT SYS | Posted Date: 06/24/2020"]

    def mytest(all_attributes):
        for i in range(0,len(all_attributes)):
            print("Going through the thing")
            # var jar=[];for (var i=0;i<strarr.length;i++){ console.log(jar.push(strarr[i].split(":")[1].trim()))}
            fullattributes=all_attributes[i].split("|")
            splitattri=[]
            jsontest={}
            jsontest['Potatoe']=[]
            for attribute in fullattributes:
                splitattri.append(attribute.strip().split(":"))
            
            print(splitattri)
            jsontest['Potatoe'].append({
                splitattri[0][0].strip():splitattri[0][1].strip(),
                splitattri[1][0].strip():splitattri[1][1].strip(),
                splitattri[2][0].strip():splitattri[2][1].strip(),
                splitattri[3][0].strip():splitattri[3][1].strip(),
            })
            print(jsontest['Potatoe'])

    final_time=round(time.time()-start_time,2)
    print("------")
    print("Time to execute:{time}".format(time=final_time))
    print("------")