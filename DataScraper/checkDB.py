import SQLAlchemy_Files.db
from SQLAlchemy_Files.db import engine
from sqlalchemy.orm import sessionmaker
from SQLAlchemy_Files.models.JobMeta import JobMeta_Model, AgencySearch_Model,JobDescrip_Model
from datetime import datetime,timedelta
from sqlalchemy import or_

import json
import os
from pathlib import Path
dir_path=str(Path(os.path.dirname(os.path.realpath(__file__))).parents[0])+'/output/'
Session = sessionmaker(bind=engine)
session=Session()
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
    session.close()

    return joblinks

# print(len(compareAgencyandMeta_DB()))
# print(compareAgencyandMeta_DB())

def writeMeta(data:dict()):
    # for category in data:
    #     print(category) [category]
    for job_dict in data:
        session.add(JobMeta_Model(
            jobNum=job_dict["jobNum"],
            hiring_agency=job_dict["HiringAgency"],
            jobLink=job_dict["jobLink"],
            job_ID=job_dict["Job ID"],
            business_title=job_dict["Business Title"],
            civil_title=job_dict["Civil Service Title"],
            title_class=job_dict["Title Classification"],
            job_category=job_dict["Job Category"],
            career_level=job_dict["Career Level"],
            work_location=job_dict["Work Location"],
            division_work_unit=job_dict["Division/Work Unit"],
            total_openings=job_dict["# of Positions"],
            title_code=job_dict["Title Code No"],
            level=job_dict["Level"],
            proposed_salary_range=job_dict["Proposed Salary Range"],
            posted=job_dict["POSTING DATE"],
            post_until=job_dict["POST UNTIL"],
        ))
    session.commit()
    


def writeDetails(data:dict()):


    for job_dict in data:
        session.add(JobDescrip_Model(
            add_info=job_dict["Additional Information"],
            hours_shift=job_dict["Hours/Shift"],
            job_descrip=job_dict["Job Description"],
            min_qual=job_dict["Minimum Qual Requirements"],
            preferred_skills=job_dict["Preferred Skills"],
            recruit_contact=job_dict["Recruitment Contact"],
            residency_req=job_dict["Residency Requirement"],
            to_apply=job_dict["To Apply"],
            work_location=job_dict["Work Location"],
            jobNum=job_dict["jobNum"],
        ))
    session.commit()