import pymssql
import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
from config import database, user, password, server


def prepare_iterative_data(target_table, n):
    
    if target_table == 'building_permits':
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()

        query = f"SELECT DISTINCT Date FROM building_permits"

        available_years_df = pd.read_sql(query, conn)
        available_years_df.sort_values(by = 'Date', inplace = True)
        available_dates = available_years_df.Date.astype('str').tolist()

        picked_date = available_dates[n]
        columns_to_select = 'Date, CountyFips, County, StateFips, [1_Unit]'
        query = f"SELECT {columns_to_select} FROM building_permits WHERE building_permits.Date = '{picked_date}'"
        target_df = pd.read_sql(query, conn)
        print(f'\nBefore Data Management: {available_years_df.shape[0]}')
        
    elif target_table == 'house_prices':
        
        pass
    
    return target_df
    
    
    
    
def prepare_data(n = False):
    
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()

    table_list = ["median_income", "house_prices"]
    prepared_data = {}
    for table in table_list:
        if table == "house_prices":
            query = f"SELECT * FROM {table} WHERE County LIKE '%Coconino%'"
        else:
            query = f"SELECT * FROM {table}"

        prepared_df = pd.read_sql(query, conn)
        print(f"Queried dbo.{table}: {prepared_df.shape[0]} records.")

        # Send to data transformation function based on what the data is
        if table == "median_income":
            prepared_df = prepare_income_data(prepared_df)
        elif table == "house_prices":
            prepared_df = prepare_house_price_data(prepared_df).head(100)

        print(f"After Data Management: {prepared_df.shape[0]}\n")
        prepared_data[table] = prepared_df
    return prepared_data


def prepare_house_price_data(df):
    df.sort_values(by="timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "record_count"}, inplace=True)
    df["timestamp"] = df["timestamp"].apply(
        lambda x: dt.datetime.fromtimestamp(x / 1000)
    )
    return df


def prepare_income_data(income_df):
    income_df = income_df[(income_df["AgeGroup"] == "overall")]
    return income_df.head(100)


def prepare_source_three():
    pass


def prepare_source_four():
    pass
