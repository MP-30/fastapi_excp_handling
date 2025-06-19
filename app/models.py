from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text
from .database import Base



class curd_table(Base):
    __tablename__ = "curd_table"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable= False)
    address = Column(String, nullable=False)
    human = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    