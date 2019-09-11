import matlab.engine

model = 'WT_SP_model_vs1total'
modelWind = 'WT_SP_model_vs1total/Wind turbine'
modelSolar = 'WT_SP_model_vs1total/Solar panels'

print('Starting engine.')
eng = matlab.engine.start_matlab()
print('Engine started.')

eng.Setup_parameters(nargout=0)
eng.Setup_Toutdoor(nargout=0)
eng.Setup_qsolar2(nargout=0)
eng.Setup_wind(nargout=0)

azimuth = '[0,0,0,0]'
inclanation = '[15,15,45,0]'
surface = '[1000,0,0,0]'
efficiency = '[15]'

power = '[0,0,10,80,160,300,400,400,400]'
wind_velocity = '[0,1,2,4,6,8,10,20,30]'
rotor_height =  '10'
terrain_rating = '1'
turbines = '2'

eng.load_system(model)

eng.set_param(modelSolar,'Az',azimuth,'Inc',inclanation,'Opp',surface,'ethasp',efficiency,nargout=0)

eng.set_param(modelWind,'P',power,'v',wind_velocity,'h',rotor_height,'a',terrain_rating,'nwt',turbines,nargout=0)

print('Starting simulation')

Output = eng.sim(model,'ReturnWorkspaceOutputs', 'on')

eng.workspace['Output'] = Output

Ewindturbine = eng.eval("Output.Ewindturbine")
Pwindturbine = eng.eval("Output.Pwindturbine")
Esolarpanel =  eng.eval("Output.Esolarpanel")
Psolarpanel = eng.eval("Output.Psolarpanel")
Ptotal = eng.eval("Output.Ptotal")

Data = [Ewindturbine,Pwindturbine,Esolarpanel,Psolarpanel,Ptotal]

print('Simulation done')
# print (Data)

eng.quit()

print('Engine stopped')