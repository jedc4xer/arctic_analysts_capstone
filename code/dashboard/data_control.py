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


def convert_to_date(year, month):
    date = dt.datetime.strptime(f"{year}-{month}-15", "%Y-%b-%d").date()
    date = dt.datetime.strftime(date, "%Y-%m-%d")
    return date


#### Below is where you can query the database and get data
#### Three examples are shown, the first is a generator that queries
#### a single time and then returns a subset of the data with each
#### callback. The second and third are standard functions that return data once.


def get_all_data():
    tables = ["year", "month", "county", "median_income", "main_table"]

    query = f"SELECT * FROM {tables[0]}"
    year_df = sql_query(query)

    query = f"SELECT * FROM {tables[1]}"
    month_df = sql_query(query)

    query = f"SELECT * FROM {tables[2]}"
    county_df = sql_query(query)

    query = f"SELECT * FROM {tables[3]}"
    median_income_df = sql_query(query)

    query = f"SELECT * FROM {tables[4]}"
    main_table = sql_query(query)

    master_table = pd.merge(
        main_table, year_df, left_on="YearID", right_on="YearID", how="inner"
    )
    # Now has 5607 rows

    master_table = pd.merge(
        master_table, month_df, left_on="MonthID", right_on="MonthID", how="inner"
    )
    # Now has 5607 rows

    master_table = pd.merge(
        master_table, county_df, left_on="FIPS", right_on="FIPS", how="inner"
    )
    # Now has 5607 rows

    master_table = pd.merge(
        master_table,
        median_income_df,
        left_on=["FIPS", "YearID"],
        right_on=["FIPS", "YearID"],
        how="inner",
    )
    # Now has 18900 rows

    # Drop unneeded
    master_table = master_table.drop(columns=["YearID", "MonthID"])

    return master_table


def bpm_by_month_map_data(current_state="OFF"):
    """ This is a generator that will return a subset of the data each run. """

    print(current_state)
    query = "SELECT * FROM building_permits WHERE FIPS LIKE '34%'"
    bpm_by_month = sql_query(query)

    bpm_by_month.sort_values(by="Date", inplace=True)
    bpm_by_month["Date"] = bpm_by_month.Date.astype("str")
    filtered = bpm_by_month.Date.unique().tolist()
    for date in filtered:
        filtered_df = bpm_by_month[(bpm_by_month.Date == date)]
        print(f"bpm_by_month_generator: {date}")
        yield filtered_df


def age_filtered_data(age_group=1):
    """ This is a static call that will return the whole range of data to the visualization builder."""

    age_groups = {1: "25-44"}

    master_df = get_all_data()

    filtered = master_df[(master_df["AgeGroup"] == age_groups[age_group])].copy()

    filtered["date"] = filtered.apply(
        lambda row: convert_to_date(row.Year, row.Month), axis=1
    )
    return filtered


def income_data():
    """ This is a static call that will only return data once."""

    print("Querying Income Data")
    query = "SELECT * FROM median_income"
    income_df = sql_query(query)
    year_df = sql_query("SELECT * FROM year")

    income_df = pd.merge(income_df, year_df, left_on="YearID", right_on="YearID")
    income_df = income_df.sort_values(by="MedianIncome", ascending=False)
    income_df.loc[(income_df.MedianIncome < 0), "MedianIncome"] = None
    return income_df
