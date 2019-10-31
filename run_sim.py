"""file containing class to run simulink from python"""

import numpy as np
import matlab.engine
import matplotlib.pyplot as plt


class Simulink():
    """class to run simulink"""
    def __init__(self, model_name):
        self.model_name = model_name
        self.wind_model_name = model_name + '/Wind turbine'
        self.solar_model_name = model_name + '/Solar panels'
        self.engine = matlab.engine.start_matlab()
        self.engine.warning('off',nargout=0)
    
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
        efficiency = '[16]'
        
        if (wm_type == 2):
            turbines = str(n_Turbine)
            curve = '[0,0,80,400,800,1200,1300,1500,1500,0,0]'
            rotor_height = '85'
            wind_velocity = '[0,3,5,7,8,9,10,12,25,25.01,40]'
        elif (wm_type == 3):
            turbines = str(n_Turbine)
            curve = '[0,0,27,1300,2700,4000,4300,5000,5000,0,0]'
            rotor_height = '124'
            wind_velocity = '[0,3,5,7,8,9,10,12,25,25.01,40]'
        elif (wm_type == 1):
            turbines = str(n_Turbine)
            curve = '[0,0,3,130,270,400,430,500,500,0,0]'
            rotor_height = '25'
            wind_velocity = '[0,3,5,7,8,9,10,12,25,25.01,40]'
        elif (wm_type== 4):
            turbines = str(n_Turbine)
            wind_velocity = '[0,2.5,3,4,5,6,7,8,9,10,11,12,25,25.01,40]'
            curve = '[0,0,47,111,217,375,595,889,1266,1736,2311,3000,3000,0,0]'
            rotor_height = '135'
        else:
            turbines = '0'
            curve = '[0,0,0,0,0,0,0,0,0,0,0]'
            wind_velocity = '[0,3,5,7,8,9,10,12,25,25.01,40]'
            rotor_height = '0'

        power = curve
        
        terrain_rating = '0.12'

        self.engine.load_system(self.model_name)

        self.engine.set_param(
            self.solar_model_name,
            'Az', azimuth,
            'Inc', inclanation,
            'Opp', surface,
            'ethasp', efficiency,
            nargout=0)

        self.engine.set_param(
            self.wind_model_name,
            'P', power,
            'v', wind_velocity,
            'h', rotor_height,
            'a', terrain_rating,
            'nwt', turbines,
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
