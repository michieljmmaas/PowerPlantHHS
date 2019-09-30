
[NUM]=xlsread('formatted_data.xls','1%overschrijding-B.2');   

t=NUM(:,18);
doy=NUM(:,19);

hod=NUM(:,4);

qglob_hor=NUM(:,5);

qdir_nor=NUM(:,8);

% TEST MET INCLINATION AND AZIMUTH VECTOR
SOL=irrad_SET3(doy,hod,qglob_hor,qdir_nor,Az,Inc,0);

%save NEN5060 t doy hod qglob_hor qdir_nor Tout phiout xout pout vout dirvout cloudout rainout
Irrad=horzcat(t,SOL);
save SOL Irrad
clear doy hod Az Inc qglob_hor qdir_nor NUM SOL TXT RAW t Irrad
