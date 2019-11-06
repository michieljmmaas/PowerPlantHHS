"""Function to plot in a configuration from a generation"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math
from save_and_load import PopulationSaver
from generators import Windturbine
from calculate_cost import CostCalculator
from Simulator import Simulator
import os

def plot(model_name, generation_number, load2=True):
    turbine = Windturbine(4)
    simulator = Simulator('formatted_data.xls', '1%overschrijding-B.2', turbine, skiprows=[0, 1, 2, 3], terrain_factor=0.15)
    generation = load(model_name=model_name, generation_number=generation_number, load2 = True)
    total_power = simulator.calc_total_power(generation[0][0:-2], generation[0][-2])
    wind_power, wind_energy = simulator.calc_wind(generation[0][-2])
    oppervlakte = [generation[0][0],generation[0][3],generation[0][6],generation[0][9]]
    angle = [generation[0][1],generation[0][4],generation[0][7],generation[0][10]]
    orientation = [generation[0][2],generation[0][5],generation[0][8],generation[0][11]]
    solar_power, solar_energy = simulator.calc_solar(Az=orientation, Inc=angle, sp_area=oppervlakte, sp_eff=16, gref=0) #todo arrays maken voor orientatie, angle en oppervlakte
    max_power = total_power.max()
    # table of the diffrent cable cost
    cb_cost_table = pd.DataFrame({'area':[1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 600, 1000, 1250, 1600, 2000, 3000, 5000, 8000 , 10000, 12000, 15000, 18000, 22000, 25000, 30000, 40000, 50000],
        'cost':[0.002, 0.003, 0.008, 0.013, 0.014, 0.016, 0.025, 0.035, 0.075, 0.1, 0.15, 0.22, 0.3, 0.39, 0.49, 0.5, 0.62, 0.8, 1.25, 1.6, 2, 2.5, 3.5, 6, 9, 11, 13, 17.5, 20, 30, 40, 50, 60, 72]})
    calculatecost = CostCalculator(190, 50, 6000, 1000000, cb_cost_table, 1000, 230)
    # get the dictionary of a configuration that has the stats of the generation
    dic = calculatecost.get_stats(total_power,319650,4,int(generation[0][-2]))
    # creating an array of the mean values from the power output of the simulation
    wind_power = np.mean(np.reshape(wind_power[:8760], (365,24)),axis=1)
    solar_power = np.mean(np.reshape(solar_power[:8760], (365,24)),axis=1)
    consumption = np.full(len(total_power), 6000)
    return consumption, total_power, solar_power, wind_power, dic, generation, max_power

def draw_energy(consumption, total_power, solar_power, wind_power, dic, generation, max_power):
    # Creating mutiple text variables to display in the graph
    total_power = np.mean(np.reshape(total_power[:8760], (365,24)), axis=1)
    power_generated = total_power.sum()
    t1 = "Storage capacity: \nAmount of windturbines: \nCable area: \nMaximum Power Output: \nTotal Power Generated: "
    t2 = str(int(dic['total_storage'])) + " kWh\n" + \
        str(int(generation[0][-2])) + "\n" + \
        str(int(dic['cable_area'])) + " mm²\n" + \
        str(int(max_power)) + " kW\n" + \
        str(int(power_generated)) + " kWh"
    # Creating the solar stats text variables to display in the graph
    t3 = ""
    for I in range(4):
        if generation[0][0 + I*3] > 0:
            t3 = t3 + "SP" + str(I + 1) + " - Area: " + str(int(generation[0][0 + I*3])) +\
                "m² - Angle: " + str(int(generation[0][1 + I*3])) +\
                "° - Orientation: " + str(int(generation[0][2 + I*3])) + "°\n"

    plt.subplot(2, 1, 1)
    plt.text(330, total_power.max() * 1.04, t2, ha='left', va='top', style='italic', wrap=False)
    plt.text(330, total_power.max() * 1.04, t1, ha='right', va='top', wrap=False)
    plt.text(362, total_power.max() * 0.78, t3, ha='right', va='top', wrap=False)
    plt.plot(total_power, color='green', alpha=0.5, label='Total energy production')
    plt.plot(solar_power, color='yellow', alpha=0.5, label='Solar energy')
    plt.plot(wind_power, color='blue', alpha=0.5, label='Wind energy')
    plt.plot(consumption, color='red', label='Energy demand')
    plt.legend()
    plt.title("Power Average per Day")
    plt.xlabel('Days')
    plt.ylabel('kW')
    plt.xlim(0,365)
    plt.subplot(2, 1, 2)
    plt.show()

def draw_Battery_Use(consumption, total_power, solar_power, wind_power, dic, generation, max_power):
    # Creating mutiple text variables to display in the graph
    power_generated = total_power.sum()
    power = total_power
    total_power = np.mean(np.reshape(total_power[:8760], (365,24)), axis=1)
    t1 = "Storage capacity: \nAmount of windturbines: \nCable area: \nMaximum Power Output: \nTotal Power Generated: "
    t2 = str(int(dic['total_storage'])) + " kWh\n" + \
        str(int(generation[0][-2])) + "\n" + \
        str(int(dic['cable_area'])) + " mm²\n" + \
        str(int(max_power)) + " kW\n" + \
        str(int(power_generated)) + " kWh"
    # Creating the solar stats text variables to display in the graph
    t3 = ""
    for I in range(4):
        if generation[0][0 + I*3] > 0:
            t3 = t3 + "SP" + str(I + 1) + " - Area: " + str(int(generation[0][0 + I*3])) +\
                "m² - Angle: " + str(int(generation[0][1 + I*3])) +\
                "° - Orientation: " + str(int(generation[0][2 + I*3])) + "°\n"

    plt.subplot(2, 1, 1)
    plt.text(330, total_power.max() * 1.04, t2, ha='left', va='top', style='italic', wrap=False)
    plt.text(330, total_power.max() * 1.04, t1, ha='right', va='top', wrap=False)
    plt.text(362, total_power.max() * 0.78, t3, ha='right', va='top', wrap=False)
    plt.plot(total_power, color='green', alpha=0.5, label='Total energy production')
    plt.plot(solar_power, color='yellow', alpha=0.5, label='Solar energy')
    plt.plot(wind_power, color='blue', alpha=0.5, label='Wind energy')
    plt.plot(consumption, color='red', label='Energy demand')
    plt.legend()
    plt.title("Power Average per Day")
    plt.xlabel('Days')
    plt.ylabel('kW')
    plt.xlim(0,365)
    plt.subplot(2, 1, 2)
    power = power - 6000
    batterycharge = [int(dic['total_storage'])/2]
    Powershortage = []
    for I in power :
        batterycharge.append(batterycharge[-1] + I)
        if(int(dic['total_storage']) < batterycharge[-1]) : 
            batterycharge[-1] = int(dic['total_storage'])
        elif(0 > batterycharge[-1]) :
            batterycharge[-1] = 0
            Powershortage.append(len(batterycharge)-1)
    plt.plot(batterycharge, color='green', alpha=0.5)
    if len(Powershortage) == 0:
        plt.scatter(np.zeros(len(Powershortage)), Powershortage, color='red')
    plt.title("Power supply level over a Year")
    plt.xlabel('Hour')
    plt.ylabel('kWh')
    plt.xlim(0,8760)
    plt.show()

"""def plot_solarenergy(generation):
    npempty = np.zeros(9)
    colors = np.array(['green','blue','red','yellow'])
    text = ""
    for I in range(4):
        if(generation[0 + I*3]>0):
            solar_distribution, _ = simulink.run_simulation(np.concatenate((generation[0 + I*3:3 + I*3], npempty), axis=None), 4, 0)
            text = "SP" + str(I + 1) + " - Area: " + str(int(generation[0 + I*3])) +\
                "m² - Angle: " + str(int(generation[1 + I*3])) +\
                "° - Orientation: " + str(int(generation[2 + I*3])) + "°\n"
            plt.plot(np.mean(np.reshape(solar_distribution[:8760], (365,24)), axis=1), color=colors[I], alpha=0.5, label=text)
    plt.legend()
    plt.show()"""    

def load(model_name, generation_number, takebest=True, load2=True):
    if model_name is None or generation_number is None:
        raise Exception('None attribute detected on model or generation parameter')
    elif generation_number < 0:
        raise Exception('There can be no generation with a number less then zero')
    if load2:
        path = 'saved_runs'+ os.sep + model_name + os.sep
    else:
        path = model_name
    if takebest: 
        return np.loadtxt(path + 'best_' + str(generation_number) + '.csv', delimiter=',')
    else:
        return np.loadtxt(path + 'generation_' + str(generation_number) + '.csv', delimiter=',')
    

if __name__ == '__main__':
    consumption, total_power, solar_power, wind_power, dic, generation, max_power = plot('20191105_112838', 99)
    draw_Battery_Use(consumption, total_power, solar_power, wind_power, dic, generation, max_power)

