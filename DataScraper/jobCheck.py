import time
import argparse
start_time=time.time()
import sys
import scraperModule
from scraperModule import selScrape
from scraperModule import fireFox_setup
from scraperModule import run_scrape
# from scrapeargs import args
from scrapeargs import linkSrchTemplate_Category, linkSrchTemplate_Code, agency_codes, careerInterest,jobLinkTemplate
import os 
import numpy
from datetime import date
from multiprocessing import Pool
import traceback
search_scrape="NA"
job_scrape="NA"
dir_path = os.path.dirname(os.path.realpath(__file__))+"/output/"

# Argparser
currTime=str(time.time()).split(".")[0]

default_code_file=str(date.today())+"_"+str(currTime)+"By-AgencyCode"

default_category_file=str(date.today())+"_"+str(currTime)+"By-Category"

default_job_file=str(date.today()) +"_"+currTime+"Job-Data"

parser = argparse.ArgumentParser(description="NYCGov Job site scraper. Outputs JSON and CSV files by job category and by specific agency.")

parser.add_argument("-afile","--agencyfile",help="Agency JSON and CSV file names.",
                    default=default_code_file)

parser.add_argument("-cfile","--categoryfile", help="Category JSON and CSV file names.",
                    default=default_category_file)

parser.add_argument("-jobout","--joboutput", help="Job Link JSON and CSV output files.",
                    default=default_job_file)
                    
parser.add_argument("-withlinks","--scrapejoblinks", help="If set, runs scrape for all job links, after getting them from search. Defaults to false",
                    action="store_true")
                          
parser.add_argument("--nosearch", help="If set, skips scrape for search pages, by category and code. Defaults to false",
                    action="store_true")

parser.add_argument("-searchjson","--searchjsonfile", help="Job JSON file to use if --nosearch is set. Required with --nosearch")


print(sys.argv[1:])
args = parser.parse_args()
# If you have a JSON job file to search
if args.nosearch:
    if not args.searchjsonfile:
        parser.error("When --nosearch is specified, --searchjson must be specified and valid.")
    else:
        try:
            with open(args.searchjsonfile,"r") as testopen:
                data=json.load(testopen)
                if len(data) ==0:
                    parser.error("File is empty")
            args.scrapejoblinks=True

        except Exception as e:
            print("Things not going as planned")
            print(e)
            sys.exit(1)

if not args.nosearch:
    
    # Run scraping and write to file 
    
    print("Performing search scrape.")
    # Scrape by category
    # Location to put files
    # category_jsonfile=dir_path+(args.categoryfile.split(".",1)[0])+".json"
    # category_csvfile=dir_path+(args.categoryfile.split(".",1)[0])+".csv"

    # careerInterest={"Administration and Human Resources":"CAS"}
    # run_scrape(category_jsonfile,careerInterest,linkSrchTemplate_Category,jobLinkTemplate,category_csvfile)

    # Scrape by Agency Code
    # Location to put files
    code_jsonfile=dir_path+(args.agencyfile.split(".",1)[0]) + ".json"
    code_csvfile=dir_path+(args.agencyfile.split(".",1)[0]) +".csv"

    # agency_codes={"ADMINISTRATION FOR CHILDRE": "067", "CUNY BRONX COMMUNITY COLLE": "463"}
    run_scrape(code_jsonfile,agency_codes,linkSrchTemplate_Code,jobLinkTemplate,code_csvfile)

    search_scrape=round(time.time()-start_time,2)
    print("------")
    print("Time to execute search:{time}".format(time=search_scrape))
    print("------")
# TO-DO: rewrite, run job link scrape without multithreading. joblinkscrape module
if args.scrapejoblinks:
    print("Preparing to run job scrape without multithreading.")
    job_jsonfile=dir_path+(args.joboutput.split(".",1)[0]) +".json"
    job_csvfile=dir_path+(args.joboutput.split(".",1)[0]) +".csv"
    
    job_details_file=dir_path+(args.joboutput.split(".",1)[0]) +"-Details"
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
print("python .\getJobDetails.py --joblinkfile "+ str(input_code_json))
print("------")
