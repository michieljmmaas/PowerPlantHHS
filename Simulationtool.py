import wx
import sys
from generators import Windturbine
from Simulator import Simulator
from train import train
import numpy as np
import pandas as pd
import os
import xlsxwriter as xlw
from calculate_cost import CostCalculator
from genetic_algorith import GeneticAlgorith
from multiprocessing import Process, Value
from location import Location

locations=[ 'Valkenburg', 'Dekooy', 'Schiphol', 'Hoornterschelling', 'Debilt',
            'Soesterberg', 'Stavoren', 'Lelystad', 'Leeuwarden', 'Marknesse',
            'Deelen', 'Lauwersoog', 'Heino', 'Hoogeveen', 'Eelde', 'Hupsel',
            'Nieuwbeerta', 'Twenthe', 'Vlissingen', 'Westdorpe',
            'Wilhelminadorp', 'Hoekvanholland', 'Rotterdam', 'Cabauw',
            'Gilzerijen', 'Herwijnen', 'Eindhoven', 'Volkel', 'Ell',
            'Maastricht', 'Arcen', 'Nen']

# Define the tab content as classes:
class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

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

        self.places = wx.ComboBox(self, wx.ID_ANY, value='Location', choices=locations)
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
        turbine = Windturbine(5)
        turbine.rotor_height = self.wt_height
        sim = Simulator(self.location, self.year_choice.GetValue(), turbine, terrain_factor=float(self.terrain_factor))
        sim.latitude = float(self.latitude)
        sim.longitude = float(self.longitude)
        windfeatures = [int(self.n_wt), int(self.wt_height)]
        solarfeatures = [float(self.sp_area_1), float(self.sp_ang_1), float(self.sp_or_1), 
                         float(self.sp_area_2), float(self.sp_ang_2), float(self.sp_or_2),
                         float(self.sp_area_3), float(self.sp_ang_3), float(self.sp_or_3),
                         float(self.sp_area_4), float(self.sp_ang_4), float(self.sp_or_4)]

        if self.store_wt_out:
            P_wt,_ = sim.calc_wind(windfeatures)
        else:
            P_wt = 0
        if self.store_sp_out:
            P_sp,_ = sim.calc_solar(Az=solarfeatures[2::3], Inc=solarfeatures[1::3],sp_area=solarfeatures[0::3], sp_eff=self.sp_eff)
        else:
            P_sp = 0
        if self.store_total_out:
            P_tot,_ = sim.calc_total_power(solarfeatures, windfeatures, self.sp_eff)
        else:
            P_tot = 0

        data = {'Pwt':P_wt,'Psp': P_sp,'Ptot': P_tot}

        self.write_data(data)
    
    def write_data(self, data):
        data_file = xlw.Workbook(self.filename_field.GetValue() + '.xlsx')
        bold = data_file.add_format({'bold': True})

        parametersheet = data_file.add_worksheet('Input parameters')

        parametersheet.write('B1', 'Place', bold)
        parametersheet.write('C1', self.location.name)
        parametersheet.write('B2', 'Year', bold)
        parametersheet.write('C2', self.year_choice.GetValue())
        parametersheet.write('B4', 'Latitude', bold)
        parametersheet.write('C4', self.latitude)
        parametersheet.write('B5', 'Longitude', bold)
        parametersheet.write('C5', self.longitude)
        parametersheet.write('B6', 'Terrain factor', bold)
        parametersheet.write('C6', self.terrain_factor)
        parametersheet.write('B7', 'N Windturbines', bold)
        parametersheet.write('C7', self.n_wt)
        parametersheet.write('B8', 'Rotor height', bold)
        parametersheet.write('C8', self.wt_height)
        parametersheet.write('B10', 'Sp Surface 1', bold)
        parametersheet.write('C10', self.sp_area_1)
        parametersheet.write('B11', 'Sp Angle 1', bold)
        parametersheet.write('C11', self.sp_ang_1)
        parametersheet.write('B12', 'Sp Orientation 1', bold)
        parametersheet.write('C12', self.sp_or_1)
        parametersheet.write('B13', 'Sp Surface 2', bold)
        parametersheet.write('C13', self.sp_area_2)
        parametersheet.write('B14', 'Sp Angle 2', bold)
        parametersheet.write('C14', self.sp_ang_2)
        parametersheet.write('B15', 'Sp Orientation 2', bold)
        parametersheet.write('C15', self.sp_or_2)
        parametersheet.write('B16', 'Sp Surface 3', bold)
        parametersheet.write('C16', self.sp_area_3)
        parametersheet.write('B17', 'Sp Angle 3', bold)
        parametersheet.write('C17', self.sp_ang_3)
        parametersheet.write('B18', 'Sp Orientation 3', bold)
        parametersheet.write('C18', self.sp_or_3)
        parametersheet.write('B19', 'Sp Surface 4', bold)
        parametersheet.write('C19', self.sp_area_4)
        parametersheet.write('B20', 'Sp Angle 4', bold)
        parametersheet.write('C20', self.sp_ang_4)
        parametersheet.write('B21', 'Sp Orientation 4', bold)
        parametersheet.write('C21', self.sp_or_4)
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

        graphsheet.insert_chart( 'B2', chart, { 'x_scale': 4, 'y_scale': 2,})
        data_file.close()

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
        sizer.Add(nb, 1, wx.ALL, 2)
        self.SetSizer(sizer)
        self.Layout()
        self.Fit()


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()