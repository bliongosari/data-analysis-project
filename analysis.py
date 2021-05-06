import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

max_temp_df = pd.read_csv(
    'mean_maximum_temperature.csv', encoding='ISO-8859-1')
max_temp_df = pd.read_csv(
    'mean_minimum_temp.csv', encoding='ISO-8859-1')

sales_df = pd.read_csv('sales-per-month-edited.csv', sep=';')
online_sales_df = pd.read_csv('online-sales-per-month-edited.csv', sep=';')


sales_df = sales_df.drop([0,1,2,3,4,5,6,7,8], axis=0)
sales_df2 = sales_df.filter(regex='Victoria')

date = sales_df['Unnamed: 0'].copy().rename("Date")
sales_df2 = sales_df2.join(date)
# for key, value in sales_df2.iteritems():
#     print(key)
#     # get data of june 2013 - feb 2021
#     plt.scatter(sales_df2["Date"][-92:], sales_df2[key][-92:]);
#     plt.show()
#     # print(value)
#     # print()

online_sales_df = online_sales_df.drop([0,1,2,3,4,5,6,7,8], axis=0)
for key, value in online_sales_df.iteritems():
    print(key)
    # # get data of june 2013 - feb 2021
    plt.scatter(online_sales_df['Unnamed: 0'], online_sales_df[key]);
    plt.show()
    print(value)
    # print()