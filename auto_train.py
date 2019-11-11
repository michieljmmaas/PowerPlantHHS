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

TURBINETYPE = 4
loc_name = 'volkel'

energy_demand = 6000
mutationrate = 150
def_cost = 1000000

solar_costs  = np.array([160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160])
storage_cost = np.array([400, 100000, 400, 100000, 400, 100000, 400, 100000, 400, 100000, 400, 100000])
numb_of_turb = np.array([0, 0, 100000, 10000, 10, 10, 100000, 100000, 10, 10, 0, 0])
terrain_arr = np.array([0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19])
sol_min = np.array([1000, 1000, 0, 0, 1000, 1000, 0, 0, 1000, 1000, 1000, 1000])
sol_max = np.array([10000000, 10000000, 0, 0, 10000000, 10000000, 0, 0, 10000000, 10000000, 10000000, 10000000])

loc_data = Location(loc_name)
file_name = 'Data' + os.sep + 'location_' + str(loc_data.stn) + '.xlsx'
year = str(loc_data.end_year)

turbine = Windturbine(TURBINETYPE)

sim = Simulator(file_name, year, turbine, index_col=0, latitude=loc_data.latitude, longitude=loc_data.longitude, terrain_factor=loc_data.terrain)

cb_cost_table = pd.DataFrame({'area': [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 600, 1000, 1250, 1600, 2000, 3000, 5000, 8000, 10000, 12000, 15000, 18000, 22000, 25000, 30000, 40000, 50000],
                              'cost': [0.002, 0.003, 0.008, 0.013, 0.014, 0.016, 0.025, 0.035, 0.075, 0.1, 0.15, 0.22, 0.3, 0.39, 0.49, 0.5, 0.62, 0.8, 1.25, 1.6, 2, 2.5, 3.5, 6, 9, 11, 13, 17.5, 20, 30, 40, 50, 60, 72]})
all_stats = pd.DataFrame(columns=['cost',
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

for i in range(0,len(solar_costs)):
    print(terrain_arr[i])
    print(solar_costs[i])
    print(storage_cost[i])
    print(sol_min[i])
    print(sol_max[i])
    print(numb_of_turb[i])

    sim.terrain_factor= terrain_arr[i]
    cost_calc = CostCalculator(solar_costs[i], storage_cost[i], energy_demand, def_cost, cb_cost_table, 0, 230)
    best_array = train(100, 100, sol_min[i], sol_max[i], 0, 90, 0, 359, mutationPercentage=mutationrate, target_kw=energy_demand, cost_calculator=cost_calc, simulator=sim, windturbineType=TURBINETYPE, N_WIND_MAX=numb_of_turb[i], tr_rating=loc_data.terrain, sp_efficiency=16)
    best_pick = best_array[0]
    best_solar = best_pick[:12]
    best_wind = best_pick[-2:]
    best_pick_power = sim.calc_total_power(best_solar, best_wind, 16)
    total_solar_sm = np.sum(best_solar[0::3])
    costings = cost_calc.calculate_cost(best_pick_power, total_solar_sm, TURBINETYPE, int(best_wind[0]))
    stats = cost_calc.get_stats(best_pick_power, total_solar_sm, TURBINETYPE, int(best_wind[0]))
    sol_power = np.sum(sim.calc_solar(Az=best_solar[2::3] ,Inc=best_solar[1::3] ,sp_area=best_solar[0::3]))
    win_power = np.sum(sim.calc_wind(best_wind))
    inputs = {'storage_st_cost': storage_cost[i],
              'zp_st_cost': solar_costs[i],
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
              'Zp_tot_power': sol_power,
              'Turbine_n':int(best_wind[0]),
              'Turbine_h':int(best_wind[1]),
              'Terrain_f': terrain_arr[i],
              'Turbine_tot_power': win_power,
              'Total_power: ': best_pick_power }

    stats.update(inputs)
    all_stats = all_stats.append(stats, ignore_index=True)

    break

#Uncomment this to store all the best stats from training
# all_stats.to_excel('Trainingstats.xlsx')
