import os
import time
import joblib
import pymssql
import data_getter
import numpy as np
import pandas as pd
import datetime as dt
import arima_model as arima
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
    income_df = all_data[["Year", "FIPS", "County", "MedianIncome", "AgeGroup"]].copy()
    income_df.dropna(inplace=True)
    income_df.loc[(income_df.MedianIncome < 0), "MedianIncome"] = None
    income_df.drop_duplicates(inplace=True)

    years = income_df["Year"].unique().tolist()

    while True:
        filtered_years = []
        for year in sorted(years):
            filtered_years.append(year)
            filtered = income_df.copy()

            # Turning off the animation of this one because I don't have time
            # to synchronize with the other visuals.
            # filtered.loc[(~filtered.Year.isin(filtered_years)), "MedianIncome"] = None
            filtered = filtered.sort_values(
                by=["Year", "MedianIncome"], ascending=[True, False]
            )
            filtered.drop_duplicates(inplace=True)

            yield income_df, filtered


def home_price_data_generator(current_state="OFF"):
    """ This generator yields a year filtered dataframe to a figure on the analysis page."""

    data_gen = data_getter.dispatcher()
    all_data = next(data_gen)

    home_price_df = all_data[
        ["FIPS", "Year", "Month", "MonthID", "MedianHousePrice"]
    ].copy()
    home_price_df["Date"] = home_price_df.apply(
        lambda row: convert_to_date(row.Year, row.Month), axis=1
    )
    years = home_price_df["Year"].unique().tolist()
    while True:
        filtered_years = []
        for year in sorted(years):
            filtered_years.append(year)
            filtered = home_price_df.copy()
            filtered.loc[
                (~filtered.Year.isin(filtered_years)), "MedianHousePrice"
            ] = None
            filtered = filtered.sort_values(
                by=["Date", "MedianHousePrice"], ascending=[True, False]
            )
            yield home_price_df, filtered


def income_data():
    """ This generator returns data to analysis visuals. """

    data_gen = data_getter.dispatcher()
    master_df = next(data_gen)

    master_df = master_df[
        [
            "FIPS",
            "County",
            "Year",
            "MedianHousePrice",
            "MedianIncome",
            "AgeGroup",
            "Month",
        ]
    ]
    while True:
        yield master_df


# STATIC DATA RETURN
####################################################


def highest_median_income():
    data_gen = data_getter.dispatcher()
    master_df = next(data_gen)

    cols_to_keep = ["FIPS", "County", "Year", "MedianIncome", "AgeGroup"]
    filtered_df = master_df[cols_to_keep].copy()


# ARIMA DISPATCHER
####################################################


def run_arima(master_df):

    target, params = yield "Ready for Next"
    while True:

        filtered_data = arima.filter_data(master_df, target, params)
        adf_filtered_df, best_col, num_diffs = arima.get_adf(filtered_data, target)
        target, params = yield adf_filtered_df
        # graph_ready, export_ready = arima.dispatcher(master_df, target, params)
        # yield graph_ready, adf_filtered_df, 'arima'


# HELPER FUNCTIONS
####################################################


def get_model():
    num_p = 1
    data_gen = data_getter.dispatcher()
    master_df = next(data_gen)

    target, params = yield master_df
    while True:

        if target == "MedianIncome":
            fips, age_group = params
            cols_to_keep = ["FIPS", "Year", "MedianIncome", "AgeGroup"]
            filtered_df = master_df[
                (master_df["FIPS"] == fips) & (master_df.AgeGroup == age_group)
            ].copy()
            drop_subset = "Year"

        filtered_df = filtered_df[[_ for _ in cols_to_keep]].copy()
        filtered_df = filtered_df.dropna()
        filtered_df = filtered_df.drop_duplicates(subset=drop_subset)

        model_list = os.listdir("model_dump")
        target_model = [
            _ for _ in model_list if (target in _ and params[0] in _ and params[1] in _)
        ][0]
        loaded_model = joblib.load("model_dump/" + target_model)

        prediction_df = pd.DataFrame(loaded_model.forecast(10, alpha=0.05))
        prediction_df.reset_index(inplace=True)
        prediction_df.rename(columns={"index": "Year"}, inplace=True)
        prediction_df["Year"] = prediction_df["Year"].astype("str")

        filtered_df["Year"] = filtered_df["Year"].astype("str")

        combined_df = pd.merge(
            filtered_df, prediction_df, left_on="Year", right_on="Year", how="outer"
        )

        combined_df["predicted_mean"] = combined_df["predicted_mean"].shift(-num_p)
        ground_truth = combined_df[target].tolist()
        predictions = combined_df["predicted_mean"].tolist()
        new_items = []
        breaker = False
        for i, item in enumerate(predictions):
            if not breaker:
                ground = ground_truth[i]
                if str(item) == "nan":
                    new_items.append(ground)
                else:
                    breaker = True
                    new_items.append(ground + item)
            else:
                try:
                    new_items.append(new_items[-1] + item)
                except:
                    pass
        combined_df["full_results"] = new_items
        combined_df["FIPS"] = fips
        combined_df["AgeGroup"] = age_group
        target, params = yield combined_df


# HELPER FUNCTIONS
####################################################


# What counties have the highest median income on average

# In what locations is home ownership most and least - han
