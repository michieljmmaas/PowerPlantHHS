% Programma om XLS bestand uit KNMI data om te zetten in een MAT bestand.
% Er wordt een matrix uitgevoerd met in de rijen de tijd
% in kolom 2 de windsnelheid op 10 m hoogte

[NUM,TXT,RAW]=xlsread('Volkel_wind_2017_matlab.xlsx',1);   

t=((1:8760)'-1)*3600;
vwind=NUM(:,1)/10; % op 10 m hoogte

vwind=horzcat(t,vwind);

save vwind vwind
clear NUM RAW TXT t