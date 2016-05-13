import pandas as pd
import sqlalchemy
import config

engine = sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI)
olives = pd.read_csv('olive.csv')
olives.rename(columns={olives.columns[0]: 'area_main'}, inplace=True)
olives.area_main = olives.area_main.map(lambda x: x.split('.')[-1])
acid_list = list(olives.columns.values)[-8:]
regions = list(olives['area_main'].unique())
olives.to_sql('olives', engine)
