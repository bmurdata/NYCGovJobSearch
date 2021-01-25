import SQLAlchemy_Files.db
from SQLAlchemy_Files.db import engine
from sqlalchemy.orm import sessionmaker
from SQLAlchemy_Files.models.JobMeta import JobMeta_Model, AgencySearch_Model,JobDescrip_Model
from datetime import datetime,timedelta
from sqlalchemy import or_
Session = sessionmaker(bind=engine)
session=Session()

import json
import os
from pathlib import Path
dir_path=str(Path(os.path.dirname(os.path.realpath(__file__))).parents[0])+'/output/'

# joblinks must be a array of tuples- form of link, jobnum
# Compare to find new details, remove old ones, return link,jobID

# Compares database tables, assumes that Agency CSV and JSON files already in Agency table.
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
    today=datetime.today().strftime( '%Y-%m-%d')
    before_todayt=session.query(JobMeta_Model).filter(or_(JobMeta_Model.post_until < today,JobMeta_Model.job_ID==0)).all()
    for row in before_todayt:
        print(row.post_until)
    print("There are "+str(len(before_todayt)))
    oldJobs=[i[0] for i in session.query(JobMeta_Model.jobNum).filter(or_(JobMeta_Model.post_until < today,JobMeta_Model.job_ID==0)).all()]
    print("There are "+str(len(oldJobs))+" In the Database to be deleted")
    session.query(JobMeta_Model).filter(or_(JobMeta_Model.post_until < today,JobMeta_Model.job_ID==0)).delete(synchronize_session="fetch")
    session.query(JobDescrip_Model).filter(JobDescrip_Model.jobNum.in_(oldJobs)).delete(synchronize_session="fetch")

    session.commit()
    for detail_id in details_jobNum:
        if detail_id in agency_jobNum:
            continue
        else:
            evilcount=evilcount+1
            x=[i for i in details_data if i[1]==detail_id]
            session.query(JobMeta_Model).filter(JobMeta_Model.job_ID==detail_id).delete(synchronize_session="fetch")
            session.query(JobDescrip_Model).filter(JobDescrip_Model.jobNum==detail_id).delete(synchronize_session="fetch")
            session.commit()
            details_data.remove(x[0])

    joblinks=agency_data
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
    return "This doesn't work. Intention is to compare old Details JSON or CSV files to newer Agency ones, however database takes priority."