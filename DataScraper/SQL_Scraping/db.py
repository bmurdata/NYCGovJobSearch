# SQLAlchemy setup

import sqlalchemy as sa
import pymysql
connection_string=""
engine = sa.create_engine()

# Declare base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()