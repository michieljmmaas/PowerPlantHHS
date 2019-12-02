import pandas as pd
import os


class Location:
    """Class for getting location information"""

    def __init__(self, name, filePath=None):
        if filePath is None:
            filePath = 'Data' + os.sep + 'locations.csv';
        self.loc_data = pd.read_csv(filePath, index_col=0, header=0)
        self.name = name.upper()
        self.latitude = self.loc_data.LAT[self.loc_data.NAME == self.name].values[0]
        self.longitude = self.loc_data.LON[self.loc_data.NAME == self.name].values[0]
        self.altitude = self.loc_data.ALT[self.loc_data.NAME == self.name].values[0]
        self.stn = self.loc_data.STN[self.loc_data.NAME == self.name].values[0]
        self.start_year = self.loc_data.BEGIN[self.loc_data.NAME == self.name].values[0]
        self.end_year = self.loc_data.END[self.loc_data.NAME == self.name].values[0]
        self.complete = self.loc_data.COMPLETE[self.loc_data.NAME == self.name].values[0]
        self.terrain = self.loc_data.Terrain[self.loc_data.NAME == self.name].values[0]
