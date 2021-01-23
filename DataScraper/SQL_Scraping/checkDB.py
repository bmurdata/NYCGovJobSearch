import db
from db import engine
from sqlalchemy.orm import sessionmaker
from models.JobMeta import JobMeta_Model, AgencySearch_Model,JobDescrip_Model

Session = sessionmaker(bind=engine)
session=Session()

# Idea- Compare new JSON data to details database, where there is no match, scrape
# for the details. Where the post_until is before today's date- remove it
# from two tables if applicacble. Output: JSON file of new jobs

import json
import os
from pathlib import Path
dir_path=str(Path(os.path.dirname(os.path.realpath(__file__))).parents[0])+'/output/'

# joblinks must be a array of tuples- form of link, jobnum
# Compare to find new details, remove old ones, return link,jobID

def compareAgencyandMeta_DB():
    details_data=session.query(JobMeta_Model.jobLink,JobMeta_Model.jobNum).all()
    agency_data=session.query(AgencySearch_Model.Link,AgencySearch_Model.jobNum).all()

    print(len(details_data))
    print(len(agency_data))
    
    joblinks=[]
    counter=0
    evilcount=0
    details_jobNum=[i[1] for i in details_data]
    agency_jobNum=[i[1] for i in agency_data]
    print(len(agency_jobNum))
    # Check for new ones. 
    for agency_id in agency_jobNum:
        
        if agency_id in details_jobNum:
            agency_data=[job for job in agency_data if job[1]!=agency_id]
        else:
            
            # print(agency_id)
            counter=counter+1
    # Remove expired from the DB
    for detail_id in details_jobNum:
        if detail_id in agency_jobNum:
            continue
        else:
            evilcount=evilcount+1
            x=[i for i in details_data if i[1]==detail_id]
            print(x[0])
            details_data.remove(x[0])
    # Remove expired
    # for detail_id in details_data:
    #     if detail_id in agency_data:
    #         continue
    #     else:
    #         evilcount=evilcount+1
    #         details_data.remove(detail_id)
    joblinks=agency_data
    # Remove expired details
    print(counter)
    print(evilcount)
    print(len(details_data))
    return joblinks

print(len(compareAgencyandMeta_DB()))
# print(compareAgencyandMeta_DB())

def compareJsonToCsv_from_file(jsonfile):
    print(dir_path)
    test='2021-01-21_1611269606By-AgencyCode.json'

    with open(dir_path+test) as ifile:
        try:
            jobNumbers=[]
            jsondata=json.load(ifile)
            print("jsondata has a length of "+str(len(jsondata)))
            for category in jsondata:
                for job in jsondata[category]:
                    jobNumbers.append(job["jobNum"])
            failure=False

        except Exception as e:
            print("Failed to load the data reason: \n"+str(e))
            failure=True

# counter=0
# allJobNum=session.query(JobDescrip_Model.jobNum).filter(JobDescrip_Model.jobNum.in_((jobNumbers))).all()

# for row in session.query(JobDescrip_Model.jobNum).filter(JobDescrip_Model.jobNum.in_((jobNumbers))).all():
#     print(row.jobNum)
#     counter=counter+1

# print(str(counter))