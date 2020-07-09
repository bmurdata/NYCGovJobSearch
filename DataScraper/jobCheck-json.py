import time 

start_time=time.time()

import scraperModule
from scraperModule import selScrape
from scraperModule import fireFox_setup
from scraperModule import writeJson

# Function to scrape NYC Gov Jobs and output to file

def run_scrape(jsonfile,searchCriteria,linkTemplate,jobLinkTemplate):
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
# Run scraping and write to file 

# Category Check
joblinkBase="https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId={jobId}&PostingSeq=1&"


    
linkSrchTemplate="https://a127-jobs.nyc.gov/index_new.html?category={category}"

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
#careerInterest={"Administration and Human Resources":"CAS"}

category_jsonfile="SECOND-job-by-category.json"

run_scrape(category_jsonfile,careerInterest,linkSrchTemplate,joblinkBase)

# Agency check
code_jsonfile="SECOND-job-by-code.json"
linkSrchTemplate="https://a127-jobs.nyc.gov/index_new.html?agency={category}"
agency_codes={
    "ADMINISTRATION FOR CHILDRE": "067",
    "BOARD OF CORRECTIONS": "073",
    "BOARD OF ELECTIONS": "003",
    "BOROUGH PRESIDENT-BRONX": "011",
    "BOROUGH PRESIDENT-BROOKLYN": "012",
    "BOROUGH PRESIDENT-MANHATTA": "010",
    "BOROUGH PRESIDENT-QUEENS": "013",
    "BOROUGH PRESIDENT-RICHMOND": "014",
    "BUSINESS INTEGRITY COMMISS": "831",
    "CAMPAIGN FINANCE BOARD": "004",
    "CITY CLERK": "103",
    "CITY COUNCIL": "102",
    "CIVILIAN COMPLAINT REVIEW": "054",
    "CIVIL SERVICE COMMISSION": "134",
    "COMMISSION ON HUMAN RIGHTS": "226",
    "COMMUNITY BOARD N0.9-MANHA": "349",
    "COMMUNITY BOARD NO.10-BRON": "390",
    "COMMUNITY BOARD NO.10-BROO": "480",
    "COMMUNITY BOARD NO.10-MANH": "350",
    "COMMUNITY BOARD NO.10-QUEE": "440",
    "COMMUNITY BOARD NO.11-BRON": "391",
    "COMMUNITY BOARD NO.11-BROO": "481",
    "COMMUNITY BOARD NO.11-MANH": "351",
    "COMMUNITY BOARD NO.11-QUEE": "441",
    "COMMUNITY BOARD NO.12-BRON": "392",
    "COMMUNITY BOARD NO.12-BROO": "482",
    "COMMUNITY BOARD NO.12-MANH": "352",
    "COMMUNITY BOARD NO.12-QUEE": "442",
    "COMMUNITY BOARD NO.13-BROO": "483",
    "COMMUNITY BOARD NO.13-QUEE": "443",
    "COMMUNITY BOARD NO.14-BROO": "484",
    "COMMUNITY BOARD NO.14-QUEE": "444",
    "COMMUNITY BOARD NO.15-BROO": "485",
    "COMMUNITY BOARD NO.16-BROO": "486",
    "COMMUNITY BOARD NO.17-BROO": "487",
    "COMMUNITY BOARD NO.18-BROO": "488",
    "COMMUNITY BOARD NO.1 BRONX": "381",
    "COMMUNITY BOARD NO.1-BROOK": "471",
    "COMMUNITY BOARD NO.1-MANHA": "341",
    "COMMUNITY BOARD NO.1-QUEEN": "431",
    "COMMUNITY BOARD NO.1-RICHM": "491",
    "COMMUNITY BOARD NO.2-BRONX": "382",
    "COMMUNITY BOARD NO.2-BROOK": "472",
    "COMMUNITY BOARD NO.2-MANHA": "342",
    "COMMUNITY BOARD NO.2-QUEEN": "432",
    "COMMUNITY BOARD NO.2-RICHM": "492",
    "COMMUNITY BOARD NO.3-BRONX": "383",
    "COMMUNITY BOARD NO.3-BROOK": "473",
    "COMMUNITY BOARD NO.3-MANHA": "343",
    "COMMUNITY BOARD NO.3-QUEEN": "433",
    "COMMUNITY BOARD NO.3-RICHM": "493",
    "COMMUNITY BOARD NO.4 BRONX": "384",
    "COMMUNITY BOARD NO.4-BROOK": "474",
    "COMMUNITY BOARD NO.4-MANHA": "344",
    "COMMUNITY BOARD NO.4-QUEEN": "434",
    "COMMUNITY BOARD NO.5-BRONX": "385",
    "COMMUNITY BOARD NO.5-BROOK": "475",
    "COMMUNITY BOARD NO.5-MANHA": "345",
    "COMMUNITY BOARD NO.5-QUEEN": "435",
    "COMMUNITY BOARD NO.6-BRONX": "386",
    "COMMUNITY BOARD NO.6-BROOK": "476",
    "COMMUNITY BOARD NO.6-MANHA": "346",
    "COMMUNITY BOARD NO.6-QUEEN": "436",
    "COMMUNITY BOARD NO.7-BRONX": "387",
    "COMMUNITY BOARD NO.7-BROOK": "477",
    "COMMUNITY BOARD NO.7-MANHA": "347",
    "COMMUNITY BOARD NO.7-QUEEN": "437",
    "COMMUNITY BOARD NO.8-BRONX": "388",
    "COMMUNITY BOARD NO.8-BROOK": "478",
    "COMMUNITY BOARD NO.8-MANHA": "348",
    "COMMUNITY BOARD NO.8-QUEEN": "438",
    "COMMUNITY BOARD NO.9-BRONX": "389",
    "COMMUNITY BOARD NO.9-BROOK": "479",
    "COMMUNITY BOARD NO.9-QUEEN": "439",
    "CONFLICTS OF INTEREST BOAR": "312",
    "CUNY BRONX COMMUNITY COLLE": "463",
    "CUNY CENTRAL OFFICE": "467",
    "CUNY COLLEGE OF STATEN ISL": "462",
    "CUNY HOSTOS COMMUNITY COLL": "468",
    "CUNY HUNTER COLLEGE HIGH S": "470",
    "CUNY KINGSBOROUGH COMMMUNI": "465",
    "CUNY LAGUARDIA COMMUNITY C": "469",
    "CUNY MANHATTAN COMMUNITY C": "466",
    "CUNY MEDGAR EVERS COLLEGE": "453",
    "CUNY QUEENSBOROUGH COMMUNI": "464",
    "DEPARTMENT FOR THE AGING": "125",
    "DEPARTMENT OF BUILDINGS": "810",
    "DEPARTMENT OF BUSINESS SER": "801",
    "DEPARTMENT OF CITY PLANNIN": "030",
    "DEPARTMENT OF CITYWIDE ADM": "868",
    "DEPARTMENT OF CONSUMER AFF": "866",
    "DEPARTMENT OF CORRECTION": "072",
    "DEPARTMENT OF CULTURAL AFF": "126",
    "DEPARTMENT OF DESIGN AND C": "850",
    "DEPARTMENT OF EDUCATION": "740",
    "DEPARTMENT OF ENVIRONMENTA": "826",
    "DEPARTMENT OF FINANCE": "836",
    "DEPARTMENT OF HEALTH AND M": "816",
    "DEPARTMENT OF HOMELESS SER": "071",
    "DEPARTMENT OF INFORMATION": "858",
    "DEPARTMENT OF INVESTIGATIO": "032",
    "DEPARTMENT OF PARKS & RECR": "846",
    "DEPARTMENT OF PROBATION": "781",
    "DEPARTMENT OF SANITATION": "827",
    "DEPARTMENT OF TRANSPORTATI": "841",
    "DEPARTMENT OF VETERANS' SE": "063",
    "DEPARTMENT OF YOUTH AND CO": "261",
    "DEPT. OF RECORDS AND INFOR": "860",
    "DISTRICT ATTORNEY-BRONX CO": "902",
    "DISTRICT ATTORNEY-KINGS CO": "903",
    "DISTRICT ATTORNEY-NEW YORK": "901",
    "DISTRICT ATTORNEY-QUEENS C": "904",
    "DISTRICT ATTORNEY-RICHMOND": "905",
    "DISTRICT ATTORNEY - SPECIA": "906",
    "EQUAL EMPLOYMENT PRACTICES": "133",
    "FINANCIAL INFORMATION SERV": "127",
    "FIRE DEPARTMENT": "057",
    "HOUSING PRESERVATION & DEV": "806",
    "HRA/DEPARTMENT OF SOCIAL S": "069",
    "INDEPENDENT BUDGET OFFICE": "132",
    "LANDMARKS PRESERVATION COM": "136",
    "LAW DEPARTMENT": "025",
    "MAYOR'S OFFICE OF CONTRACT": "082",
    "MUNICIPAL WATER FINANCE AU": "185",
    "NEW YORK CITY FIRE PENSION": "257",
    "NYC EMPLOYEES' RETIREMENT": "009",
    "N.Y.C. HOUSING AUTHORITY": "996",
    "NYC POLICE PENSION FUND": "256",
    "N.Y.C. TRANSIT AUTHORITY": "998",
    "OFFICE OF ADMINISTRATIVE T": "820",
    "OFFICE OF COLLECTIVE BARGA": "313",
    "OFFICE OF EMERGENCY MANAGE": "017",
    "OFFICE OF LABOR RELATIONS": "214",
    "OFFICE OF MANAGEMENT AND B": "019",
    "OFFICE OF PAYROLL ADMINIST": "131",
    "OFFICE OF THE ACTUARY": "008",
    "OFFICE OF THE COMPTROLLER": "015",
    "OFFICE OF THE MAYOR": "002",
    "POLICE DEPARTMENT": "056",
    "PUBLIC ADMINISTRATOR BRONX": "942",
    "PUBLIC ADMINISTRATOR KINGS": "943",
    "PUBLIC ADMINISTRATOR NEW Y": "941",
    "PUBLIC ADMINISTRATOR QUEEN": "944",
    "PUBLIC ADMINISTRATOR RICHM": "945",
    "PUBLIC ADVOCATE": "101",
    "TAX COMMISSION": "021",
    "TAXI AND LIMOUSINE COMMISS": "156",
    "TEACHERS' RETIREMENT SYSTE": "041",
    "TRIBOROUGH BRIDGE AND TUNN": "993"
}
#agency_codes={"ADMINISTRATION FOR CHILDRE": "067"}
run_scrape(code_jsonfile,agency_codes,linkSrchTemplate,joblinkBase)


final_time=round(time.time()-start_time,2)
print("------")
print("Time to execute:{time}".format(time=final_time))
print("------")