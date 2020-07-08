import time 

start_time=time.time()

import scraperModule
from scraperModule import selScrape
from scraperModule import fireFox_setup
linkBase="https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId={jobId}&PostingSeq=1&"


    
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

   
print("Opened the Browser")
jsonfile="output.json"
try:
    browser=fireFox_setup()
    selScrape(careerInterest,badCareer,linkSrchTest,jsonfile,browser,linkBase)
except Exception as e:
    print("Failed due to "+ str(e))

stillBad={}
try:
    browser=fireFox_setup()
    selScrape(badCareer,stillBad,linkSrchTest,jsonfile,browser,linkBase)
except Exception as e:
    print("Failed due to "+ str(e))


print("The following still failed:")
for x in stillBad:
    print(x)
final_time=round(time.time()-start_time,2)
print("------")
print("Time to execute:{time}".format(time=final_time))
print("------")