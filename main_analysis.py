import math
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.metrics.cluster import normalized_mutual_info_score

def get_correlation_with_sales(variable, sales_df, variable_name):
    variable = variable.transpose()
    variable = variable.iloc[2:-1]

    # make start year 1983
    cols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    variable = variable.drop(variable.columns[cols], axis=1)
    variable_changed_format = []
    count = 0
    # changing format from table like to column
    for i in variable:
        for j in variable[i]:
            if count % 13 != 0:
                variable_changed_format.append(j)
            count += 1

    # make max temp range months same as sales (Jan 1983 - Dec 2020)
    # remove all values of 2021
    variable_changed_format = variable_changed_format[:-12]
    sales_df[variable_name] = variable_changed_format

    # changing commas to dot
    sales_df = sales_df.replace(to_replace= r',', value='.', regex=True)

    # change format from object to numeric
    keys = sales_df.columns[sales_df.dtypes.eq('object')]
    sales_df[keys[:-1]] = sales_df[keys[:-1]].apply(pd.to_numeric, errors='coerce', axis=1)
    year = sales_df['Date'].str[4:]

    year = year.apply(pd.to_numeric, errors = 'coerce')
    sales_df["year"] = year

    year_start = 1983
    year_end = 2020
    current_year = year_start
    inflation_price = []

    # add value of 100 dollars in that year for inflation adjustment
    while current_year <= year_end:
        value_of_100_in_year = inflation.loc[inflation['year'] == current_year]
        inflation_price.extend([value_of_100_in_year['amount'].values[0] for i in range(12)])
        current_year += 1

    sales_df["inflation_price"] = inflation_price
    base_value = inflation.loc[inflation['year'] == year_start]['amount'].values[0]
    sales_df["multiplier"] = sales_df["inflation_price"]/base_value

    # adjust for inflation
    for key in keys[:-1]:
        sales_df[key] = sales_df[key]/sales_df['multiplier']

    # removing outliers
    sales_df = sales_df.iloc[:, :-3];
    objects = sales_df.columns[sales_df.dtypes.eq('object')]
    sales_df = sales_df.drop(objects, axis = 1)
    # remove when z index > 3
    sales_df = sales_df[(np.abs(stats.zscore(sales_df)) < 3).all(axis=1)]
    variable = sales_df[variable_name]

    # sturge's rule of binning
    bins = 1 + math.log(len(sales_df), 2)

    for key in keys[:-1]:
        # get pearson correlation
        r_value = str(variable.corr(sales_df[key]))
        plt.scatter(variable, sales_df[key])
        variable2 = pd.cut(variable, bins=round(bins))
        sales_df[key] = pd.cut(sales_df[key], bins=round(bins))

        # get normalized mutual info
        mi = normalized_mutual_info_score(variable2, sales_df[key])

        plt.xlabel(variable_name)
        plt.ylabel(key[24:-2])
        plt.title(key[24:-2] + " vs " + variable_name + "\nCorrelation = " + r_value + "\n" + "MI = " + str(mi), fontsize = 10)
        # plt.savefig(key[24:-2])
        plt.show()
        plt.clf()

if __name__ == '__main__':
    max_temp_monthly_original = pd.read_csv('monthly_max_temp.csv', encoding='ISO-8859-1')
    min_temp_monthly_original = pd.read_csv('monthly_min_temp.csv', encoding='ISO-8859-1')
    rainfall_monthly_original = pd.read_csv('monthly_rainfall.csv', encoding='ISO-8859-1')

    # sales_df = pd.read_csv('sales-per-month-edited.csv', sep=';')
    sales_df = pd.read_csv('seasonally-adjusted-sales.csv', sep=';')
    inflation = pd.read_csv('inflation_data.csv', encoding='ISO-8859-1')

    # original
    # sales_df = sales_df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 474, 475], axis=0)
    # adjusted sales
    sales_df = sales_df.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,474,475,476], axis=0)
    sales_df2 = sales_df.filter(regex='Victoria')

    # changed date tile, give it proper name
    date = sales_df['Unnamed: 0'].copy().rename("Date")
    sales_df2 = sales_df2.join(date)
    get_correlation_with_sales(max_temp_monthly_original, sales_df2, "max_temp")
    get_correlation_with_sales(min_temp_monthly_original, sales_df2, "min_temp")
    get_correlation_with_sales(rainfall_monthly_original, sales_df2, "rainfall")
