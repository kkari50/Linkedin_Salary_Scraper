import pyodbc
import pandas as pd
import xlrd
import sqlalchemy
import urllib
from input_details import *



#create table in database and write data to table:---!!

def database_handler(db_instance_name, db_name, db_table_name, data):

    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={db_instance_name};'
        f'DATABASE={db_name};'
        f'Trusted_Connection=Yes;'
    )

    conn.autocommit=True
    cursor=conn.cursor()

    q_use_db = f'USE {db_name}'
    cursor.execute(q_use_db)

    # if table doesn't exist in database create table:
    q_create_table = f"IF NOT Exists (select * from INFORMATION_SCHEMA.TABLES where TABLE_NAME= '{db_table_name}')" \
        f'CREATE TABLE {db_table_name} (' \
        f'Title varchar(max),' \
        f'Location varchar(max),' \
        f'Compensation varchar(100),' \
        f'Min_Comp varchar(100),' \
        f'Max_Comp varchar(100)' \
        f')'

    cursor.execute(q_create_table)

    params = urllib.parse.quote_plus(f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={db_instance_name};"
                                     f"DATABASE={db_name};"
                                     f"autocommit=True;"
                                     f"Trusted_Connection=Yes;")
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s"%params)


    data.to_sql(db_table_name, schema='dbo', con=engine, index=False, if_exists='append')

    print('Write to Database Successful..!!')



    cursor.close()
    conn.close()
