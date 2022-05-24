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
        
def income_vs_house_price():

    data_gen = data_getter.dispatcher()
    try:
        final_table = next(data_gen)
    except Exception as E:
        print("Data Control Error: 7E15")

    year_income = final_table[["Year", "MedianIncome"]].copy()
    year_income = year_income.groupby(by=["Year"]).agg("mean")
    year_income = year_income.reset_index()
    year_hp = final_table[["Year", "MedianHousePrice"]].copy()
    year_hp = year_hp.groupby(by=["Year"]).agg("mean")
    year_hp = year_hp.reset_index()
    year_income_hp = pd.merge(year_income, year_hp, on="Year", how="inner")
    year_income_hp.reset_index()

    while True:
        yield year_income_hp


# STATIC DATA RETURN
####################################################


def highest_median_income():
    data_gen = data_getter.dispatcher()
    master_df = next(data_gen)

    cols_to_keep = ["FIPS", "County", "Year", "MedianIncome", "AgeGroup"]
    filtered_df = master_df[cols_to_keep].copy()
    return





# ARIMA DISPATCHER
####################################################


def run_arima(master_df):

    target, params = yield "Started Arima"
    while True:

        filtered_data = arima.filter_data(master_df, target, params)
        adf_filtered_df, best_col, num_diffs, results = arima.get_adf(filtered_data, target)

        target, params = yield adf_filtered_df, results
        # graph_ready, export_ready = arima.dispatcher(master_df, target, params)
        # yield graph_ready, adf_filtered_df, 'arima'


# ARIMA FUNCTIONS
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

        old_path = "model_dump/old_model_dump" # Requires undifferencing
        new_path = "model_dump/"
        model_list = os.listdir(new_path)
        target_model = [
            _
            for _ in model_list
            if (target in _ and params[0] in _ and params[1] in _ and "train" in _)
        ][0]
        loaded_model = joblib.load(new_path + target_model)

        prediction_df = pd.DataFrame(loaded_model.forecast(10, alpha=0.05))
        prediction_df.reset_index(inplace=True)
        prediction_df.rename(columns={"index": "Year"}, inplace=True)
        prediction_df["Year"] = prediction_df["Year"].astype("str")

        filtered_df["Year"] = filtered_df["Year"].astype("str")

        combined_df = pd.merge(
            filtered_df, prediction_df, left_on="Year", right_on="Year", how="outer"
        )

        # combined_df["predicted_mean"] = combined_df["predicted_mean"].shift(-num_p)
        # ground_truth = combined_df[target].tolist()
        # predictions = combined_df["predicted_mean"].tolist()
        # new_items = []
        # breaker = False
        # for i, item in enumerate(predictions):
        #     if not breaker:
        #         ground = ground_truth[i]
        #         if str(item) == "nan":
        #             new_items.append(ground)
        #         else:
        #             breaker = True
        #             new_items.append(ground + item)
        #     else:
        #         try:
        #             new_items.append(new_items[-1] + item)
        #         except:
        #             pass
        # combined_df["full_results"] = new_items
        combined_df["full_results"] = combined_df["predicted_mean"]
        combined_df["full_results"].update(combined_df["MedianIncome"])
        combined_df["FIPS"] = fips
        combined_df["AgeGroup"] = age_group

        target, params = yield combined_df


# AFFORDABILITY CALCULATIONS
####################################################

def desparse_affordability(df):
    
    print(df)
    time.sleep(5)
    return


def calculate_affordability(master_df):
    
    while True:
        desparse_affordability(master_df)
    
    
    # reading in predictions
    path = "shapefiles/dat_cbo.csv"
    df = pd.read_csv(path)

    # Preparing
    #########################
    df["MedianIncome"].update(df["train_and_predicted"])
    cleaned_predictions = df[(df.Year > 2019) & (df.Year < 2023)].drop(
        columns=["train_and_predicted"]
    )
    cleaned_predictions["FIPS"] = cleaned_predictions["FIPS"].astype("str")

    # Calculating monthly income
    cleaned_predictions["MonthlyIncome"] = cleaned_predictions["MedianIncome"] / 12
    cleaned_predictions.drop(columns=["MedianIncome"], inplace=True)

    # Filtering master table to just the targeted data
    target_df = master_df[(master_df.Year > 2019) & (master_df.Year < 2023)]
    target_df = target_df[
        ["FIPS", "Year", 'Month', "AverageRate", "AveragePoints", "County", "MedianHousePrice"]
    ]

    # Merging predicting with actual
    merged_tables = pd.merge(
        cleaned_predictions,
        target_df,
        left_on=["Year", "FIPS"],
        right_on=["Year", "FIPS"],
        how="outer",
    )
    ##########################3
    # Finished filtering

    # Actual Calculator
    # down_payment started as .12, mort_inc_ratio started as .25, term started as 30, tax_rate started as .0189
    
    # TODO - We need to run the affordability calculation on all years, and not just the predicted
    # Then we can have a chart showing how affordability changed over time.
    # To do this, we may also need to use months somehow
    # it should be simple because we just keep the months when we merge in the data
    (
        down_payment,
        mort_inc_ratio,
        term,
        tax_rate,
        time_frame,
    ) = yield "Started Affordability Calculator"
    while True:
        final_table = merged_tables.copy()
        for row in final_table:
            P = final_table["MedianHousePrice"] - (
                final_table["MedianHousePrice"] * down_payment
            )
            r = final_table["AverageRate"] / 100
            t = term
            n = 12
            monthly_tax = (final_table["MedianHousePrice"] * tax_rate) / 12
            final_table["MonthlyMortgage"] = (
                P
                * (
                    ((r / n) * pow((1 + (r / n)), (n * t)))
                    / (pow((1 + r / n), (n * t)) - 1)
                )
            ) + monthly_tax

        # mortgage to income ratio
        final_table["mortgage_income_ratio"] = (
            final_table["MonthlyMortgage"] / final_table["MonthlyIncome"]
        )

        # affordability determination
        def affordable_condition(x):
            if x <= mort_inc_ratio:
                return "Yes"
            elif np.isnan(x):
                return "Missing"
            else:
                return "No"

        final_table["affordable"] = final_table["mortgage_income_ratio"].apply(
            affordable_condition
        )

        # Data Return Logic
        if time_frame == "monthly":
            final_table["MonthlyMortgage"] = final_table["MonthlyMortgage"].round(2)
            down_payment, mort_inc_ratio, term, tax_rate, time_frame = yield final_table
        else:
            final_annual_df = (
                final_table.groupby(by=["Year", "FIPS", "AgeGroup", "County"])[
                    ["MedianHousePrice", "MonthlyIncome", "MonthlyMortgage"]
                ]
                .agg("mean")
                .reset_index()
            )

            final_annual_df["mortgage_income_ratio"] = (
                final_annual_df["MonthlyMortgage"] / final_annual_df["MonthlyIncome"]
            )
            final_annual_df["affordable"] = final_annual_df[
                "mortgage_income_ratio"
            ].apply(affordable_condition)
            final_annual_df["MonthlyMortgage"] = final_annual_df[
                "MonthlyMortgage"
            ].round(2)
            (
                down_payment,
                mort_inc_ratio,
                term,
                tax_rate,
                time_frame,
            ) = yield final_annual_df
