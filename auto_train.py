from train import train
import numpy as np
import pandas as pd
import os
from calculate_cost import CostCalculator
from genetic_algorith import GeneticAlgorith
from save_and_load import PopulationSaver
from multiprocessing import Process, Value
from generators import Windturbine
from Simulator import Simulator
from location import Location
import sys

batch_number = int(sys.argv[1])

TURBINETYPE = 4

energy_demand = 6000
mutationrate = 50
def_cost = 1000000

# solar_costs  = np.array([160, 160, 160])
# storage_cost = np.array([400, 400, 400])
# numb_of_turb = np.array([10, 10, 10])
# terrain_arr = np.array([0.12, 0.19, 0.12])
# sol_min = np.array([1000, 1000, 1000])
# sol_max = np.array([10000000, 10000000, 10000000])
loc_array = np.array(['DEKOOY', 'SCHIPHOL', 'HOORNTERSCHELLING', 'DEBILT', 'SOESTERBERG', 
                      'STAVOREN', 'LELYSTAD', 'LEEUWARDEN', 'MARKNESSE', 'DEELEN', 'LAUWERSOOG',
                      'HEINO', 'HOOGEVEEN', 'EELDE', 'HUPSEL', 'NIEUWBEERTA' , 'TWENTHE', 'VLISSINGEN',
                      'WESTDORPE', 'WILHELMINADORP', 'HOEKVANHOLLAND', 'ROTTERDAM', 'CABAUW', 'GILZERIJEN',
                      'HERWIJNEN', 'EINDHOVEN', 'VOLKEL', 'ELL', 'MAASTRICHT', 'ARCEN'])

turbine = Windturbine(TURBINETYPE)

# Loop locations here
for i in range(len(loc_array)):
    loc_data = Location(loc_array[i])
    file_name = 'Data' + os.sep + 'location_' + str(loc_data.stn) + '.xlsx'
    excel_file = pd.ExcelFile(file_name)
    years = np.array(excel_file.sheet_names)

    all_stats = pd.DataFrame(columns=['Name',
                                      'Year',
                                      'Lat',
                                      'Lon',
                                      'cost',
                                      'solar_cost',
                                      'wind_cost',
                                      'cable_cost',
                                      'cable_area',
                                      'storage_cost',
                                      'deficit_cost',
                                      'total_surplus',
                                      'total_storage',
                                      'storage_st_cost',
                                      'zp_st_cost',
                                      'wt_st_cost',
                                      'Zp1_angle',
                                      'Zp1_or',
                                      'Zp1_area',
                                      'Zp2_angle',
                                      'Zp2_or',
                                      'Zp2_area',
                                      'Zp3_angle',
                                      'Zp3_or',
                                      'Zp3_area',
                                      'Zp4_angle',
                                      'Zp4_or',
                                      'Zp4_area',
                                      'ZP_tot_area',
                                      'Zp_tot_power',
                                      'Turbine_n',
                                      'Turbine_h',
                                      'Terrain_f',
                                      'Turbine_tot_power',
                                      'Total_power'])

    for j in range(len(years)):
        # for z in range()
        sim = Simulator(file_name, years[j], turbine, terrain_factor=loc_data.terrain)
        cost_calc = CostCalculator(160, 400, energy_demand, def_cost, 0)
        best_array = train(1, 300, 0, 10000000, 0, 90, -45, 45, mutationPercentage=mutationrate, target_kw=energy_demand, cost_calculator=cost_calc, simulator=sim, windturbineType=TURBINETYPE, N_WIND_MAX=7, tr_rating=loc_data.terrain, sp_efficiency=16)

        best_pick = best_array[0]
        best_solar = best_pick[:12]
        best_wind = best_pick[-2:]

        best_pick_power,_ = sim.calc_total_power(best_solar, best_wind, 16)
        total_solar_sm = np.sum(best_solar[0::3])
        costings = cost_calc.calculate_cost(best_pick_power, total_solar_sm, TURBINETYPE, int(best_wind[0]))
        stats = cost_calc.get_stats(best_pick_power, total_solar_sm, TURBINETYPE, int(best_wind[0]))

        sol_power,_ = sim.calc_solar(Az=best_solar[2::3] ,Inc=best_solar[1::3] ,sp_area=best_solar[0::3])
        win_power,_ = sim.calc_wind(best_wind)
        win_power_total = np.sum(win_power)
        sol_power_total = np.sum(sol_power)

        inputs = {'Name': loc_data.name,
                  'Year': years[j],
                  'Lat': loc_data.latitude,
                  'Lon': loc_data.longitude,
                  'storage_st_cost': 400,
                  'zp_st_cost': 160,
                  'wt_st_cost': 3210000,
                  'Zp1_angle': best_solar[1],
                  'Zp1_or': best_solar[2],
                  'Zp1_area': best_solar[0],
                  'Zp2_angle': best_solar[4],
                  'Zp2_or': best_solar[5],
                  'Zp2_area': best_solar[3],
                  'Zp3_angle': best_solar[7],
                  'Zp3_or': best_solar[8],
                  'Zp3_area': best_solar[6],
                  'Zp4_angle': best_solar[10],
                  'Zp4_or': best_solar[11],
                  'Zp4_area': best_solar[9],
                  'ZP_tot_area': total_solar_sm,
                  'Zp_tot_power': sol_power_total,
                  'Turbine_n':int(best_wind[0]),
                  'Turbine_h':int(best_wind[1]),
                  'Terrain_f': loc_data.terrain,
                  'Turbine_tot_power': win_power_total,
                  'Total_power': np.sum(best_pick_power)}

        stats.update(inputs)
        outputs = {0:0}

        for k in range(len(best_pick_power)):
            outputs.update({k:best_pick_power[k]})

        stats.update(outputs)
        all_stats = all_stats.append(stats, ignore_index=True)
        #Uncomment this to store all the best stats from training
        print('Done with: ' + loc_array[i] + '. Year: ' + years[j])
        all_stats.to_excel('Output_data' + os.sep + 'Batch_' + str(batch_number)+ os.sep + 'Trainingstats_'+loc_array[i]+'_'+years[j]+'_'+'.xlsx')



