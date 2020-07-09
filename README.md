# NYCGovJobSearch
A Python based data scrape of https://www1.nyc.gov/jobs/index.page to provide help those seeking a career in civil service.

# About

 This project provides a list of jobs from the NYC Jobs search site, grouped by category, agency, and more. In addition, it provides a direct link to jobs, something the website does not directly support. 
 
 In the main directory I have posted CSV files of the jobs by category, as well as agency code and name. Json files can be found in Datascraper folder, along with current project files.

 The main project script(jobCheck-json.py) currently outputs the jobs into a JSON format. If needed, a second script (readjson.py) converts it to CSV. Agency names were taken from [NYC Open Data Civil List](https://data.cityofnewyork.us/City-Government/Civil-List/ye3c-m4ga). 
 
 
# Installation and Setup

 Python 3.7 is required to run this project. You can do so from Python.org [here](https://www.python.org/downloads/). In addtion, make sure to have pip3 installed. 

 For dependency and environment management, this project uses [pipenv](https://pipenv-fork.readthedocs.io/en/latest/). A list of packages is in the next section.  
    To install pipenv:  
    pip install pipenv

   To install dependencies run:  
    pipenv install

   To activate the environment run:  
    pipenv shell

   From there you can jobCheck-json.py to generate a JSON file, and readjson.py to convert it to CSV. These are the preferred ways to get the data, and other methods provided in this repo will be updated afterwards.

   *NOTE:* A SQL Server Database setup script is provided. However, the jobCheck-json.py file will make no attempt to connect to it, and it is NOT required to run.
# Python packages used in the project
 ## In the Pipfile
   * scrapy- an initial attempt at webscraping. Not used as it could not be easily told to wait for the pages to load.
   * requests- part of the initial attempt. Unused.
   * selenium- the main web scraper component. Does so using Firefox web browser.
   * pyodbc- a module that provides connection to SQL Server. Unused outside of files that call dbtest.py.
 ## Other packages
   * json- used to read to JSON file and read to CSV.
   * time- used to track time of program execution.
   * re- unused but referenced.
   * requests- unused but referenced.

# Current Progress

   - Initial web scraping complete. 
   - Basic JSON and CSV files generated.
   - SQL Server connections made, HTML files can be made as well.
   - Pulled list of NYC agencies and agency codes from [NYC Open Data Civil List](https://data.cityofnewyork.us/City-Government/Civil-List/ye3c-m4ga) using Socrata API through SoQL, which borrows from SQL.
   - Scraped jobs sorted by agency and agency code, in addition to category

# Next Steps
   - Get more from scraped links. Posted date, posted until, etc.  
   - Follow links and get additional data- salary, number of positions, job id.
# Future
   - Clean up pipfile to remove packages not used in main files. Consider splitting them up.
   - Website to display information and provide searches, along with updates.
