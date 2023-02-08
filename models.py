from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Audite(Base):
    __tablename__ = "audites"
    TrackingNo = Column(Integer, primary_key=True)
    Url = Column(String)
    Title = Column(String)
    Symbol = Column(String)
    PdfUrl = Column(String)
    CompanyName = Column(String)
    SentDateTime = Column(String)
    AttachmentUrl = Column(String)
    PublishDateTime = Column(String)
