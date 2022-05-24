import joblib
import pandas as pd
from math import sqrt
import datetime as dt
from warnings import filterwarnings
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller
from sklearn.model_selection import train_test_split

filterwarnings('ignore')


# HELPER FUNCTIONS
########################################

def get_date_range(start_date, period_range, freq):
    
    start_date = dt.datetime.strptime(str(start_date), '%Y')
    date_list = (
        pd.date_range(start=start_date, periods=period_range + 1, freq=freq)
        .to_pydatetime()
        .tolist()
    )
    date_list = [
        str(_.year) for _ in date_list
    ]
    # date_list = [dt.datetime.strptime(f'{_.year}-{_.month}-15', '%Y-%m-%d') for _ in date_list]
    return date_list[1:]

def convert_to_date(year, month):
    date = dt.datetime.strptime(f"{year}-{month}", "%Y-%b")
    #date = dt.datetime.strftime(date, "%Y-%m-%d")
    return date



# DATA FILTERING
###########################################

def filter_data(df, which, args):
    if which == 'MedianIncome':
        fips, age_group = args
        cols_to_keep = ['FIPS','Year','MedianIncome', 'AgeGroup']
        drop_subset = 'Year' # This will be the value checked for dups
        
        df = df[(df.FIPS == fips) & (df.AgeGroup == age_group)]
    elif which == 'MedianHousePrice':
        fips = args[0]
        cols_to_keep = ['FIPS','Year','Month','MedianHousePrice']
        df = df[(df.FIPS == fips)]
        
    filtered_df = df[[_ for _ in cols_to_keep]].copy()
    filtered_df = filtered_df.dropna()
    
    if which == 'MedianIncome':
        filtered_df.drop_duplicates(subset = drop_subset, inplace = True)
    else:
        filtered_df.drop_duplicates(inplace = True)
    
    if which == 'MedianIncome':
        filtered_df['new_index'] = filtered_df.Year.copy()
        filtered_df['new_index'] = filtered_df['new_index'].apply(lambda x: dt.datetime.strptime(str(x), '%Y'))
        filtered_df.set_index('new_index', inplace = True)
        filtered_df.index = filtered_df.index.to_period('Y')
    else: 
        filtered_df["new_index"] = filtered_df.apply(
            lambda row: convert_to_date(row.Year, row.Month), axis=1
        )
        filtered_df.set_index('new_index', inplace = True)
        #raise ValueError("Did not set up for this dataset yet.")

    
        filtered_df.index = filtered_df.index.to_period('M')


    return filtered_df


# GRID SEARCH
#########################################

def evaluate_arima_model(X, arima_order):
    # prepare training dataset
    train_size = int(len(X) * 0.66)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit()
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    rmse = sqrt(mean_squared_error(test, predictions))
    return rmse

def evaluate_models(df, p_values, d_values, q_values):
    df = df.astype('float32')
    best_score, best_cfg = float("inf"), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
                try:
                    rmse = evaluate_arima_model(df, order)
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                        print('ARIMA%s RMSE=%.3f' % (order,rmse))
                except Exception as E:
                    print(E)
                    continue
    print('Best ARIMA%s RMSE=%.3f' % (best_cfg, best_score))
    return best_cfg


# AUGMENTED DICKEY-FULLER
####################################

def get_adf(df, target):
    df['diff_1'] = df[target].diff()
    df['diff_2'] = df[target].diff().diff()
    
    cols_to_check = [target, 'diff_1', 'diff_2']#,'diff_3']
    
    if target != 'MedianIncome':
        df['diff_12'] = df[target].diff(periods=12)
        cols_to_check = [target, 'diff_12']
    
    best_adf = 1000000000
    for i, col in enumerate(cols_to_check):
        adf_result = adfuller(df[col].dropna())
        if col == target:
            best_adf = adf_result[1]
        else:
            if adf_result[1] < best_adf:
                print(f'In the best result. Current Iteration: {i}, current_col: {col}')
                best_col = col
                best_adf = adf_result[1]
                num_diffs = i
                
             
        print(f'Column: {col} | ADF Statistic: {adf_result[0]} | P-Value: {adf_result[1]}')
    print("\n###############################################\n")
    print(f'Best Result: Column: {best_col} | ADF Statistic: {adf_result[0]}\nP-Value: {adf_result[1]} | Passed? {adf_result[1] <.05} | Num Diffs: {num_diffs}')
    print("\n###############################################\n")
    if best_col == 'diff_12':
        num_diffs = 12
    return df, best_col, num_diffs


