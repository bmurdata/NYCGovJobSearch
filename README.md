# NYCGovJobSearch
A Python based data scrape of https://www1.nyc.gov/jobs/index.page to provide help those seeking a career in civil service.

# About

 This project provides a list of jobs from the NYC Jobs search site, grouped by category, agency, and more. In addition, it provides a direct link to jobs, something the website does not directly support. 
 
 In the main directory there are copies of CSV generated when program was last run. Json files can be found in Datascraper folder, along with current project files. Original CSVs are also there as well.

 The main project script(jobCheck.py) outputs JSON and CSV files.By default, it scrapes the job search pages for information on jobs, including links. Optionally, job links can then be scraped(referred to as Job or joblink scrapes) to get more information, as well as full details.
 
 In addition, there is also a multithread version of scraping job link data, which is provided as an option for those who can take advantage of multiple threads. Once the job scrape is done, the command will automatically output the command to do this. This represents a large performance increase!

 Agency names were taken from [NYC Open Data Civil List](https://data.cityofnewyork.us/City-Government/Civil-List/ye3c-m4ga), by using the [SODA Api](https://dev.socrata.com/foundry/data.cityofnewyork.us/kpav-sd4t), which uses the SoQL SQL based query language.
 
 # Current Progress
   - Web scraping of search page, as well as following job links.  
   - Scraped jobs sorted by agency and agency code, in addition to category.
   - Outputs to CSV and JSON, accepting custom names in the command line.
   - Implemented multithreading for the job link scrape.
# Usage and Examples
## Help file
Run `python jobcheck.py -h` to get the following:  
```
usage: jobCheck.py [-h] [-afile AGENCYFILE] [-cfile CATEGORYFILE]  
                   [-jobout JOBOUTPUT] [-scrapelinks] [--nosearch]  
                   [-searchjson SEARCHJSONFILE]  

NYCGov Job site scraper. Outputs JSON and CSV files by job category and by
specific agency.  

optional arguments:  
  -h, --help            show this help message and exit  
  -afile AGENCYFILE, --agencyfile AGENCYFILE  
                        Agency JSON and CSV file names.  
  -cfile CATEGORYFILE, --categoryfile CATEGORYFILE  
                        Category JSON and CSV file names.  
  -jobout JOBOUTPUT, --joboutput JOBOUTPUT  
                        Job Link JSON and CSV output files.  
  -withlinks, --scrapejoblinks  
                        If set, runs scrape for all job links, after getting  
                        them from search. Defaults to false  
  --nosearch            If set, skips scrape for search pages, by category and  
                        code. Defaults to false  
  -searchjson SEARCHJSONFILE, --searchjsonfile SEARCHJSONFILE  
                        Job JSON file to use if --nosearch is set. Required  
                        with --nosearch  
```
## Examples
- To run job search scrape, with automatically generated prefix filenames of YYYY-MM-DD_TIME. 
- *Note* Will not scrape links by default.  
 ```python jobCheck.py```  
- Custom filenames can be specified as well  
 ```python jobCheck.py -afile AgencyFileName -cfile CategoryFileName```  
  Any unspecified options will be set to defaults.  
- To scrape joblinks after the search is scraped  
 ```python jobCheck.py -withlinks -jobout JobDetailsInfo```  
  *Note* jobout is optional name for files.  
- To run scrape of joblinks without scraping search  
 ```python jobCheck.py --nosearch -searchjson AgencyJSONFile -jobout JobOutputFileName```  

# Installation and Setup

 Python 3.7 is required to run this project. You can do so from Python.org [here](https://www.python.org/downloads/). In addtion, make sure to have pip3 installed, and the Selenium Webdriver for Python.
## Selenium setup- Firefox
By default, this project uses FireFox with Selenium Webdriver, and assumes you have a geckodriver. In the `scrapermodule.py`, you can set its location with the `gecko_Location` variable, if it is not on PATH or in the same directory.

If you want to use a different brower, modify the `scraperModule.py` fireFox_setup() function to use a different browser, and changes the options. As long as the function returns a browser object, you should be good! 

For more details on Selenium Drivers see [here](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/)
## Dependency and environment management
For dependency and environment management, this project uses [pipenv](https://pipenv-fork.readthedocs.io/en/latest/). A list of packages is in the next section.  
    To install pipenv:  
    pip install pipenv

   To install dependencies run:  
    pipenv install

   To activate the environment run:  
    pipenv shell

   From there you can jobCheck.py to generate a JSON file and CSV file. This is the preferred ways to get the data, and other methods provided in this repo will be updated afterwards.

   *NOTE:* A SQL Server Database setup script is provided. However, the jobCheck.py file will make no attempt to connect to it, and it is NOT required to run.
# Python packages used in the project
 ## In the Pipfile
   * selenium- the main web scraper component. Uses Firefox web browser.
   * pyodbc- a module that provides connection to SQL Server. Unused outside of files that call dbtest.py.  
 ## Other packages used

   * json- used to read to JSON file and read to CSV.
   * time- used to track time of program execution.
   * argparse- to parse command line arguments.

# Next Steps
   - Refinements as needed.  
   - Refine the Job link details JSON  
   - Update support for SQL Server.  
   - Create SQL output file. (low priority)
# Future
   - Website to display information and provide searches, along with updates.

