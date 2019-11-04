
[NUM]=xlsread('formatted_data.xls','1%overschrijding-B.2');   

t=NUM(:,18);
[NUM]=xlsread('location_375.xls','2018');

vwind=NUM(:,5)/10;
%vwind=NUM(:,21);
vwind=horzcat(t,vwind);

save vwind vwind
clear NUM RAW TXT t
