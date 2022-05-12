import pymssql
import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
from config import database, user, password, server


def prepare_data():
    return
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()
    
    table_list = []
    prepared_data = {}
    for table in table_list:
        query = f'SELECT * FROM {table}'
        print('Queried the data')
        
        capstone_df = pd.read_sql(query, conn)
        print(f'\nBefore Data Management: {capstone_df.shape[0]}')
        
        # Send to data transformation function based on what the data is
        
        print(f'After Data Management: {capstone_df.shape[0]}\n')
        #prepared_data[table] = prepared_df
    return prepared_data

def prepare_source_one():
    pass

def prepare_source_two():
    pass

def prepare_source_three():
    pass

def prepare_source_four():
    pass