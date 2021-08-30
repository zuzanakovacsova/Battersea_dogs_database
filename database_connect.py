from mysql.connector import MySQLConnection, Error
import pandas as pd
from sqlalchemy import create_engine 
import pymysql

from connection_config_dog import read_db_config

conn_string = read_db_config('connection_cred.cred')
engine = create_engine(conn_string)

current_dogs_df = pd.read_csv('/Projects/Battersea_dogs_database/Doggos.csv',header = 0)


#current_dogs_df.to_sql('dog_data_raw',con = engine,if_exists = 'fail')