
from sqlalchemy import create_engine
import pandas as pd


credential = 'postgres://youname:yourpwd@ip_adress:5432/name_db'


# define the string for postgres
engine = create_engine(credential)


# # load the data related to the anemity
print('load anemity data')
path_anemity = '../data/anemities.csv'
data_frame_anemity = pd.read_csv(path_anemity,header=0,sep=',',index_col=None)
print(data_frame_anemity.head(5))
# # write on postgres
data_frame_anemity.to_sql('anemity', engine,schema='poi',if_exists='append',index=False)
print('done')
