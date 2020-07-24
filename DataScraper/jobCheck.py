import time
start_time=time.time()
import sys
import scraperModule
from scraperModule import selScrape
from scraperModule import fireFox_setup
from scraperModule import writeJson
from scraperModule import jsonToCSV
from scraperModule import run_scrape
from scrapeargs import args
from scrapeargs import linkSrchTemplate_Category, linkSrchTemplate_Code, agency_codes, careerInterest

import numpy
from multiprocessing import Pool
import traceback
search_scrape="NA"
job_scrape="NA"
if not args.nosearch:
    # Run scraping and write to file 
    joblinkBase="https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId={jobId}&PostingSeq=1&"

    print("Performing search scrape.")
    #Scrape by category
    category_jsonfile=(args.categoryfile.split(".",1)[0])+".json"
    category_csvfile=(args.categoryfile.split(".",1)[0])+".csv"

    #careerInterest={"Administration and Human Resources":"CAS"}
    run_scrape(category_jsonfile,careerInterest,linkSrchTemplate_Category,joblinkBase,category_csvfile)

    #Scrape by Code
    code_jsonfile=(args.agencyfile.split(".",1)[0]) + ".json"
    code_csvfile=(args.agencyfile.split(".",1)[0]) +".csv"

    #agency_codes={"ADMINISTRATION FOR CHILDRE": "067", "CUNY BRONX COMMUNITY COLLE": "463"}
    run_scrape(code_jsonfile,agency_codes,linkSrchTemplate_Code,joblinkBase,code_csvfile)

    search_scrape=round(time.time()-start_time,2)
    print("------")
    print("Time to execute search:{time}".format(time=search_scrape))
    print("------")

if args.scrapejoblinks:
    print("Preparing to run job scrape without multithreading.")
    job_jsonfile=(args.joboutput.split(".",1)[0]) +".json"
    job_csvfile=(args.joboutput.split(".",1)[0]) +".csv"
    
    job_details_file=(args.joboutput.split(".",1)[0]) +"-Details"
    
    import linkScrape
    try:
        input_code_json=code_jsonfile 
    except:
        input_code_json= args.searchjsonfile

    jlinks=linkScrape.pulljoblinks(input_code_json)
    linkScrape.jobLinkScrape(jlinks,linkScrape.labels,job_jsonfile,job_details_file)
    linkScrape.writeJobtoCsv(job_jsonfile,job_csvfile)
    job_scrape=round(time.time()-start_time,2)

print("------")
print("Time to execute job scrape:{time}".format(time=job_scrape))
print("------")


final_time=round(time.time()-start_time,2)
print("------")
print("Time to execute search:{time}".format(time=search_scrape))
print("Time to execute job scrape:{time}".format(time=job_scrape))
print("Final time to execute:{time}".format(time=final_time))
print("To perform job scrape with multithreading run the following:")
try:
    input_code_json=code_jsonfile 
except:
    input_code_json= args.searchjsonfile
print("python .\linkScrape_multithread.py --joblinkfile "+ str(input_code_json))
print("------")
