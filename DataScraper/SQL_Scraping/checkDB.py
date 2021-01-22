import db
from db import engine
from sqlalchemy.orm import sessionmaker
from models.JobMeta import JobMeta_Model, AgencySearch_Model,JobDescrip_Model
# Job Meta Class
# class JobMeta(Base):
#     __tablename__='job_info_short'

#     jobNum = sa.Column(sa.Integer, primary_key=True)
#     hiring_agency=sa.Column(sa.String(200))
#     jobLink=sa.Column(sa.String(2083))
#     job_ID=sa.Column(sa.Integer)
#     business_title=sa.Column(sa.String(500))
#     civil_title=sa.Column(sa.String(200))
#     title_class=sa.Column(sa.String(100))
#     job_category=sa.Column(sa.String(200))
#     career_level=sa.Column(sa.String(100))
#     work_location=sa.Column(sa.String(300))
#     division_work_unit=sa.Column(sa.String(300))
#     total_openings=sa.Column(sa.Integer)
#     title_code=sa.Column(sa.String(100))
#     level=sa.Column(sa.String(20))
#     proposed_salary_range=sa.Column(sa.String(200))
#     posted=sa.Column(sa.DateTime)
#     post_until=sa.Column(sa.DateTime)

Session = sessionmaker(bind=engine)
session=Session()
for row in session.query(JobMeta_Model,JobMeta_Model.hiring_agency).all():
    print(row.JobMeta_Model.jobLink)

for row in session.query(JobDescrip_Model,JobDescrip_Model.jobNum).all():
    print(row.JobDescrip_Model.work_location)

for row in session.query(AgencySearch_Model,AgencySearch_Model.jobNum).all():
    print(row.AgencySearch_Model.shortCategory)  

# SUCCESSSSSSS WITH SQLALCHEMY!!!! Now to work on the actual checker

# Idea- Compare new JSON data to details database, where there is no match, scrape
# for the details. Where the post_until is before today's date- remove it
# from two tables if applicacble. Output: JSON file of new jobs

import json
import os
from pathlib import Path
dir_path=str(Path(os.path.dirname(os.path.realpath(__file__))).parents[0])+'/output/'
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
# jobNumbers=[457084,452082,456830]
finalcomplete=[]
print(len(jobNumbers))
counter=0
allJobNum=session.query(JobDescrip_Model.jobNum).filter(JobDescrip_Model.jobNum.in_((jobNumbers))).all()

for row in session.query(JobDescrip_Model.jobNum).filter(JobDescrip_Model.jobNum.in_((jobNumbers))).all():
    print(row.jobNum)
    counter=counter+1

print(str(counter))