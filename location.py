import pandas as pd
import os

class Location():
    """Class for getting location information"""
    def __init__(self, name):
        self.loc_data = pd.read_csv('Data' + os.sep + 'locations.csv', index_col=0, header=0)
        self.name = name.upper()
        self.latitude = self.loc_data.LAT[self.loc_data.NAME == self.name].values
        self.longitude = self.loc_data.LON[self.loc_data.NAME == self.name].values
        self.altitude = self.loc_data.ALT[self.loc_data.NAME == self.name].values
        self.stn = self.loc_data.STN[self.loc_data.NAME == self.name].values

if __name__ =='__main__':
    ijmond = Location('ijmond')
    print(ijmond.latitude)
