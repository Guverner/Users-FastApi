from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from config import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Employee (Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key = True)
    username = Column(String, nullable = False)
    name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    status = Column(String, nullable = False)
    join_date  = Column(TIMESTAMP(timezone=True), nullable = False)
    salary = Column (Integer, nullable = False)

class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key = True)
    task_name = Column(String, nullable = False)
    task_content = Column(String, nullable = False)
    status = Column(Boolean ,server_default = 'False', nullable = False)
    createt_at  = Column(TIMESTAMP(timezone=True), nullable = False)
    owner_id = Column(Integer, ForeignKey("employee.id", ondelete= "CASCADE"), nullable = False)

