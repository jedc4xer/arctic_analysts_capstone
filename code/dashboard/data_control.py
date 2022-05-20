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


# Helper Functions
##########################################


def convert_to_date(year, month):
    date = dt.datetime.strptime(f"{year}-{month}-15", "%Y-%b-%d").date()
    date = dt.datetime.strftime(date, "%Y-%m-%d")
    return date


def check_response(target, locale, current_target, current_locale):
    """ This function checks the response from the dashboard 
    for the model layout to see if anything has changed
    """
    target_change = False
    if target != current_target or locale != current_locale:
        target_change = True
        current_target = target
        current_locale = locale
    return target_change, current_target, current_locale


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


# Query Control
##########################################


def sql_query(query):
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()
    queried_data = pd.read_sql(query, conn)
    return queried_data


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


# Data Cleaning
##########################################


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

    master_table.loc[(master_table.MedianIncome < 0), "MedianIncome"] = None
    return master_table


def prepare_data_for_poly_models(master_table, target, locale, age_group):
    """ This function prepares the data for the poly models. 
    This is step 2 in the sequence after getting the data.
    """

    # Convert the month and year to a date for sorting
    master_table["date"] = master_table.apply(
        lambda row: convert_to_date(row.Year, row.Month), axis=1
    )

    # Filter the data for a specific age group and locale
    filtered = master_table[
        (master_table["AgeGroup"] == age_group) & (master_table.FIPS == locale)
    ].copy()

    filtered.sort_values(by="date", inplace=True)

    if target == "MedianIncome":
        relevant = ["AgeGroup", "FIPS", "Year", "County", "MedianIncome", "date"]
        filtered.drop(
            columns=[_ for _ in filtered.columns if _ not in relevant], inplace=True
        )
        filtered.drop_duplicates(subset=relevant[:-1], inplace=True)

    # Reset the index to be used as the predictor values
    filtered.reset_index(drop=True, inplace=True)
    filtered.reset_index(inplace=True)

    filtered.rename(columns={"index": "predictor"}, inplace=True)

    filtered.dropna(inplace=True)
    return filtered


# Data Management
##########################################


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


def create_poly_models(master_table, target, locale, age_group="25-44"):
    """ This function creates the models for the generator. 
    This function is called from the poly_generator which is called from the model layout page. 
    This is step 2 in the sequence after getting the data.
    """

    # Send the data to a function to filter it and prep it
    filtered = prepare_data_for_poly_models(master_table, target, locale, age_group)

    # Assign X and y
    X = filtered[["predictor"]]
    y = filtered[[target]]

    results = {}
    models = []
    current_best = 100000
    print("Running Models...")
    cntr = 1
    # best_result = None
    future_predictions = None
    # Step backwards through the degrees for visual impact
    for i in range(45, 1, -1):
        try:
            # Create and Run Models
            model, x_poly, poly_pred, rmse, future_predictions = create_and_run_models(
                X, y, i
            )
        except Exception as E:
            print("Exception in create_and_run_models", E)
            break

        poly_pred = [_[0] for _ in poly_pred]
        result_df = pd.DataFrame(
            zip(x_poly, poly_pred), columns=["x_var", "predictions"]
        )

        # Pack the results from the model (Degrees, predictors, predictions) into a list
        model_results = [i, x_poly, poly_pred]

        # Get the rmse from the model and store it in a dictionary
        results[rmse] = model_results

        # Get the filtered data set that was used for the model
        original_data = filtered[["predictor", target, "date"]].copy()

        # Repack the model_results
        model_results = [i, result_df, original_data, future_predictions]

        # Store model results for visualizations
        models.append(model_results)
        if rmse < current_best:
            current_best = rmse
            if i < 12:
                best_result = [rmse, cntr, i]
        # Do an else break here if you want to iterate normally and stop at the best.
        cntr += 1
    # Return the list of all models, and the best result to the
    return models, best_result


# Active Data Return Functions
##########################################


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


