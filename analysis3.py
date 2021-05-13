import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

climate_data = pd.read_csv('climate-data.csv', encoding='ISO-8859-1')
climate_data = climate_data.drop(['Annual', 'Number of Years', 'Start Year', 'End Year'], axis=1)
mean_max_temp = pd.Series(climate_data.loc[0], name ="min_temp")
mean_min_temp = pd.Series(climate_data.loc[10], name ="max_temp")
mean_rainfall = pd.Series(climate_data.loc[23], name ="rainfall")

mean_max_temp = pd.to_numeric(mean_max_temp[1:], errors='coerce')

plt.scatter(mean_max_temp.index, mean_max_temp)

plt.show()