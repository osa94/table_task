import pandas as pd
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class MaturityExam(Base):
    __tablename__ = 'maturity_exam'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)
    territory = Column(VARCHAR(20))
    took_or_passed = Column(VARCHAR(20))
    sex = Column(VARCHAR(10))
    year = Column(Integer)
    number_of_people = Column(Integer)

    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
    csv_file = 'data.csv'

    with open(csv_file, 'r') as content:
        content = ''.join([i for i in content]).replace(' ;', ';').replace("/", "_").replace(' ', '_')
        with open(csv_file, 'w') as new_content:
            new_content.writelines(content)

    df = pd.read_csv(csv_file, encoding='windows-1250', sep=';')
    df.to_sql(con=engine, index_label='id', name=__tablename__, if_exists='replace')



