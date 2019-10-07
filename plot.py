"""Function to plot in a configuration from a generation"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from run_sim import Simulink
from save_and_load import PopulationSaver

def plot(model_name, generation_number):
    simulink = Simulink('WT_SP_model_vs1total')
    generation = load(model_name=model_name, generation_number=generation_number)
    kW_distribution = simulink.run_simulation(generation[0][0:-1], 3, 4)
    kW_distribution = np.mean(np.reshape(kW_distribution[:8760], (365,24)), axis=1)
    consumption = np.full(len(kW_distribution), 6000)

    sns.set()
    plt.subplot()
    plt.subplot(2, 1, 1)
    plt.plot(kW_distribution, color='green', alpha=0.5)
    plt.plot(consumption, color='red')
    plt.xlabel('Days')
    plt.ylabel('kW')
    plt.subplot(2, 1, 2)
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
    path = 'saved_runs\\' + model_name + '\\'
    if takebest: 
        return np.loadtxt(path + 'best_' + str(generation_number) + '.csv', delimiter=',')
    else:
        return np.loadtxt(path + 'generation_' + str(generation_number) + '.csv', delimiter=',')
    

if __name__ == '__main__':
    plot('20190919_154332', 49)