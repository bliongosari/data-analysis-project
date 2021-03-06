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
# for key in cols:
#     plt.scatter(grouped_sales['month'], grouped_sales[key]);
#     plt.title(key)
#     plt.ylabel(key)
#     plt.xlabel("month")
#     plt.show()

climate_data = climate_data.drop(['Annual', 'Number of Years', 'Start Year', 'End Year', 'Statistic Element'], axis=1)
mean_max_temp = pd.Series(climate_data.loc[0], name ="min_temp")
mean_min_temp = pd.Series(climate_data.loc[10], name ="max_temp")
mean_rainfall = pd.Series(climate_data.loc[23], name ="rainfall")

df = pd.concat([mean_max_temp, mean_min_temp, mean_rainfall], axis = 1)
df = df.reset_index()
grouped_sales = grouped_sales.reset_index()

result = pd.concat([grouped_sales, df], axis=1)
result = result.drop(['index', 'month'], axis = 1)

obj = result.columns[result.dtypes.eq('object')]
result[obj] = result[obj].apply(pd.to_numeric, errors='coerce', axis=1)

# change to max_temp or rainfall to test
variable = "min_temp"

# remove december (comment out if want to include outlier)
# result = result[:11]

result = result.sort_values(by=variable)
temp = result[variable]

for key in cols:
    r_value = str(temp.corr(result[key]))
    plt.scatter(result[variable], result[key]);
    plt.xlabel(variable)
    plt.ylabel(key)
    plt.title(key[24:-2] + " vs " + variable)
    plt.suptitle("Correlation = " + r_value)
    plt.savefig(key[24:-2])
    plt.clf()