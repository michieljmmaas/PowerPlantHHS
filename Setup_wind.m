
[NUM]=xlsread('formatted_data.xls','1%overschrijding-B.2');   

t=NUM(:,18);

vwind=NUM(:,21);

vwind=horzcat(t,vwind);

save vwind vwind
clear NUM RAW TXT t
