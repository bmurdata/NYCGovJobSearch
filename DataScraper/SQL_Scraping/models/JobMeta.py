# Job Meta Class
from db import sa, Base

# Job Details and Meta- work location, etc.
class JobMeta_Model(Base):
    __tablename__='job_info_short'

    jobNum = sa.Column(sa.Integer, primary_key=True)
    hiring_agency=sa.Column(sa.String(200))
    jobLink=sa.Column(sa.String(2083))
    job_ID=sa.Column(sa.Integer)
    business_title=sa.Column(sa.String(500))
    civil_title=sa.Column(sa.String(200))
    title_class=sa.Column(sa.String(100))
    job_category=sa.Column(sa.String(200))
    career_level=sa.Column(sa.String(100))
    work_location=sa.Column(sa.String(300))
    division_work_unit=sa.Column(sa.String(300))
    total_openings=sa.Column(sa.Integer)
    title_code=sa.Column(sa.String(100))
    level=sa.Column(sa.String(20))
    proposed_salary_range=sa.Column(sa.String(200))
    posted=sa.Column(sa.DateTime)
    post_until=sa.Column(sa.DateTime)

# Full job descriptions
class JobDescrip_Model(Base):
    __tablename__='job_info_details'

    add_info=sa.Column(sa.Text)
    hours_shift=sa.Column(sa.String(200))
    job_descrip=sa.Column(sa.Text)
    min_qual=sa.Column(sa.Text)
    preferred_skills=sa.Column(sa.Text)
    recruit_contact=sa.Column(sa.String(500))
    residency_req=sa.Column(sa.Text)
    to_apply=sa.Column(sa.Text)
    work_location=sa.Column(sa.Text)
    jobNum=sa.Column(sa.Integer,primary_key=True)

# Search by agency codes
class AgencySearch_Model(Base):
    __tablename__='search_by_agencycode'

    jobNum=sa.Column(sa.Integer,primary_key=True)
    Title=sa.Column(sa.String(300))
    Link=sa.Column(sa.String(2043))
    shortCategory=sa.Column(sa.String(100))
    LongCategory=sa.Column(sa.String(300))
    Department=sa.Column(sa.String(300))
    Location=sa.Column(sa.String(300))
    Agency=sa.Column(sa.String(300))
    Posted_Date=sa.Column(sa.DateTime)
