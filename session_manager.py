from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

'''DB Settings, and session'''

#engine = create_engine('mysql://{login}:{password}@localhost/{mysql-database}', echo=False)
engine = create_engine('mysql://root@localhost/core-data-prototype', echo=False)

Session = sessionmaker(bind=engine)
session = Session()