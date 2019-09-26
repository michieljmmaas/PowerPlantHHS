"""file containing class to run simulink from python"""

import numpy as np
import matlab.engine


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
        efficiency = '[15]'
        
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
        
        terrain_rating = '1'
        

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
        total = np.sum(output[:,1:], axis=1)
        return total

if __name__ == '__main__':
    sim = Simulink('WT_SP_model_vs1total')

    output = sim.run_simulation(np.array([1000, 15, 0, 0, 15, 0, 0, 45, 0, 0, 0, 0]), 4)

    print(output)
    print(np.mean(output))
