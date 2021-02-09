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

def writeMeta(data:list(dict())):
    # for category in data:
    #     print(category) [category]
    for job_dict in data:
        try:
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
        except Exception as e:
            continue
    session.commit()
    


def writeDetails(data:list(dict())):


    for job_dict in data:
        try:
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
        except Exception as e:
            continue
    session.commit()

def writeAgencyData(data:dict(),removePrev:bool):
    if removePrev==True:
        print("Deleting the table")
        session.query(AgencySearch_Model).delete()
        session.commit()
    for category in data:
        for job_dict in data[category]:
            session.add(AgencySearch_Model(
                jobNum=job_dict["jobNum"],
                Title=job_dict["title"],
                Link=job_dict["link"],
                shortCategory=job_dict["shortcategory"],
                LongCategory=job_dict["longcategory"],
                Department=job_dict["Department"],
                Location=job_dict["Location"],
                Agency=job_dict["Agency"],
                Posted_Date=job_dict["Posted_Date"],
            ))
    session.commit()

def testAndClear():
    # Cause I'm tired of writing on command line all the time
    agency_Data={
    "003": [],
    "011": [],
    "012": [],
    "010": [
        {
            "jobNum": "457063",
            "title": "Information Technology Manager",
            "link": "https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=457063&PostingSeq=1",
            "shortcategory": "010",
            "longcategory": "BOROUGH PRESIDENT-MANHATTA",
            "jobAttributes": "Information Technology Manager\nJob ID457063\nLocationMANHATTAN\nDepartmentAdministration\nAgencyPRESIDENT BOROUGH OF MANHATTAN\nPosted Date01/19/2021",
            "Department": "Administration",
            "Agency": "PRESIDENT BOROUGH OF MANHATTAN",
            "Location": "MANHATTAN",
            "Posted_Date": "2021-01-19"
        },
        {
            "jobNum": "456969",
            "title": "Intern/Volunteer Coordinator",
            "link": "https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=456969&PostingSeq=1",
            "shortcategory": "010",
            "longcategory": "BOROUGH PRESIDENT-MANHATTA",
            "jobAttributes": "Intern/Volunteer Coordinator\nJob ID456969\nLocationMANHATTAN\nDepartmentExecutive\nAgencyPRESIDENT BOROUGH OF MANHATTAN\nPosted Date01/16/2021",
            "Department": "Executive",
            "Agency": "PRESIDENT BOROUGH OF MANHATTAN",
            "Location": "MANHATTAN",
            "Posted_Date": "2021-01-16"
        }
    ],
    "831": [
        {
            "jobNum": "403522",
            "title": "Agency Attorney",
            "link": "https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=403522&PostingSeq=1",
            "shortcategory": "831",
            "longcategory": "BUSINESS INTEGRITY COMMISS",
            "jobAttributes": "Agency Attorney\nJob ID403522\nLocationMANHATTAN\nDepartmentDefault\nAgencyBUSINESS INTEGRITY COMMISSION\nPosted Date08/07/2019",
            "Department": "Default",
            "Agency": "BUSINESS INTEGRITY COMMISSION",
            "Location": "MANHATTAN",
            "Posted_Date": "2019-08-07"
        },
        {
            "jobNum": "403516",
            "title": "Executive Agency Counsel",
            "link": "https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=403516&PostingSeq=1",
            "shortcategory": "831",
            "longcategory": "BUSINESS INTEGRITY COMMISS",
            "jobAttributes": "Executive Agency Counsel\nJob ID403516\nLocationMANHATTAN\nDepartmentDefault\nAgencyBUSINESS INTEGRITY COMMISSION\nPosted Date08/07/2019",
            "Department": "Default",
            "Agency": "BUSINESS INTEGRITY COMMISSION",
            "Location": "MANHATTAN",
            "Posted_Date": "2019-08-07"
        },
        {
            "jobNum": "361229",
            "title": "Salesforce Specialist",
            "link": "https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=361229&PostingSeq=1",
            "shortcategory": "831",
            "longcategory": "BUSINESS INTEGRITY COMMISS",
            "jobAttributes": "Salesforce Specialist\nJob ID361229\nLocationMANHATTAN\nDepartmentDefault\nAgencyBUSINESS INTEGRITY COMMISSION\nPosted Date08/21/2018",
            "Department": "Default",
            "Agency": "BUSINESS INTEGRITY COMMISSION",
            "Location": "MANHATTAN",
            "Posted_Date": "2018-08-21"
        },
        {
            "jobNum": "357984",
            "title": "Computer Systems Manager",
            "link": "https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=357984&PostingSeq=1",
            "shortcategory": "831",
            "longcategory": "BUSINESS INTEGRITY COMMISS",
            "jobAttributes": "Computer Systems Manager\nJob ID357984\nLocationMANHATTAN\nDepartmentDefault\nAgencyBUSINESS INTEGRITY COMMISSION\nPosted Date08/08/2018",
            "Department": "Default",
            "Agency": "BUSINESS INTEGRITY COMMISSION",
            "Location": "MANHATTAN",
            "Posted_Date": "2018-08-08"
        }
    ]
    }
    meta_Data=[
    {
        "HiringAgency": "DEPT OF HEALTH/MENTAL HYGIENE",
        "jobLink": "https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=434514&PostingSeq=1",
        "jobNum": "434514",
        "Job ID": "434514",
        "Business Title": "Data Analyst, Bureau of HIV",
        "Civil Service Title": "CITY RESEARCH SCIENTIST",
        "Title Classification": "Non-Competitive",
        "Job Category": "Health, Policy, Research & Analysis",
        "Career Level": "Experienced (non-manager)",
        "Work Location": "42-09 28th Street",
        "Division/Work Unit": "Not Listed",
        "# of Positions": "1",
        "Title Code No": "21744",
        "Level": "02",
        "Proposed Salary Range": "$ 75,504.00 - $ 93,776.40 (Annual)",
        "POSTING DATE": "2020-03-18",
        "POST UNTIL": "2021-03-21"
    },
    {
        "HiringAgency": "DEPT OF HEALTH/MENTAL HYGIENE",
        "jobLink": "https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=437242&PostingSeq=1",
        "jobNum": "437242",
        "Job ID": "437242",
        "Business Title": "Data Analyst, Bureau of Immunization",
        "Civil Service Title": "CITY RESEARCH SCIENTIST",
        "Title Classification": "Non-Competitive",
        "Job Category": "Health, Policy, Research & Analysis",
        "Career Level": "Experienced (non-manager)",
        "Work Location": "42-09 28th Street",
        "Division/Work Unit": "Immunization Surveillance",
        "# of Positions": "1",
        "Title Code No": "21744",
        "Level": "02",
        "Proposed Salary Range": "$ 75,504.00 - $ 93,776.40 (Annual)",
        "POSTING DATE": "2020-12-08",
        "POST UNTIL": "2021-02-06"
    }]
    details_Data=[
    {
        "Additional Information": "**IMPORTANT NOTES TO ALL CANDIDATES:\n\nPlease note:\u00a0 If you are called for an interview you will be required to bring to your interview copies of original documentation, such as:\n\u2022 A document that establishes identity for employment eligibility, such as: A Valid U.S. Passport, Permanent Resident Card/Green Card, or Driver\u2019s license.\u00a0\n\n\u2022 Proof of Education according to the education requirements of the civil service title.\u00a0\n\n\u2022 Current Resume\u00a0\u00a0\n\n\u2022 Proof of Address/NYC Residency dated within the last 60 days, such as: Recent Utility Bill (i.e. Telephone, Cable, Mobile Phone)\n\nAdditional documentation may be required to evaluate your qualification as outlined in this posting\u2019s \u201cMinimum Qualification Requirements\u201d section. Examples of additional documentation may be, but not limited to: college transcript, experience verification or professional trade licenses.\n\nIf after your interview you are the selected candidate you will be contacted to schedule an on-boarding appointment.\u00a0\u00a0 By the time of this appointment you will be asked to produce the originals of the above documents along with your original Social Security card.\n\n**LOAN FORGIVENESS\n\nThe federal government provides student loan forgiveness through its Public Service Loan Forgiveness Program (PSLF) to all qualifying public service employees. Working with the DOHMH qualifies you as a public service employee and you may be able to take advantage of this program while working full-time and meeting the program\u2019s other requirements.\u00a0\n\nPlease visit the Public Service Loan Forgiveness Program site to view the eligibility requirements:\n\nhttps://studentaid.ed.gov/sa/repay-loans/forgiveness-cancellation/public-service\n\n\n\"FINAL APPOINTMENTS ARE SUBJECT TO OFFICE OF MANAGEMENT & BUDGET APPROVAL\u201d",
        "Hours/Shift": "Not listed",
        "Job Description": "The Research and Evaluation Unit in the HIV Prevention Program of the Bureau of HIV/AIDS Prevention and Control has an opening for a City Research Scientist II.\u00a0\u00a0\n\nUnder the supervision of the Senior Analyst, as part of a diverse team conducting a dynamic portfolio of high priority projects aimed to End the Epidemic of HIV in New York City.\n\nDUTIES WILL INCLUDE BUT NOT BE LIMITED TO:\n\n\u2022 Coordinate study operations for select high-impact HIV prevention research and evaluation projects, including CDC-funded cooperative agreements and demonstration projects.\n\n\u2022 Coordinate field-based operations, including venue engagement, staffing, protocol adherence, and ensuring participant confidentiality and data security.\n\n\u2022 Act as a lead analyst to clean, manage and analyze behavioral surveillance data utilizing more advanced coding to create automated reports to assess model fidelity and data quality and completeness; experience with SAS is essential.\n\n\u2022 Act as a lead analyst to analyze data in preparation of scheduled reports and presentations to internal and external stakeholders.\n\n\u2022 Fulfill Prevention Program and Bureau staff data requests accurately and in a timely fashion. Work closely with data requestors to ensure that data provided will accurately and thoroughly fulfill their needs.\n\n\u2022 Participate in the development and execution of evaluation plans and research protocols for HIV Prevention programs.\n\n\u2022 Prepare study protocol materials related to human subjects protections for IRB review at the NYC DOHMH.\n\n\u2022 Ensure and maintain study participant confidentiality and data security.\n\n\u2022 Lead and contribute to dissemination products including presentations and conference abstracts.",
        "Minimum Qual Requirements": "1.\u00a0 For Assignment Level I (only physical, biological and environmental sciences and public health) A master's degree from an accredited college or university with a specialization in an appropriate field of physical, biological or environmental science or in public health.\nTo be appointed to Assignment Level II and above, candidates must have:\n1. A doctorate degree from an accredited college or university with specialization in an appropriate field of physical, biological, environmental or social science and one year of full-time experience in a responsible supervisory, administrative or research capacity in the appropriate field of specialization; or\n2. A master's degree from an accredited college or university with specialization in an appropriate field of physical, biological, environmental or social science and three years of responsible full-time research experience in the appropriate field of specialization; or\n3. Education and/or experience which is equivalent to \"1\" or \"2\" above. However, all candidates must have at least a master's degree in an appropriate field of specialization and at least two years of experience described in \"2\" above. Two years as a City Research Scientist Level I can be substituted for the experience required in \"1\" and \"2\" above.\n\nNOTE:\nProbationary Period\nAppointments to this position are subject to a minimum probationary period of one year.",
        "Preferred Skills": "\u2022 A Master's degree or PhD form an accredited college or university with a specialization in epidemiology, statistics, public health or related field.\n\n\u2022 Strong project management skills are essential.\n\n\u2022 Experience and expertise in collecting, managing, cleaning, analyzing, and reporting on quantitative data, is essential.\n\n\u2022 Excellent analytical skills and reasoning with attention to detail.\n\n\u2022 Understanding of and appreciation for quality assurance and protocol adherence.\n\n\u2022 a firm grasp of the content area and specific concerns of HIV program evaluation.\n\n\u2022 Strong written and oral communication skills.\n\n\u2022 Outstanding working knowledge of SAS as well as Access and other MS Office software.\n\n\u2022 All Research and Evaluation staff members are expected to maintain multiple projects simultaneously and function effectively both independently and as part of a team.\n\n\u2022 Ability to work harmoniously as a member of a research and evaluation team and to interact effectively with research and evaluation team members.",
        "Recruitment Contact": "Not listed",
        "Residency Requirement": "New York City residency is generally required within 90 days of appointment. However, City Employees in certain titles who have worked for the City for 2 continuous years may also be eligible to reside in Nassau, Suffolk, Putnam, Westchester, Rockland, or Orange County. To determine if the residency requirement applies to you, please discuss with the agency representative at the time of interview.",
        "To Apply": "Apply online with a cover letter to https://a127-jobs.nyc.gov/.\u00a0 In the Job ID search bar, enter: job ID number # 434514.\n\nWe appreciate the interest and thank all applicants who apply, but only those candidates under consideration will be contacted.\n\nThe NYC Health Department is committed to recruiting and retaining a diverse and culturally responsive workforce. We strongly encourage people of color, people with disabilities, veterans, women, and lesbian, gay, bisexual, and transgender and gender non-conforming persons to apply.\n\nAll applicants will be considered without regard to actual or perceived race, color, national origin, religion, sexual orientation, marital or parental status, disability, sex, gender identity or expression, age, prior record of arrest; or any other basis prohibited by law.\n\nNOTE: This position is open to qualified persons with a disability who are eligible for the 55-a Program. Please indicate in your resume that you would like to be considered for the position under the 55-a Program.\n\n**LOAN FORGIVENESS\n\nThe federal government provides student loan forgiveness through its Public Service Loan Forgiveness Program (PSLF) to all qualifying public service employees. Working with the DOHMH qualifies you as a public service employee and you may be able to take advantage of this program while working full-time and meeting the program\u2019s other requirements.\u00a0\n\nPlease visit the Public Service Loan Forgiveness Program site to view the eligibility requirements:\n\nhttps://studentaid.ed.gov/sa/repay-loans/forgiveness-cancellation/public-service\n\n\n\"FINAL APPOINTMENTS ARE SUBJECT TO OFFICE OF MANAGEMENT & BUDGET APPROVAL\u201d",
        "Work Location": "Not listed",
        "jobNum": "434514"
    },
    {
        "Additional Information": "**IMPORTANT NOTES TO ALL CANDIDATES:\n\nPlease note:\u00a0 If you are called for an interview you will be required to bring to your interview copies of original documentation, such as:\n\u2022 A document that establishes identity for employment eligibility, such as: A Valid U.S. Passport, Permanent Resident Card/Green Card, or Driver\u2019s license.\u00a0\n\n\u2022 Proof of Education according to the education requirements of the civil service title.\u00a0\n\n\u2022 Current Resume\u00a0\u00a0\n\n\u2022 Proof of Address/NYC Residency dated within the last 60 days, such as: Recent Utility Bill (i.e. Telephone, Cable, Mobile Phone)\n\nAdditional documentation may be required to evaluate your qualification as outlined in this posting\u2019s \u201cMinimum Qualification Requirements\u201d section. Examples of additional documentation may be, but not limited to: college transcript, experience verification or professional trade licenses.\n\nIf after your interview you are the selected candidate you will be contacted to schedule an on-boarding appointment.\u00a0\u00a0 By the time of this appointment you will be asked to produce the originals of the above documents along with your original Social Security card.\n\n**LOAN FORGIVENESS\n\nThe federal government provides student loan forgiveness through its Public Service Loan Forgiveness Program (PSLF) to all qualifying public service employees. Working with the DOHMH qualifies you as a public service employee and you may be able to take advantage of this program while working full-time and meeting the program\u2019s other requirements.\u00a0\n\nPlease visit the Public Service Loan Forgiveness Program site to view the eligibility requirements:\n\nhttps://studentaid.ed.gov/sa/repay-loans/forgiveness-cancellation/public-service\n\n\n\"FINAL APPOINTMENTS ARE SUBJECT TO OFFICE OF MANAGEMENT & BUDGET APPROVAL\u201d",
        "Hours/Shift": "Not listed",
        "Job Description": "The mission of the Bureau of Immunization is to protect the health of all New Yorkers through the prevention and control of vaccine-preventable diseases (VPD). The School Compliance Unit, within the Bureau of Immunization, is responsible for monitoring and enforcing compliance with immunization requirements among children enrolled in schools and childcare centers in New York City. The Unit ensures compliance with immunization requirements for over 1.4 million school-aged children enrolled in approximately 5,000 public schools, non-public schools and childcare centers in NYC. The City Research Scientist II will be assigned the core activities of analyzing immunization compliance in schools and childcare centers.\n\nDUTIES WILL INCLUDE BUT NOT BE LIMITED TO:\n\n* Conduct analyses using epidemiologic and program evaluation methods.\n\n* Review program data, assuring data quality and summarizing data on school immunization compliance for the Unit, as well as internal and external partners.\n\n* Maintain and enhance the Unit's databases in Access and Maven.\n\n* Standardizing databases, merging records, cleaning data, and reconciling differences from various sources using SAS, SQL, and/or R.\n\n* Improve the Unit's data systems to optimize efficiency and usability.\n\n* Develop sampling strategies to determine representative sites for audit.\n\n* Review the Unit's protocols and procedures as it relates to data collection and compliance monitoring.\n\n* Update field staff on data collection protocols and procedures for school immunization compliance audits.\n\n* Supervise Unit's Administrative staff.\n\n* Assist with coordinating quarterly non-public school liaison meetings.\n\n* Provide written and/or oral summaries of analyses to Unit Chief and others, as directed.\n\n* Prepare abstracts for presentations at regional and national meetings.\n\n* Serve as Liaison between the Unit and program partners.\n\n* Assist with answering calls on the Unit's hotline.",
        "Minimum Qual Requirements": "1.\u00a0 For Assignment Level I (only physical, biological and environmental sciences and public health) A master's degree from an accredited college or university with a specialization in an appropriate field of physical, biological or environmental science or in public health.\nTo be appointed to Assignment Level II and above, candidates must have:\n1. A doctorate degree from an accredited college or university with specialization in an appropriate field of physical, biological, environmental or social science and one year of full-time experience in a responsible supervisory, administrative or research capacity in the appropriate field of specialization; or\n2. A master's degree from an accredited college or university with specialization in an appropriate field of physical, biological, environmental or social science and three years of responsible full-time research experience in the appropriate field of specialization; or\n3. Education and/or experience which is equivalent to \"1\" or \"2\" above. However, all candidates must have at least a master's degree in an appropriate field of specialization and at least two years of experience described in \"2\" above. Two years as a City Research Scientist Level I can be substituted for the experience required in \"1\" and \"2\" above.\n\nNOTE:\nProbationary Period\nAppointments to this position are subject to a minimum probationary period of one year.",
        "Preferred Skills": "- Strong experience managing, cleaning and analyzing datasets using SAS, SQL, and/or R software\n- Excellent computer skills, including proficiency in Microsoft Access, Excel, PowerPoint, and Word is strongly preferred\n- Excellent verbal, written, interpersonal, and organizational skills\n-Independence, initiative, and attention to detail\n- Ability to prioritize and handle multiple tasks efficiently\n- Flexibility to respond to changing priorities.",
        "Recruitment Contact": "Not listed",
        "Residency Requirement": "New York City residency is\u00a0 required within 90 days of appointment. However, city employees in certain titles who have worked for the City for 2 continuous years may also be eligible to reside in Nassau, Suffolk, Putnam, Westchester, Rockland, or Orange County. To determine if the residency requirement applies to you, please discuss with the agency representative at the time of interview.",
        "To Apply": "Apply online with a cover letter to https://a127-jobs.nyc.gov/.\u00a0 In the Job ID search bar, enter: job ID number # 437242.\n\nWe appreciate the interest and thank all applicants who apply, but only those candidates under consideration will be contacted.\n\nThe NYC Health Department is committed to recruiting and retaining a diverse and culturally responsive workforce. We strongly encourage people of color, people with disabilities, veterans, women, and lesbian, gay, bisexual, and transgender and gender non-conforming persons to apply.\n\nAll applicants will be considered without regard to actual or perceived race, color, national origin, religion, sexual orientation, marital or parental status, disability, sex, gender identity or expression, age, prior record of arrest; or any other basis prohibited by law.\n\nNOTE: This position is open to qualified persons with a disability who are eligible for the 55-a Program. Please indicate in your resume that you would like to be considered for the position under the 55-a Program.",
        "Work Location": "Not listed",
        "jobNum": "437242"
    }]
    writeAgencyData(agency_Data,True)
    writeMeta(meta_Data)
    writeDetails(details_Data)
