# SQLAlchemy setup

import sqlalchemy as sa
import pymysql
connection_string="mysql+pymysql://root:root@localhost/nyc_gov_jobs"
engine = sa.create_engine(connection_string)

# Declare base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()