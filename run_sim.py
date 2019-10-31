"""file containing class to run simulink from python"""

import numpy as np
import matlab.engine
from windTurbine import WindTurbine
import matplotlib.pyplot as plt


class Simulink():
    """class to run simulink"""
    def __init__(self, model_name, efficiency='[15]', terrain_rating='0.12'):
        self.model_name = model_name
        self.wind_model_name = model_name + '/Wind turbine'
        self.solar_model_name = model_name + '/Solar panels'
        self.engine = matlab.engine.start_matlab()
        self.engine.warning('off', nargout=0)
        self.efficiency = efficiency
        self.terrain_rating = terrain_rating
    
    def __del__(self):
        self.engine.quit()
    
    def run_simulation(self, solar_features, wm_type, n_Turbine):
        """run new simulation"""
        self.engine.Setup_parameters(nargout=0)

        surface_features = solar_features[0::3]
        angle_features = solar_features[1::3]
        orientation_features = solar_features[2::3]

        azimuth = str(list(orientation_features)).replace(' ', '')
        inclanation = str(list(angle_features)).replace(' ', '')
        surface = str(list(surface_features)).replace(' ', '')

        windTurbine = WindTurbine(n_turbines=str(n_Turbine), wm_type=wm_type)

        self.engine.load_system(self.model_name)

        self.engine.set_param(
            self.solar_model_name,
            'Az', azimuth,
            'Inc', inclanation,
            'Opp', surface,
            'ethasp', self.efficiency,
            nargout=0)

        self.engine.set_param(
            self.wind_model_name,
            'P', windTurbine.power,
            'v', windTurbine.wind_velocity,
            'h', windTurbine.rotor_height,
            'a', self.terrain_rating,
            'nwt', windTurbine.n_turbines,
            nargout=0)

        self.engine.Setup_Toutdoor(nargout=0)
        self.engine.Setup_qsolar2(nargout=0)
        self.engine.Setup_wind(nargout=0)        
        
        output = self.engine.sim(self.model_name, 'ReturnWorkspaceOutputs', 'on')
        self.engine.workspace['Output'] = output
        output = np.array(self.engine.eval("Output.Ptotal"))
        total = np.sum(output[:, 1:], axis=1)
        return total, output

if __name__ == '__main__':
    sim = Simulink('WT_SP_model_vs1total')
    output, all_out = sim.run_simulation(np.array([1000, 15, 0, 1000, 15, 0, 1000, 15, 0, 1000, 15, 0]), 4, 7)

    output1 = sim.run_simulation(np.array([6000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 0,0)
    output2 = sim.run_simulation(np.array([6000, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 0,0)
    output3 = sim.run_simulation(np.array([6000, 35, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 0,0)
    output4 = sim.run_simulation(np.array([6000, 35, -45, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 0,0)


    #print(output)
    #print(np.mean(output))
    reshape01 = np.reshape(output1[:8760], (365,24))
    mean1 = np.mean(reshape01, axis=0)
    reshape02 = np.reshape(output2[:8760], (365,24))
    mean2 = np.mean(reshape02, axis=0)
    reshape03 = np.reshape(output3[:8760], (365,24))
    mean3 = np.mean(reshape03, axis=0)
    reshape04 = np.reshape(output4[:8760], (365,24))
    mean4 = np.mean(reshape04, axis=0)
    
    #print('maximale waarde van 0 graden is: ', reshape01.max())
    #print('minimale waarde van 0 graden is: ', reshape01.min())

    #plt.subplot(2,1,1)
    plt.plot(mean1, label='0 degrees angle, 0 degrees rotation')
    #plt.subplot(2,1,2)
    plt.plot(mean2, label='35 degrees angle, 0 degrees rotation')
    plt.plot(mean3, label='35 degrees angle, 45 degrees rotation')
    plt.plot(mean4, label='35 degrees angle, -45 degrees rotation')
    plt.xlabel('Hours of the day')
    plt.ylabel('Production')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.16),
          ncol=2, fancybox=True, shadow=True)
    # plt.show()
