import time
import pymssql
import data_getter
import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from config import database, user, password, server


# HELPER FUNCTIONS
####################################################

def convert_to_date(year, month):
    date = dt.datetime.strptime(f"{year}-{month}-15", "%Y-%b-%d").date()
    date = dt.datetime.strftime(date, "%Y-%m-%d")
    return date


def get_date_range(start_date, period_range, freq):

    date_list = (
        pd.date_range(start=start_date, periods=period_range + 1, freq=freq)
        .to_pydatetime()
        .tolist()
    )

    date_list = [
        str(_.year) + "-" + str(_.month).zfill(2) + "-" + "15" for _ in date_list
    ]
    # date_list = [dt.datetime.strptime(f'{_.year}-{_.month}-15', '%Y-%m-%d') for _ in date_list]
    return date_list[1:]


# DATA GENERATORS
####################################################

def income_data_generator(current_state="OFF"):
    """ This is a generator."""

    data_gen = data_getter.dispatcher()
    try:
        all_data = next(data_gen)
    except Exception as E:
        print(E)
    income_df = all_data[['Year', 'FIPS','MedianIncome','AgeGroup']].copy()
    income_df.dropna(inplace = True)
    income_df.loc[(income_df.MedianIncome < 0), "MedianIncome"] = None
    income_df.drop_duplicates(inplace = True)
    
    years = income_df["Year"].unique().tolist()
    
    while True:
        filtered_years = []
        for year in sorted(years):
            filtered_years.append(year)
            filtered = income_df.copy()
            
            # Turning off the animation of this one because I don't have time 
            # to synchronize with the other visuals.
            #filtered.loc[(~filtered.Year.isin(filtered_years)), "MedianIncome"] = None
            filtered = filtered.sort_values(
                by=["Year", "MedianIncome"], ascending=[True, False]
            )
            filtered.drop_duplicates(inplace = True)

            yield income_df, filtered

def home_price_data_generator(current_state="OFF"):
    """ This generator yields a year filtered dataframe to a figure on the analysis page."""

    data_gen = data_getter.dispatcher()
    all_data = next(data_gen)

    home_price_df = all_data[['FIPS','Year','Month','MonthID','MedianHousePrice']].copy()
    home_price_df['Date'] = home_price_df.apply(lambda row: convert_to_date(row.Year, row.Month), axis = 1)
    years = home_price_df["Year"].unique().tolist()
    while True:
        filtered_years = []
        for year in sorted(years):
            filtered_years.append(year)
            filtered = home_price_df.copy()
            filtered.loc[(~filtered.Year.isin(filtered_years)), "MedianHousePrice"] = None
            filtered = filtered.sort_values(
                by=["Date", "MedianHousePrice"], ascending=[True, False]
            )
            yield home_price_df, filtered
            

def income_data():
    """ This is a static call that will only return data once."""

    data_gen = data_getter.dispatcher()
    master_df = next(data_gen)
    
    master_df = master_df[
        ["FIPS", 'County', "Year", "MedianHousePrice", "MedianIncome", "AgeGroup", "Month"]
    ]
    while True:
        yield master_df
            

# STATIC DATA RETURN
####################################################




# HELPER FUNCTIONS
####################################################




# HELPER FUNCTIONS
####################################################