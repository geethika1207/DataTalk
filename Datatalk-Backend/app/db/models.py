from sqlalchemy import Column, String, INTEGER, ForeignKey, JSON
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class USER(Base):
    __tablename__ = "Users"

    id = Column(INTEGER, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

class dataset(Base):
    __tablename__ = "Dataset"

    id = Column(INTEGER, primary_key = True)
    filepath = Column(String, unique=True, nullable = False)
    filename = Column(String,  nullable = False)
    title = Column(String, nullable = False)
    user_id = Column(INTEGER, ForeignKey("Users.id", ondelete = "CASCADE"), nullable = False)  
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    queries = relationship("Query")

class Query(Base):
    __tablename__ = "Question"

    id = Column(INTEGER, primary_key = True)
    question = Column(String, nullable = False)
    answer = Column(String, nullable = False)
    charts = Column(JSON, nullable = True)
    user_id = Column(INTEGER, ForeignKey("Users.id", ondelete = "CASCADE"), nullable = False)  
    dataset_id = Column(INTEGER, ForeignKey("Dataset.id", ondelete = "CASCADE"), nullable = False)  
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))