from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#try:
    #conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Thechosen_1',
                            #cursor_factory=RealDictCursor)
    #cursor = conn.cursor()
    #print("connecting was successful")
#except:
    #print("connecting to database has failed.")