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
    salary = Column(Integer, nullable=True)
    poc = Column(String, nullable=True)
    recruiter_screen = Column(Date, nullable=True)
    interview_1 = Column(Date, nullable=True)
    interview_2 = Column(Date, nullable=True)
    interview_3 = Column(Date, nullable=True)
    interview_4 = Column(Date, nullable=True)
    rejection_date = Column(Date, nullable=True)
    offer_date = Column(Date, nullable=True)
    offer_amount = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)

    def to_dict(self):
        return  {col.name: getattr(self, col.name) for col in self.__table__.columns}