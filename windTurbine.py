
class WindTurbine:
    def __init__(self, n_turbines="", curve="", rotor_height="", wind_velocity="", wm_type=4):
        self.n_turbines = str(n_turbines)
        self.curve = curve
        self.rotor_height = rotor_height
        self.wind_velocity = wind_velocity
        self.wm_type = wm_type

        if wm_type == 2:
            self.curve = '[0,0,80,400,800,1200,1300,1500,1500,0,0]'
            self.rotor_height = '85'
            self.wind_velocity = '[0,3,5,7,8,9,10,12,25,25.01,40]'
        elif wm_type == 3:
            self.curve = '[0,0,27,1300,2700,4000,4300,5000,5000,0,0]'
            self.rotor_height = '124'
            self.wind_velocity = '[0,3,5,7,8,9,10,12,25,25.01,40]'
        elif wm_type == 1:
            self.curve = '[0,0,3,130,270,400,430,500,500,0,0]'
            self.rotor_height = '25'
            self.wind_velocity = '[0,3,5,7,8,9,10,12,25,25.01,40]'
        elif wm_type == 4:
            self.wind_velocity = '[0,2.5,3,4,5,6,7,8,9,10,11,12,25,25.01,40]'
            self.curve = '[0,0,47,111,217,375,595,889,1266,1736,2311,3000,3000,0,0]'
            self.rotor_height = '135'
        # else:
        #     self.n_turbines = '0'
        #     curve = '[0,0,0,0,0,0,0,0,0,0,0]'
        #     self.wind_velocity = '[0,3,5,7,8,9,10,12,25,25.01,40]'
        #     self.rotor_height = '0'

        self.power = self.curve


