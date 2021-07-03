import time
import argparse
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
start_time=time.time()
agency_scrape_time="NA"
category_scrape_time="NA"
dir_path = os.path.dirname(os.path.realpath(__file__))+"/output/"

# Argparser
currTime=str(time.time()).split(".")[0]

default_code_file=str(date.today())+"_"+str(currTime)+"By-AgencyCode"

default_category_file=str(date.today())+"_"+str(currTime)+"By-Category"

parser = argparse.ArgumentParser(description="NYCGov Job site scraper. Outputs JSON and CSV files by job category and by specific agency.")

parser.add_argument("-afile","--agencyfile",help="Agency JSON and CSV file names.",
                    default=default_code_file)

parser.add_argument("-cfile","--categoryfile", help="Category JSON and CSV file names.",
                    default=default_category_file)
parser.add_argument("-writeDB","--writeDB",action="store_true",help="Update database from JSON data directly. Unless --noOutput is set, files will be created. Database must be setup for proper function.")
parser.add_argument("-noOutput","--noOutput",action="store_true",help="Stops creation of file output. Recommended only use when writeDB is set.")
parser.add_argument("-test","--test",action="store_true",help="Test script with two agencies to make sure all works.")

print(sys.argv[1:])
args = parser.parse_args()

# Run scraping and write to file 

print("Performing search scrape.")
# Scrape by category-Commented out by default.
# Location to put files
# category_jsonfile=dir_path+(args.categoryfile.split(".",1)[0])+".json"
# category_csvfile=dir_path+(args.categoryfile.split(".",1)[0])+".csv"

# careerInterest={"Administration and Human Resources":"CAS"}
# run_scrape(category_jsonfile,careerInterest,linkSrchTemplate_Category,jobLinkTemplate,category_csvfile)
# category_scrape_time=round(time.time()-start_time,2)

# Scrape by Agency Code
# Location to put files
code_jsonfile=dir_path+(args.agencyfile.split(".",1)[0]) + ".json"
code_csvfile=dir_path+(args.agencyfile.split(".",1)[0]) +".csv"

if args.test==True:
    print("Running using test parameters")
    agency_codes={"ADMINISTRATION FOR CHILDRE": "067", "CUNY BRONX COMMUNITY COLLE": "463"}
run_scrape(code_jsonfile,agency_codes,linkSrchTemplate_Code,jobLinkTemplate,code_csvfile,args.writeDB,args.noOutput)

agency_scrape_time=round(time.time()-start_time,2)
print("------")
print("Time to execute search by agency:{time}".format(time=agency_scrape_time))
print("------")
print("Time to execute search by category:{time}".format(time=category_scrape_time))

final_time=round(time.time()-start_time,2)

print("------")
print("Final time to execute:{time}".format(time=final_time))
print("To perform job scrape with multithreading run the following:")
try:
    input_code_json=code_jsonfile 
except:
    input_code_json= args.searchjsonfile
print("python .\getJobDetails.py --joblinkfile "+ str(input_code_json))
print("------")