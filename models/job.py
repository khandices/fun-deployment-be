from sqlalchemy import Column, Integer, String, Date, Boolean
from ..db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    date_applied = Column(Date, nullable=False)
    location_type = Column(String, nullable=False)
    referral = Column(Boolean, nullable=False)

    def to_dict(self):
        return  {col.name: getattr(self, col.name) for col in self.__table__.columns}