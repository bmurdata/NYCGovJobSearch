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

# Run scraping and write to file 
joblinkBase="https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId={jobId}&PostingSeq=1&"


#Scrape by category
category_jsonfile=(args.categoryfile.split(".",1)[0])+".json"
category_csvfile=(args.categoryfile.split(".",1)[0])+".csv"

careerInterest={"Administration and Human Resources":"CAS"}
run_scrape(category_jsonfile,careerInterest,linkSrchTemplate_Category,joblinkBase,category_csvfile)

#Scrape by Code
code_jsonfile=(args.agencyfile.split(".",1)[0]) + ".json"
code_csvfile=(args.agencyfile.split(".",1)[0]) +".csv"

agency_codes={"ADMINISTRATION FOR CHILDRE": "067", "CUNY BRONX COMMUNITY COLLE": "463"}
run_scrape(code_jsonfile,agency_codes,linkSrchTemplate_Code,joblinkBase,code_csvfile)


if args.scrapelinks:
    job_jsonfile=(args.joboutput.split(".",1)[0]) +".json"
    job_csvfile=(args.joboutput.split(".",1)[0]) +".csv"


final_time=round(time.time()-start_time,2)
print("------")
print("Time to execute:{time}".format(time=final_time))
print("------")