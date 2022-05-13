import pymssql
import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
from config import database, user, password, server


def prepare_data():
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()
    
    table_list = ['median_income', 'house_prices']
    prepared_data = {}
    for table in table_list:
        
        query = f'SELECT * FROM {table}'
        
        prepared_df = pd.read_sql(query, conn)
        print(f'Queried dbo.{table}')
        print(f'\nBefore Data Management: {prepared_df.shape[0]}')
        
        # Send to data transformation function based on what the data is
        if table == 'median_income':
            prepared_df = prepare_income_data(prepared_df)
        elif table == 'house_prices':
            prepared_df = prepare_house_price_data(prepared_df).head(10000)
        
        print(f'After Data Management: {prepared_df.shape[0]}\n')
        prepared_data[table] = prepared_df
        print(f'Finished {table}: Processed {len(prepared_df)} records')
    return prepared_data

def prepare_house_price_data(df):
    df.sort_values(by = 'timestamp', inplace = True)
    df.reset_index(drop = True, inplace = True)
    df.reset_index(inplace = True)
    df.rename(columns = {'index': 'record_count'}, inplace = True)
    df['timestamp'] = df['timestamp'].apply(
        lambda x: dt.datetime.fromtimestamp(x/1000)
    )
    return df

def prepare_income_data(income_df):
    income_df = income_df[(income_df['AgeGroup'] == 'overall')]
    return income_df.head(1000)

def prepare_source_three():
    pass

def prepare_source_four():
    pass