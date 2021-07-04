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
from datetime import date
import time
import json
import sys
import os
from scrapeargs import gecko_Location,jobLinkTemplate,agency_codes
# Selenium Setup
options = webdriver.ChromeOptions()
options.add_argument('-headless')





# Setup of browser
def Chrome_setup():
    try:
        browser=webdriver.Chrome(options=options)
        browser.set_page_load_timeout(90)
    except:
        print("Switching to use selpysettings with driver at: "+gecko_Location)
        try:
            
            browser = webdriver.Chrome(executable_path=gecko_Location,options=options)
            browser.set_page_load_timeout(90)

        except Exception as e:
            print("Webdriver not found. Either add it to PATH or to the geckodrivers folder. Alternatively, edit the scraperModule.py file gecko_Location variable.")
            print(e)
            exit()
    print("Browser setup and ready for use")
    return browser
brow=Chrome_setup()
brow.get('https://github.com/bmurdata')
txt=brow.find_element_by_tag_name('body')
print(txt.text)
brow.close()