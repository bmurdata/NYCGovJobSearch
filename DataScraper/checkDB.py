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
    fullDescription=[i[0] for i in session.query(JobDescrip_Model.jobNum).all()]
    # print(len(details_data))
    # print(len(agency_data))
    # print(len(fullDescription))

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
    # Remove expired from the Job Details
    today=datetime.today().strftime( '%Y-%m-%d')
    before_todayt=session.query(JobMeta_Model).filter(or_(JobMeta_Model.post_until < today,JobMeta_Model.job_ID==0)).all()
    # for row in before_todayt:
    #     print(row.post_until)
    #     print(row.job_ID)

    print("There are "+str(len(before_todayt)))
    oldJobs=[i[0] for i in session.query(JobMeta_Model.jobNum).filter(or_(JobMeta_Model.post_until < today,JobMeta_Model.job_ID==0)).all()]
    print("There are "+str(len(oldJobs))+" In the Database to be deleted")

    session.query(JobMeta_Model).filter(or_(JobMeta_Model.post_until < today,JobMeta_Model.job_ID==0)).delete(synchronize_session="fetch")
    session.query(JobDescrip_Model).filter(JobDescrip_Model.jobNum.in_(oldJobs)).delete(synchronize_session="fetch")

    session.commit()
    # Remove non matches from details
    for detail_id in details_jobNum:
        if detail_id in agency_jobNum:
            continue
        else:
            evilcount=evilcount+1
            session.query(JobMeta_Model).filter(JobMeta_Model.job_ID==detail_id).delete(synchronize_session="fetch")
            session.query(JobDescrip_Model).filter(JobDescrip_Model.jobNum==detail_id).delete(synchronize_session="fetch")
            session.commit()

    # Remove non matches from the Job Description
    descrip_count=0
    for descrip_id in fullDescription:
        if descrip_id in agency_jobNum:
            continue
        else:
            descrip_count=descrip_count+1
            session.query(JobDescrip_Model).filter(JobDescrip_Model.jobNum==descrip_id).delete(synchronize_session="fetch")
            session.commit()
    joblinks=agency_data
    # print(counter)
    # print(evilcount)
    print("There were this many job descriptions removed "+str(descrip_count))

    return joblinks

# print(len(compareAgencyandMeta_DB()))
# print(compareAgencyandMeta_DB())