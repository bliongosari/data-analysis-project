import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

climate_data = pd.read_csv('climate-data.csv', encoding='ISO-8859-1')
sales_df = pd.read_csv('sales-per-month-edited.csv', sep=';')
online_sales_df = pd.read_csv('online-sales-per-month-edited.csv', sep=';')

sales_df = sales_df.drop([0,1,2,3,4,5,6,7,8], axis=0)
sales_df2 = sales_df.filter(regex='Victoria')

date = sales_df['Unnamed: 0'].copy().rename("Date")
sales_df2 = sales_df2.join(date)
month = sales_df2['Date'].str[0:3]

sales_df2.pop("Date")
sales_df2 = sales_df2.replace(to_replace=r',', value='.', regex=True)

cols = sales_df2.columns[sales_df2.dtypes.eq('object')]
sales_df2[cols] = sales_df2[cols].apply(pd.to_numeric, errors='coerce', axis=1)
sales_df2["month"] = month
grouped_sales = sales_df2.groupby(["month"]).mean().reset_index()
grouped_sales["month_int"] = pd.to_datetime(grouped_sales.month, format='%b', errors='coerce').dt.month
grouped_sales = grouped_sales.sort_values(by="month_int")
print(grouped_sales)
# for key in cols:
#     plt.scatter(grouped_sales['month'], grouped_sales[key]);
#     plt.title(key)
#     plt.ylabel(key)
#     plt.xlabel("month")
#     plt.show()

mean_max_temp = climate_data.loc[0]
mean_min_temp = climate_data.loc[10]
mean_rainfall = climate_data.loc[23]


# online_sales_df = online_sales_df.drop([0,1,2,3,4,5,6,7,8], axis=0)
# date = online_sales_df['Unnamed: 0'].copy().rename("Date")
# online_sales_df2 = online_sales_df.join(date)
# month = online_sales_df2['Date'].str[0:3]
#
# online_sales_df2.pop("Date")
# online_sales_df2.pop('Unnamed: 0')
# online_sales_df2 = online_sales_df2.replace(to_replace=r',', value='.', regex=True)
# cols2 = online_sales_df2.columns[online_sales_df2.dtypes.eq('object')]
# online_sales_df2[cols2] = online_sales_df2[cols2].apply(pd.to_numeric, errors='coerce', axis=1)
# online_sales_df2["month"] = month
# online_grouped_sales = online_sales_df2.groupby(["month"]).mean().reset_index()

# for key in cols2:
#     plt.scatter(online_grouped_sales['month'], online_grouped_sales[key]);
#     plt.title(key)
#     plt.ylabel(key)
#     plt.xlabel("month")
#     plt.show()
