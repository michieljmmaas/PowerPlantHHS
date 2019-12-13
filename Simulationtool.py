import wx
import sys
from generators import Windturbine
from Simulator import Simulator
import numpy as np
import pandas as pd
import os
import xlsxwriter as xlw
import threading
from location import Location

myEVT_SIMDONE = wx.NewEventType()
EVT_SIMDONE = wx.PyEventBinder(myEVT_SIMDONE, 1)

class SimDoneEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, filename=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._filename = filename

    def GetName(self):
        
        return self._filename

class sim_worker(threading.Thread):
    def __init__(self, parent, params):

        threading.Thread.__init__(self)
        self.parent = parent
        self.location = params[0]
        self.year_choice = params[1]
        self.terrain_factor = params[2]
        self.latitude = params[3]
        self.longitude = params[4]
        self.windfeatures = params[5]
        self.solarfeatures = params[6]
        self.store_wt_out = params[7][0]
        self.store_sp_out = params[7][1]
        self.store_total_out = params[7][2]
        self.filename = params[8]
        self.sp_eff = params[9]

    def run(self):

        sim = Simulator(self.location, self.year_choice, Windturbine(5), terrain_factor = self.terrain_factor )
        sim.latitude = self.latitude
        sim.longitude = self.longitude

        if self.store_wt_out:
            P_wt,_ = sim.calc_wind(self.windfeatures)
        else:
            P_wt = 0
        if self.store_sp_out:
            P_sp,_ = sim.calc_solar(Az=self.solarfeatures[2::3], Inc=self.solarfeatures[1::3],sp_area=self.solarfeatures[0::3], sp_eff=self.sp_eff)
        else:
            P_sp = 0
        if self.store_total_out:
            P_tot,_ = sim.calc_total_power(self.solarfeatures, self.windfeatures, self.sp_eff)
        else:
            P_tot = 0

        data = {'Pwt':P_wt,'Psp': P_sp,'Ptot': P_tot}

        self.write_data(data, self.filename)

        evt = SimDoneEvent(myEVT_SIMDONE, -1, filename=self.filename)
        wx.PostEvent(self.parent, evt)

    def write_data(self, data, filename):
        
        data_file = xlw.Workbook('Output_Data' + os.sep + filename + '.xlsx')
        bold = data_file.add_format({'bold': True})

        parametersheet = data_file.add_worksheet('Input parameters')

        parametersheet.write('B1', 'Place', bold)
        parametersheet.write('C1', self.location.name)
        parametersheet.write('B2', 'Year', bold)
        parametersheet.write('C2', self.year_choice)
        parametersheet.write('B4', 'Latitude', bold)
        parametersheet.write('C4', self.latitude)
        parametersheet.write('B5', 'Longitude', bold)
        parametersheet.write('C5', self.longitude)
        parametersheet.write('B6', 'Terrain factor', bold)
        parametersheet.write('C6', self.terrain_factor)
        parametersheet.write('B7', 'N Windturbines', bold)
        parametersheet.write('C7', self.windfeatures[0])
        parametersheet.write('B8', 'Rotor height', bold)
        parametersheet.write('C8', self.windfeatures[1])
        parametersheet.write('B10', 'Sp Surface 1', bold)
        parametersheet.write('C10', self.solarfeatures[0])
        parametersheet.write('B11', 'Sp Angle 1', bold)
        parametersheet.write('C11', self.solarfeatures[1])
        parametersheet.write('B12', 'Sp Orientation 1', bold)
        parametersheet.write('C12', self.solarfeatures[2])
        parametersheet.write('B13', 'Sp Surface 2', bold)
        parametersheet.write('C13', self.solarfeatures[3])
        parametersheet.write('B14', 'Sp Angle 2', bold)
        parametersheet.write('C14', self.solarfeatures[4])
        parametersheet.write('B15', 'Sp Orientation 2', bold)
        parametersheet.write('C15', self.solarfeatures[5])
        parametersheet.write('B16', 'Sp Surface 3', bold)
        parametersheet.write('C16', self.solarfeatures[6])
        parametersheet.write('B17', 'Sp Angle 3', bold)
        parametersheet.write('C17', self.solarfeatures[7])
        parametersheet.write('B18', 'Sp Orientation 3', bold)
        parametersheet.write('C18', self.solarfeatures[8])
        parametersheet.write('B19', 'Sp Surface 4', bold)
        parametersheet.write('C19', self.solarfeatures[9])
        parametersheet.write('B20', 'Sp Angle 4', bold)
        parametersheet.write('C20', self.solarfeatures[10])
        parametersheet.write('B21', 'Sp Orientation 4', bold)
        parametersheet.write('C21', self.solarfeatures[11])
        parametersheet.write('B22', 'Sp Efficiency', bold)
        parametersheet.write('C22', self.sp_eff)
        
        datasheet = data_file.add_worksheet('Output data')
        
        demand = np.full(365, 6000)
        data_sized = {'Pwt': 0, 'Psp': 0, 'Ptot': 0}

        datasheet.write('A1', 'Hourly', bold)        
        datasheet.write('E1', 'Daily', bold)
        datasheet.write('A2', 'Pwt', bold)
        datasheet.write('B2', 'Psp', bold)
        datasheet.write('C2', 'Ptot', bold)
        datasheet.write('E2', 'Pwt', bold)
        datasheet.write('F2', 'Psp', bold)
        datasheet.write('G2', 'Ptot', bold)
        datasheet.write('H2', 'Demand', bold)
        datasheet.write_column('H3', demand)

        if self.store_wt_out:
            datasheet.write_column('A3', data['Pwt'])
            data_sized['Pwt'] = np.mean(np.reshape(data['Pwt'], (365,24)), axis=1)
            datasheet.write_column('E3', data_sized['Pwt'])
        
        if self.store_sp_out:
            datasheet.write_column('B3', data['Psp'])
            data_sized['Psp'] = np.mean(np.reshape(data['Psp'], (365,24)), axis=1)
            datasheet.write_column('F3', data_sized['Psp'])
        
        if self.store_total_out:
            datasheet.write_column('C3', data['Ptot'])
            data_sized['Ptot'] = np.mean(np.reshape(data['Ptot'], (365,24)), axis=1)
            datasheet.write_column('G3', data_sized['Ptot'])

        graphsheet = data_file.add_worksheet('Graphs')

        chart = data_file.add_chart({'type': 'line'})
        chart.set_title({'name':'Daily avg. output'})
        chart.set_x_axis({'display units':'days'})
        chart.set_y_axis({'display units':'Output'})

        if self.store_wt_out:
            chart.add_series({
            'values':     '=Output data!$E$3:$E$367',
            'line':       {'color': 'blue'},
            'name': 'Wind'
            })

        if self.store_sp_out:
            chart.add_series({
            'values':     '=Output data!$F$3:$F$367',
            'line':       {'color': 'yellow'},
            'name': 'Solar'
            })

        if self.store_total_out:     
            chart.add_series({
            'values':     '=Output data!$G$3:$G$367',
            'line':       {'color': 'green'},
            'name': 'Total'
            })

        chart.add_series({
        'values':     '=Output data!$H$3:$H$367',
        'line':       {'color': 'red'},
        'name': 'Demand'
        })

        graphsheet.insert_chart( 'B2', chart, { 'x_scale': 3, 'y_scale': 2,})

        graph1 = data_file.add_chart({'type': 'line'})
        graph1.set_title({'name': 'Hourly output graph 1 of 12'})
        graph1.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph1.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph2 = data_file.add_chart({'type': 'line'})
        graph2.set_title({'name': 'Hourly output graph 2 of 12'})
        graph2.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph2.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph3 = data_file.add_chart({'type': 'line'})
        graph3.set_title({'name': 'Hourly output graph 3 of 12'})
        graph3.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph3.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph4 = data_file.add_chart({'type': 'line'})
        graph4.set_title({'name': 'Hourly output graph 4 of 12'})
        graph4.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph4.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph5 = data_file.add_chart({'type': 'line'})
        graph5.set_title({'name': 'Hourly output graph 5 of 12'})
        graph5.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph5.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph6 = data_file.add_chart({'type': 'line'})
        graph6.set_title({'name': 'Hourly output graph 6 of 12'})
        graph6.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph6.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph7 = data_file.add_chart({'type': 'line'})
        graph7.set_title({'name': 'Hourly output graph 7 of 12'})
        graph7.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph7.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph8 = data_file.add_chart({'type': 'line'})
        graph8.set_title({'name': 'Hourly output graph 8 of 12'})
        graph8.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph8.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph9 = data_file.add_chart({'type': 'line'})
        graph9.set_title({'name': 'Hourly output graph 9 of 12'})
        graph9.set_x_axis({ 'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph9.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph10 = data_file.add_chart({'type': 'line'})
        graph10.set_title({'name': 'Hourly output graph 10 of 12'})
        graph10.set_x_axis({'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph10.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})
        
        graph11 = data_file.add_chart({'type': 'line'})
        graph11.set_title({'name': 'Hourly output graph 11 of 12'})
        graph11.set_x_axis({'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph11.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})

        graph12 = data_file.add_chart({'type': 'line'})
        graph12.set_title({'name': 'Hourly output graph 12 of 12'})
        graph12.set_x_axis({'display units':'hours',
                            'name_font': {'size': 14, 'bold': True}})
        graph12.set_y_axis({'display units': 'Output',
                            'name_font': {'size': 14, 'bold': True}})


        if self.store_wt_out:
            graph1.add_series({
            'values': '=Output data!$A$3:$A$733',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph2.add_series({
            'values': '=Output data!$A$733:$A$1463',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph3.add_series({
            'values': '=Output data!$A$1463:$A$2193',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph4.add_series({
            'values': '=Output data!$A$2193:$A$2923',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph5.add_series({
            'values': '=Output data!$A$2923:$A$3653',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph6.add_series({
            'values': '=Output data!$A$3653:$A$4383',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph7.add_series({
            'values': '=Output data!$A$4383:$A$5113',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph8.add_series({
            'values': '=Output data!$A$5113:$A$5843',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph9.add_series({
            'values': '=Output data!$A$5843:$A$6573',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph10.add_series({
            'values': '=Output data!$A$6573:$A$7303',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph11.add_series({
            'values': '=Output data!$A$7303:$A$8033',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
            graph12.add_series({
            'values': '=Output data!$A$8033:$A$8763',
            'line': { 'color': 'blue'},
            'name': 'Wind'
                })
        if self.store_sp_out:
            graph1.add_series({
            'values': '=Output data!$B$3:$B$733',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph2.add_series({
            'values': '=Output data!$B$733:$B$1463',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph3.add_series({
            'values': '=Output data!$B$1463:$B$2193',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph4.add_series({
            'values': '=Output data!$B$2193:$B$2923',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph5.add_series({
            'values': '=Output data!$B$2923:$B$3653',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph6.add_series({
            'values': '=Output data!$B$3653:$B$4383',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph7.add_series({
            'values': '=Output data!$B$4383:$B$5113',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph8.add_series({
            'values': '=Output data!$B$5113:$B$5843',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph9.add_series({
            'values': '=Output data!$B$5843:$B$6573',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph10.add_series({
            'values': '=Output data!$B$6573:$B$7303',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph11.add_series({
            'values': '=Output data!$B$7303:$B$8033',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
            graph12.add_series({
            'values': '=Output data!$B$8033:$B$8763',
            'line': {'color' : 'yellow'},
            'name': 'Solar'
                })
        if self.store_total_out:
            graph1.add_series({
            'values': '=Output data!$C$3:$C$733',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph2.add_series({
            'values': '=Output data!$C$733:$C$1463',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph3.add_series({
            'values': '=Output data!$C$1463:$C$2193',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph4.add_series({
            'values': '=Output data!$C$2193:$C$2923',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph5.add_series({
            'values': '=Output data!$C$2923:$C$3653',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph6.add_series({
            'values': '=Output data!$C$3653:$C$4383',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph7.add_series({
            'values': '=Output data!$C$4383:$C$5113',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph8.add_series({
            'values': '=Output data!$C$5113:$C$5843',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph9.add_series({
            'values': '=Output data!$C$5843:$C$6573',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph10.add_series({
            'values': '=Output data!$C$6573:$C$7303',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph11.add_series({
            'values': '=Output data!$C$7303:$C$8033',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
            graph12.add_series({
            'values': '=Output data!$C$8033:$C$8763',
            'line': { 'color': 'green'},
            'name': 'Total'
                })
        

        graphsheet.insert_chart( 'B34', graph1, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B68', graph2, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B102', graph3, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B136', graph4, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B170', graph5, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B204', graph6, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B238', graph7, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B272', graph8, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B306', graph9, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B340', graph10, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B374', graph11, { 'x_scale': 2, 'y_scale': 2,})
        graphsheet.insert_chart( 'B408', graph12, { 'x_scale': 2, 'y_scale': 2,})


        data_file.close()

class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.locations = [i.lower().capitalize() for i in pd.read_csv('Data/locations.csv',index_col=0,header=0).NAME.values]

        self.years = ['0000']

        self.store_wt_out = False
        self.store_sp_out = False
        self.store_total_out = False

        self.sp_area_1 = 10000
        self.sp_area_2 = 10000
        self.sp_area_3 = 10000
        self.sp_area_4 = 10000
        self.sp_or_1 = -5
        self.sp_or_2 = -10
        self.sp_or_3 = 10
        self.sp_or_4 = 5
        self.sp_ang_1 = 15
        self.sp_ang_2 = 15
        self.sp_ang_3 = 15
        self.sp_ang_4 = 15
        self.sp_eff = 16

        self.wt_height = 100
        self.n_wt = 7

        self.latitude = 0
        self.longitude = 0
        self.terrain_factor = 0

        vbox = wx.BoxSizer(wx.VERTICAL)

        locbox = wx.StaticBox(self, -1, 'Location')
        solbox = wx.StaticBox(self, -1, 'Solar options')
        winbox = wx.StaticBox(self, -1, 'Windturbine options')
        storebox = wx.StaticBox(self, -1, 'Storage options')

        locSizer = wx.StaticBoxSizer(locbox, wx.VERTICAL)
        solSizer = wx.StaticBoxSizer(solbox, wx.VERTICAL)
        winSizer = wx.StaticBoxSizer(winbox, wx.VERTICAL)
        storeSizer = wx.StaticBoxSizer(storebox, wx.VERTICAL)

        hlocSizer = wx.BoxSizer(wx.HORIZONTAL)
        hsolSizer = wx.BoxSizer(wx.HORIZONTAL)
        hwinSizer = wx.BoxSizer(wx.HORIZONTAL)
        hstoreSizer = wx.BoxSizer(wx.HORIZONTAL)
        hnameSizer = wx.BoxSizer(wx.HORIZONTAL)
        hbuttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        loc_grid = wx.FlexGridSizer(3, 2, 10, 10)
        sol_grid = wx.FlexGridSizer(4, 5, 10, 10)
        win_grid = wx.FlexGridSizer(3, 2, 10, 10)

        self.lat_field = wx.TextCtrl(self, wx.ID_ANY, value=str(self.latitude))
        self.lon_field = wx.TextCtrl(self, wx.ID_ANY, value=str(self.longitude))

        self.lat_txt = wx.StaticText(self, wx.ID_ANY, 'Latitude ')
        self.lon_txt = wx.StaticText(self, wx.ID_ANY, 'Longitude ')

        self.places = wx.ComboBox(self, wx.ID_ANY, value='Location', choices=self.locations)
        self.year_choice = wx.ComboBox(self, wx.ID_ANY, value='Year', choices=self.years)

        self.sp_eff_text = wx.StaticText(self, wx.ID_ANY, 'Panel efficiency(%) ')
        self.sp_eff_field = wx.TextCtrl(self, wx.ID_ANY, value = str(self.sp_eff))
        self.area_txt = wx.StaticText(self, wx.ID_ANY, 'Surface ')
        self.area_field1 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_area_1))
        self.area_field2 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_area_2))
        self.area_field3 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_area_3))
        self.area_field4 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_area_4))

        self.angle_txt = wx.StaticText(self, wx.ID_ANY, 'Angle ')
        self.angle_field1 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_ang_1))
        self.angle_field2 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_ang_2))
        self.angle_field3 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_ang_3))
        self.angle_field4 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_ang_4))

        self.or_txt = wx.StaticText(self, wx.ID_ANY, 'Orientation ')
        self.or_field1 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_or_1))
        self.or_field2 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_or_2))
        self.or_field3 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_or_3))
        self.or_field4 = wx.TextCtrl(self, wx.ID_ANY, value=str(self.sp_or_4))

        self.nwt_txt = wx.StaticText(self, wx.ID_ANY, 'Number of turbines ')
        self.nwt_field = wx.TextCtrl(self, wx.ID_ANY, value=str(self.n_wt))
        self.wth_txt = wx.StaticText(self, wx.ID_ANY, 'Turbine height ')
        self.wth_field = wx.TextCtrl(self, wx.ID_ANY, value=str(self.wt_height))
        self.ter_txt = wx.StaticText(self, wx.ID_ANY, 'Terrain factor ')
        self.ter_field = wx.TextCtrl(self, wx.ID_ANY, value=str(self.terrain_factor))

        self.wt_out = wx.CheckBox(self, wx.ID_ANY, 'Turbinepower ')
        self.sp_out = wx.CheckBox(self, wx.ID_ANY, 'Solarpower ')
        self.total_out = wx.CheckBox(self, wx.ID_ANY, 'Total power ')
        self.filename_txt = wx.StaticText(self, wx.ID_ANY, 'Filename: ')
        self.filename_field = wx.TextCtrl(self, wx.ID_ANY, 'Sim_output')

        self.sim_button = wx.Button(self, wx.ID_ANY, label='Simulate')
        self.sim_button.Bind(wx.EVT_BUTTON, self.on_simbutton_clicked)

        self.places.Bind(wx.EVT_COMBOBOX, self.on_location_picked)
        self.sp_out.Bind(wx.EVT_CHECKBOX, self.on_checkbox_ticked)
        self.wt_out.Bind(wx.EVT_CHECKBOX, self.on_checkbox_ticked)
        self.total_out.Bind(wx.EVT_CHECKBOX, self.on_checkbox_ticked)

        self.area_field1.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.area_field2.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.area_field3.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.area_field4.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.or_field1.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.or_field2.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.or_field3.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.or_field4.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.angle_field1.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.angle_field2.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.angle_field3.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.angle_field4.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.sp_eff_field.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.lat_field.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.lon_field.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.ter_field.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.wth_field.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)
        self.nwt_field.Bind(wx.EVT_TEXT, self.on_fieldbox_changed)

        self.Bind(EVT_SIMDONE, self.on_simdone)

        hlocSizer.Add(self.places, 0, wx.ALL, 2)
        hlocSizer.Add(self.year_choice, 0, wx.ALL, 2)
        
        loc_grid.Add(self.lat_txt, 0, wx.ALL, 2)
        loc_grid.Add(self.lat_field, 0, wx.ALL, 2)
        loc_grid.Add(self.lon_txt, 0, wx.ALL, 2)
        loc_grid.Add(self.lon_field, 0, wx.ALL, 2)

        hlocSizer.Add(loc_grid, 0, wx.ALL, 2)

        sol_grid.Add(self.area_txt, 0, wx.ALL, 2)
        sol_grid.Add(self.area_field1, 0, wx.ALL, 2)
        sol_grid.Add(self.area_field2, 0, wx.ALL, 2)
        sol_grid.Add(self.area_field3, 0, wx.ALL, 2)
        sol_grid.Add(self.area_field4, 0, wx.ALL, 2)
        sol_grid.Add(self.angle_txt, 0, wx.ALL, 2)
        sol_grid.Add(self.angle_field1, 0, wx.ALL, 2)
        sol_grid.Add(self.angle_field2, 0, wx.ALL, 2)
        sol_grid.Add(self.angle_field3, 0, wx.ALL, 2)
        sol_grid.Add(self.angle_field4, 0, wx.ALL, 2)
        sol_grid.Add(self.or_txt, 0, wx.ALL, 2)
        sol_grid.Add(self.or_field1, 0, wx.ALL, 2)
        sol_grid.Add(self.or_field2, 0, wx.ALL, 2)
        sol_grid.Add(self.or_field3, 0, wx.ALL, 2)
        sol_grid.Add(self.or_field4, 0, wx.ALL, 2)
        sol_grid.Add(self.sp_eff_text, 0, wx.ALL, 2)
        sol_grid.Add(self.sp_eff_field, 0, wx.ALL, 2)
        
        hsolSizer.Add(sol_grid, 0, wx.ALL, 2)
        
        # hbox3.Add(self.power_label, 0, wx.ALL, 8)
        hstoreSizer.Add(self.wt_out, 0, wx.ALL, 8)
        hstoreSizer.Add(self.sp_out, 0, wx.ALL, 8)
        hstoreSizer.Add(self.total_out, 0, wx.ALL, 8)
        hnameSizer.Add(self.filename_txt, 0, wx.ALL, 8)
        hnameSizer.Add(self.filename_field, 0, wx.ALL, 8)

        win_grid.Add(self.nwt_txt, 0, wx.ALL, 2)
        win_grid.Add(self.nwt_field, 0, wx.ALL, 2)
        win_grid.Add(self.wth_txt, 0, wx.ALL, 2)
        win_grid.Add(self.wth_field, 0, wx.ALL, 2)
        win_grid.Add(self.ter_txt, 0, wx.ALL, 2)
        win_grid.Add(self.ter_field, 0, wx.ALL, 2)

        hwinSizer.Add(win_grid, 0, wx.ALL, 2)

        hbuttonSizer.Add(self.sim_button, 0, wx.ALL|wx.CENTER, 8)

        locSizer.Add(hlocSizer, 0 , wx.ALL, 2)
        solSizer.Add(hsolSizer, 0, wx.ALL, 2)
        winSizer.Add(hwinSizer, 0, wx.ALL, 2)
        storeSizer.Add(hstoreSizer, 0, wx.ALL, 2)
        storeSizer.Add(hnameSizer, 0, wx.ALL, 2)

        vbox.Add(locSizer, 0, wx.ALL, 2)
        vbox.Add(solSizer, 0, wx.ALL, 2)
        vbox.Add(winSizer, 0, wx.ALL, 2)
        vbox.Add(storeSizer, 0, wx.ALL, 2)
        vbox.Add(hbuttonSizer, 0, wx.ALL|wx.CENTER, 2)

        self.SetSizer(vbox)

    def on_location_picked(self, event):
        self.location = Location(event.GetString())
        self.years = self.location.get_years()
        self.update_fields()

    def on_checkbox_ticked(self, event):
        self.store_wt_out = self.wt_out.GetValue()
        self.store_sp_out = self.sp_out.GetValue()
        self.store_total_out = self.total_out.GetValue()

    def update_fields(self):
        self.year_choice.Clear()
        self.year_choice.AppendItems(self.years)

        self.lat_field.SetValue(str('%.3f'%self.location.latitude))
        self.lon_field.SetValue(str('%.3f'%self.location.longitude))
        self.ter_field.SetValue(str('%.3f'%self.location.terrain))
    
    def on_fieldbox_changed(self, event):
        self.sp_area_1 = float(self.area_field1.GetValue())
        self.sp_area_2 = float(self.area_field2.GetValue())
        self.sp_area_3 = float(self.area_field3.GetValue())
        self.sp_area_4 = float(self.area_field4.GetValue())
        self.sp_or_1 = float(self.or_field1.GetValue())
        self.sp_or_2 = float(self.or_field2.GetValue())
        self.sp_or_3 = float(self.or_field3.GetValue())
        self.sp_or_4 = float(self.or_field4.GetValue())
        self.sp_ang_1 = float(self.angle_field1.GetValue())
        self.sp_ang_2 = float(self.angle_field2.GetValue())
        self.sp_ang_3 = float(self.angle_field3.GetValue())
        self.sp_ang_4 = float(self.angle_field4.GetValue())
        self.sp_eff = float(self.sp_eff_field.GetValue())
        self.latitude = float(self.lat_field.GetValue())
        self.longitude = float(self.lon_field.GetValue())
        self.terrain_factor = float(self.ter_field.GetValue())
        self.wt_height = float(self.wth_field.GetValue())
        self.n_wt = float(self.nwt_field.GetValue())

    def on_simbutton_clicked(self, event):
        
        windfeatures = [int(self.n_wt), int(self.wt_height)]
        solarfeatures = [float(self.sp_area_1), float(self.sp_ang_1), float(self.sp_or_1), 
                         float(self.sp_area_2), float(self.sp_ang_2), float(self.sp_or_2),
                         float(self.sp_area_3), float(self.sp_ang_3), float(self.sp_or_3),
                         float(self.sp_area_4), float(self.sp_ang_4), float(self.sp_or_4)]
        store_params = [self.store_wt_out, self.store_sp_out, self.store_total_out]
        parameters = [self.location, self.year_choice.GetValue(), self.terrain_factor, 
                      self.latitude, self.longitude, windfeatures, solarfeatures, store_params, 
                      self.filename_field.GetValue(), self.sp_eff]

        worker = sim_worker(self, parameters)
        worker.start()

    def on_simdone(self, evt):
        filename = evt.GetName()

        file_info = 'Simulation stored in ' + filename + '.xlsx'
        wx.MessageBox(file_info, 'Simulation done', wx.OK)

class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Simulator")

        # Create a panel and notebook (tabs holder)
        nb = wx.Notebook(self)

        # Create the tab windows
        tab1 = TabOne(nb)
        tab2 = TabTwo(nb)

        # Add the windows to tabs and name them.
        nb.AddPage(tab1, "Simulation")
        nb.AddPage(tab2, "Training")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(sizer)
        self.Layout()
        self.Fit()


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
