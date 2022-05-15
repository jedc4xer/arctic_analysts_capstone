import pymssql
import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
from config import database, user, password, server


def sql_query(query):
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()
    queried_data = pd.read_sql(query, conn)
    return queried_data


#### Below is where you can query the database and get data
#### Two examples are shown, the first is a generator that queries
#### a single time and then returns a subset of the data with each
#### callback. The second is a standard function that returns data once.


def bpm_by_month_map_data(current_state="OFF"):
    """ This is a generator that will return a subset of the data each run. """

    print(current_state)
    query = "SELECT * FROM building_permits"
    bpm_by_month = sql_query(query)

    bpm_by_month.sort_values(by="Date", inplace=True)
    bpm_by_month["Date"] = bpm_by_month.Date.astype("str")
    filtered = bpm_by_month.Date.unique().tolist()
    for date in filtered:
        filtered_df = bpm_by_month[(bpm_by_month.Date == date)]
        print(f"bpm_by_month_generator: {date}")
        yield filtered_df


def income_data():
    """ This is a static call that will only return data once."""

    print("Querying Income Data")
    query = "SELECT * FROM median_income WHERE AgeGroup = 'overall'"
    income_df = sql_query(query)
    return income_df
