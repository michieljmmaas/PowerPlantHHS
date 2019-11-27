"""get data from wind turbines and do data science"""

import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

data_folder = 'training_data'
files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))]

data = pd.DataFrame(columns=['lat', 'lon', 'power per turbine'])

for file in files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_excel(file_path)
    df_2018 = df[df.Year == 2018]
    if len(df_2018) == 1:
        series = df_2018.iloc[0]
        power_per_turbine = series['Total_power'] / max(series['Turbine_n'], 1)
        data = data.append({'lat': series['Lat'], 'lon': series['Lon'], 'power per turbine': power_per_turbine}, ignore_index=True)

x = []
y = []
for i in range(len(data)):
    series = data.iloc[i]
    x.append([series['lat'], series['lon']])
    y.append(series['power per turbine'])

reg = LinearRegression().fit(x, y)
score = reg.score(x, y)
weights = reg.coef_
bias = reg.intercept_ 
print('score', score)
print('weights', weights)
print('bias', bias)
