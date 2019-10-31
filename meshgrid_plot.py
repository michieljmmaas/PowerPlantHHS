import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 


data = np.array(pd.read_csv('total_df.csv',index_col=0))

x = [ i for i in range(0,90)]

y = [ i for i in range(0,360,5)]

data = np.concatenate((data[:,36:],data[:,:36]),axis=1)

plt.xticks(list(range(0,72,6)), list(range(0,360,30)))
plt.xlabel('Degrees of orientation (North = 0)')
plt.ylabel('Degrees of inclanation')
plt.title('Solar panel power production')

plt.pcolor(data)
plt.show()