def poly_generator():
    """ This generator returns model results to a visualization. 
    This is the primary generator function that creates polynomial
    prediction models and then yields them to the dashboard.
    Steps:
    1. Get the data
    2. Prepare the data
    3. Model the data
    4. Preserve the results
    5. Return the data to the dashboard
    """

    # Step 1: Initiate the data hold
    # try:
    #     data_hold = get_and_hold_data()
    # except Exception as E:
    #     print(E)
    #     print("DataHold is already created.")

    # Step 2: Get the data from the data hold
    master_table = next(data_hold)

    # Step 3: Set preliminary variables
    current_target, current_locale = "MedianHousePrice", "34001"
    target, locale = current_target, current_locale

    target_change = False  # Has the targeted information changed?
    resp = None

    while True:
        print(f"The target is currently {current_target}")
        try:
            # This sends the data to be prepared, and then that function will send it
            # to be modeled.
            models, best_result = create_poly_models(master_table, target, locale)
        except Exception as E:
            print("Exception in create_poly_models.")
            print(E)

        while True:
            # Each model contains [i, result_df, original, future_predictions]
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
                    target_change, current_target, current_locale = check_response(
                        target, locale, current_target, current_locale
                    )

                if target_change:
                    break

            if target_change:
                print("Changing the targets", current_target, current_locale)
                target_change = False
                break


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


# Static Data Return Functions
##########################################


def income_data():
    """ This is a static call that will only return data once."""

    master_df = next(data_hold)
    master_df = master_df[
        ["FIPS", "Year", "MedianHousePrice", "MedianIncome", "AgeGroup", "Month"]
    ]

    return master_df


# Machine Learning
##########################################


def create_and_run_models(X, y, degree):
    """ This function creates and fits the regression model to the data.
    This is step 4 of the sequence:
    1. Get the data
    2. Filter the data
    3. Starting the model creation master generator """
    Input = [
        ("polynomial", PolynomialFeatures(degree=degree)),
        ("modal", LinearRegression()),
    ]

    pipe = Pipeline(Input)

    pipe.fit(X, y)

    poly_pred = pipe.predict(X)
    range_max = X.iloc[:, 0].max()

    future_range = range(range_max + 1, int((X.shape[0]) * 1.15))
    future_X = pd.DataFrame(future_range, columns=["predictor"])

    try:
        future_predictions = model_predictions(pipe, future_X)
        future_predictions = [_[0] for _ in future_predictions]

        # print(type(future_predictions))
        # X = pd.concat([X, future_X])
        # poly_pred = np.concatenate([poly_pred, future_predictions])
    except Exception as E:
        print("run_predictions Exception")
        print(E)

    try:
        future_predictions = pd.DataFrame(
            zip(future_X["predictor"].tolist(), future_predictions),
            columns=["predictor", "futures"],
        )
    except Exception as E:
        print(E)

    # try:
    #     futures_predictions = pd.merge(future_X, future_predictions, left_index = True, right_index = True)
    # except Exception as E:
    #     print('Future Prediction Merge Exception', E)

    sorted_zip = sorted(zip(X["predictor"].tolist(), poly_pred))

    x_poly, poly_pred = zip(*sorted_zip)
    return (
        pipe,
        x_poly,
        poly_pred,
        np.sqrt(mean_squared_error(y, poly_pred)),
        future_predictions,
    )


# ML Predictions
##########################################


def model_predictions(model, future_steps):
    future_pred = model.predict(future_steps)
    return future_pred


# Activate Data Hold
###################################

try:
    data_hold = get_and_hold_data()
    print("Data Hold Started")
except Exception as E:
    pass


# Possible Trash
##########################################


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


# def age_filtered_data(age_group=1):
#     """ This is a static call that will return the whole range of data to the visualization builder."""

#     age_groups = {1: "25-44"}

#     master_df = next(data_hold)

#     filtered = master_df[(master_df["AgeGroup"] == age_groups[age_group])].copy()

#     filtered["date"] = filtered.apply(
#         lambda row: convert_to_date(row.Year, row.Month), axis=1
#     )
#     return filtered
