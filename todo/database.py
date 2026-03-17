from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:JAbhi%403008$@localhost/TodoApplicationDB'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:JAbhi%403008$@127.0.0.1:3306/TodoApplicationDB'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()