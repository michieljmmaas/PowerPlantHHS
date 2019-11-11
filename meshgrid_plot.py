import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 


# data = np.array(pd.read_csv('df_median_solar.csv',index_col=0))

# x = [ i for i in range(0,90)]

# y = [ i for i in range(0,360,5)]

# data = np.concatenate((data[:,36:],data[:,:36]),axis=1)

# plt.xticks(list(range(0,72,6)), list(range(0,360,30)))
# plt.xlabel('Degrees of orientation (North = 0)')
# plt.ylabel('Degrees of inclanation')
# # plt.title('Maximum output recorded anually')
# plt.title('Annual total output')

# # plt.pcolor(data, edgecolors='k', linewidths=0.10)
# plt.pcolor(data,cmap='plasma')
# cbar = plt.colorbar()
# cbar.set_label('Production in kWh')
# plt.show()


"""
"""
t = [i for i in range(0,8760)]
data1 = pd.read_csv('df_wind_volker.csv',index_col=0)
data2 = pd.read_csv('df_volkerspeed.csv',index_col=0)

# data1 = data1.iloc[6000:]
# data2 = data2.iloc[6000:]

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time (hr)')
ax1.set_ylabel('Power output (kW)', color=color)
ax1.plot(t, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Wind speed (m/s)', color=color)  
ax2.plot(t, data2, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Windspeed vs. Power output from last 760hrs of year')
# fig.tight_layout()  
plt.show()

"""
"""
# data = pd.read_csv('df_wind_volker.csv',index_col=0)

# data.hist(bins=100)
# plt.title('Wind turbine power output')
# plt.ylabel('Number of hours')
# plt.xlabel('Power (kW)')

# plt.show()
