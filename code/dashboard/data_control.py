import time
import pymssql
import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
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


def run_predictions(X, y, degree):
    Input = [
        ("polynomial", PolynomialFeatures(degree=degree)),
        ("modal", LinearRegression()),
    ]

    pipe = Pipeline(Input)

    pipe.fit(X, y)

    poly_pred = pipe.predict(X)

    sorted_zip = sorted(zip(X["predictor"].tolist(), poly_pred))

    x_poly, poly_pred = zip(*sorted_zip)
    return pipe, x_poly, poly_pred, np.sqrt(mean_squared_error(y, poly_pred))


#### Below is where you can query the database and get data
#### Three examples are shown, the first is a generator that queries
#### a single time and then returns a subset of the data with each
#### callback. The second and third are standard functions that return data once.
def run_queries():
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

    all_df = [year_df, month_df, county_df, median_income_df, main_table]
    return all_df


def join_tables(all_df):
    year_df = all_df[0]
    month_df = all_df[1]
    county_df = all_df[2]
    median_income_df = all_df[3]
    main_table = all_df[4]

    master_table = pd.merge(
        main_table, year_df, left_on="YearID", right_on="YearID", how="outer"
    )
    print(master_table.shape[0])
    # Now has 5607 rows

    master_table = pd.merge(
        master_table, month_df, left_on="MonthID", right_on="MonthID", how="outer"
    )
    # Now has 5607 rows
    print(master_table.shape[0])

    master_table = pd.merge(
        master_table, county_df, left_on="FIPS", right_on="FIPS", how="outer"
    )
    # Now has 5607 rows
    print(master_table.shape[0])

    master_table = pd.merge(
        master_table,
        median_income_df,
        left_on=["FIPS", "YearID"],
        right_on=["FIPS", "YearID"],
        how="outer",
    )
    # Now has 20727 rows
    print(master_table.shape[0])
    return master_table


def get_and_hold_data():
    """ Ideally, this will preserve the data so that the database doesn't need to be called constantly."""
    start = time.perf_counter()
    all_data = run_queries()
    mark = time.perf_counter()
    print(f"\nQueries took {round(mark - start, 3)} seconds")

    master_table = join_tables(all_data)
    print(f"Table Joins took {round(time.perf_counter() - mark,3)} seconds\n")

    while True:
        yield master_table


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


def income_data_generator(current_state="OFF"):
    """ This is a generator."""

    print("Querying Income Data")
    query = "SELECT * FROM median_income"
    income_df = sql_query(query)
    year_df = sql_query("SELECT * FROM year")

    income_df = pd.merge(income_df, year_df, left_on="YearID", right_on="YearID")
    income_df = income_df.sort_values(by="MedianIncome", ascending=False)
    income_df.loc[(income_df.MedianIncome < 0), "MedianIncome"] = None

    years = income_df["Year"].unique().tolist()
    while True:
        filtered_years = []
        for year in sorted(years):
            filtered_years.append(year)
            filtered = income_df.copy()
            filtered.loc[(~filtered.Year.isin(filtered_years)), "MedianIncome"] = None
            filtered = filtered.sort_values(
                by=["Year", "MedianIncome"], ascending=[True, False]
            )
            yield income_df, filtered


def create_poly_models(master_table, target, locale):
    """ This function creates the models for the generator. """

    master_table["date"] = master_table.apply(
        lambda row: convert_to_date(row.Year, row.Month), axis=1
    )

    filtered = master_table[
        (master_table["AgeGroup"] == "25-44") & (master_table.FIPS == locale)
    ].copy()
    filtered.sort_values(by="date", inplace=True)

    if target == "MedianIncome":
        relevant = ["AgeGroup", "FIPS", "Year", "County", "MedianIncome", "date"]
        filtered.drop(
            columns=[_ for _ in filtered.columns if _ not in relevant], inplace=True
        )
        filtered.drop_duplicates(subset=relevant[:-1], inplace=True)

    filtered.reset_index(drop=True, inplace=True)
    filtered.reset_index(inplace=True)

    filtered.rename(columns={"index": "predictor"}, inplace=True)

    filtered.dropna(inplace=True)

    X = filtered[["predictor"]]
    y = filtered[[target]]

    results = {}
    models = []
    current_best = 100000
    print("Running Models...")
    cntr = 1
    for i in range(45, 1, -1):
        try:
            model, x_poly, poly_pred, rmse = run_predictions(X, y, i)
        except:
            break
        poly_pred = [_[0] for _ in poly_pred]
        result_df = pd.DataFrame(
            zip(x_poly, poly_pred), columns=["x_var", "predictions"]
        )
        model_results = [i, x_poly, poly_pred]
        results[rmse] = model_results
        model_results = [i, result_df, filtered[["predictor", target, "date"]].copy()]

        models.append(model_results)
        if rmse < current_best:
            current_best = rmse
            if i < 15:
                best_result = [rmse, cntr, i]
        # Do an else break here if you want to iterate normally and stop at the best.
        cntr += 1
    return models, best_result


def poly_generator():
    """ This generator returns model results to a visualization. """
    try:
        data_hold = get_and_hold_data()
    except Exception as E:
        print(E)
        print("DataHold is already created.")

    master_table = next(data_hold)

    current_target, current_locale = "MedianHousePrice", "34001"
    target, locale = current_target, current_locale

    target_change = False
    passed = False
    resp = None
    while not passed:
        print(f"The target is currently {current_target}")
        models, best_result = create_poly_models(master_table, target, locale)
        while True:
            print("Visual Activated")
            for i, item in enumerate(models):
                best = False
                if i == best_result[1]:
                    best = True
                try:
                    target, locale = yield item, best
                except Exception as E:
                    target, locale = yield item, best

                if target is None:
                    target, locale = current_target, current_locale
                else:
                    target_change, current_target, current_locale = check_result(
                        target, locale, current_target, current_locale
                    )

                if target_change:
                    break

            if target_change:
                print("Changing the targets", current_target, current_locale)
                target_change = False
                break


def check_result(target, locale, current_target, current_locale):
    target_change = False
    if target != current_target or locale != current_locale:
        target_change = True
        current_target = target
        current_locale = locale
    return target_change, current_target, current_locale