# FINALIZATION
#####################################################

def finalize_results(completed_df, target):
    completed_df['converted'] = completed_df['predicted_mean']#.shift(num_diffs)

    copy_for_graph = completed_df.reset_index().copy()
    copy_for_graph.drop(columns = ['Year'], inplace = True)
    copy_for_graph.rename(columns = {'index': "Year"}, inplace = True)

    df_for_export = copy_for_graph.copy()
    df_for_export = df_for_export.drop(columns = ['diff_1','diff_2','predicted_mean','train_set','test_set'])
    df_for_export.rename(columns = {'converted': 'train_and_predicted'}, inplace = True)
    print('Run Completed. Dataframes Exported: "graph_ready", "export_ready"')
    return copy_for_graph, df_for_export


# ARIMA CONTROL FUNCTION (MAIN)
###########################################3

def control_arima(master_table, target, params):
    """ This function contains the meat of the ARIMA Method."""
    def ARIMA_predict(df, best_col, best_arima, num_periods, target, params):

        y_train, y_test = train_test_split(df[target].dropna(), train_size = .75, shuffle = False)
        model = ARIMA(y_train, order = best_arima)
        fitted = model.fit()
        file_name = f'model_dump/{target}_{params[0]}_{params[1]}_model_train.sav'
        joblib.dump(fitted, file_name)
        
        # Running this again because I actually want the predictions using the whole dataset
        # And the update methods weren't working.
        model = ARIMA(df[target].dropna(), order = best_arima)
        fitted = model.fit()        
        predictions = fitted.forecast(num_periods, alpha=0.05)

        file_name = f'model_dump/{target}_{params[0]}_{params[1]}_model_pred.sav'
        joblib.dump(fitted, file_name)
        
        

        return predictions, y_train, y_test
    
    # Get the filtered data
    filtered_df = filter_data(master_table, target, params)
    
    # Augmented Dickey-Fuller test
    adf_filtered_df, best_col, num_diffs = get_adf(filtered_df, target)
    
    print(adf_filtered_df.shape)
    
    print(f'Best Num Differences: {num_diffs}')
    # gridsearch for hyper parameters
    if target == 'MedianIncome':
        best_arima = evaluate_models(
            adf_filtered_df[best_col].dropna(),
            [0,1,2,3,4,5,6],
            [num_diffs],
            range(0,5)
        )
    else:
        best_arima = evaluate_models(
            adf_filtered_df[best_col].dropna(),
            [2,3,4,5],
            [num_diffs],
            range(1,3)
        )
    
    # Get Arima predictions
    if target == 'MedianIncome':
        prediction_periods = 10
    else:
        prediction_periods = int(filtered_df.shape[0] * .1)
    predictions, y_train, y_test = ARIMA_predict(
        filtered_df, best_col, best_arima, 10, target, params
    )

    # Convert returned predictions to dataframe
    predictions = predictions.reset_index().set_index('index')

    # Convert training set to dataframe
    train_set = y_train.reset_index().set_index('new_index')
    train_set.rename(columns = {target: 'train_set'}, inplace = True)

    # Convert testing set to dataframe
    test_set = y_test.reset_index().set_index('new_index')
    test_set.rename(columns = {target: 'test_set'}, inplace = True)

    # Combine testing and training and predictions (model results)
    model_result_df = pd.merge(predictions, train_set, left_index = True, right_index = True, how = 'outer')
    model_result_df = pd.merge(model_result_df, test_set, left_index = True, right_index = True, how = 'outer')

    # Combine filtered ground truth dataframe with model results
    completed_df = pd.merge(filtered_df, model_result_df, left_index = True, right_index = True, how = 'outer')
    
    return completed_df, num_diffs


def dispatcher(master_table, target, params):
    try:
        predicted_data, num_diffs = control_arima(master_table, target, params)
    except Exception as E:
        print(E)
        
    graph_ready, export_ready = finalize_results(predicted_data, target)
    return graph_ready, export_ready

