"""Function to plot in a configuration from a generation"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math
from run_sim import Simulink
from save_and_load import PopulationSaver
from calculate_cost import CostCalculator
import os

def plot(model_name, generation_number):
    simulink = Simulink('WT_SP_model_vs1total')
    generation = load(model_name=model_name, generation_number=generation_number)
    kW_distribution, _ = simulink.run_simulation(generation[0][0:-1], 4, generation[0][-1])
    cb_cost_table = pd.DataFrame({'area':[1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 600, 1000, 1250, 1600, 2000, 3000, 5000, 8000 , 10000, 12000, 15000, 18000, 22000, 25000, 30000, 40000, 50000],
        'cost':[0.002, 0.003, 0.008, 0.013, 0.014, 0.016, 0.025, 0.035, 0.075, 0.1, 0.15, 0.22, 0.3, 0.39, 0.49, 0.5, 0.62, 0.8, 1.25, 1.6, 2, 2.5, 3.5, 6, 9, 11, 13, 17.5, 20, 30, 40, 50, 60, 72]})
    calculatecost = CostCalculator(190, 50, 6000, 1000000, cb_cost_table, 1000, 230)
    dic = calculatecost.get_stats(kW_distribution,319650,4,int(generation[0][-1]))
    kW_distribution = np.mean(np.reshape(kW_distribution[:8760], (365,24)), axis=1)
    consumption = np.full(len(kW_distribution), 6000)

    #sns.set()
    t1 = "Storage capacity: \nAmount of windturbines: \nCable Area: "
    t2 = str(int(dic['total_storage'])) + " kWh\n" + str(int(generation[0][-1])) + "\n" + str(int(dic['cable_area'])) + "mm²"
    t3 = ""
    for I in range(4):
        if generation[0][0 + I*3] > 0:
            t3 = t3 + "SP" + str(I) + " - Area: " + str(int(generation[0][0 + I*3])) +\
                "m² - Angle: " + str(int(generation[0][1 + I*3])) +\
                "° - Orientation: " + str(int(generation[0][2 + I*3])) + "°\n"

    #sns.set_style("whitegrid")
    plt.subplot(2, 1, 1)
    plt.text(350, kW_distribution.max() * 0.90, t2, ha='left', style='italic', wrap=True)
    plt.text(350, kW_distribution.max() * 0.90, t1, ha='right', wrap=True)
    plt.text(280, kW_distribution.max() * 0.65, t3, ha='left', wrap=True)
    #sns.set_style("whitegrid")
    plt.plot(kW_distribution, color='green', alpha=0.5)
    plt.plot(consumption, color='red')
    plt.xlabel('Days')
    plt.ylabel('kW')
    plt.subplot(2, 1, 2)
    #sns.set_style("whitegrid")
    plt.plot(np.cumsum(kW_distribution - 6000), color='green', alpha=0.5)
    plt.plot(np.zeros(len(kW_distribution)), color='red')
    plt.xlabel('Days')
    plt.ylabel('kWh')
    plt.show()

def load(model_name, generation_number, takebest=True):
    if model_name is None or generation_number is None:
        raise Exception('None attribute detected on model or generation parameter')
    elif generation_number < 0:
        raise Exception('There can be no generation with a number less then zero')
    path = 'saved_runs'+ os.sep + model_name + os.sep
    if takebest: 
        return np.loadtxt(path + 'best_' + str(generation_number) + '.csv', delimiter=',')
    else:
        return np.loadtxt(path + 'generation_' + str(generation_number) + '.csv', delimiter=',')
    

if __name__ == '__main__':
    plot('Save_Accukosten_100000', 52)
