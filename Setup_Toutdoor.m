
[NUM]=xlsread('formatted_data.xls','1%overschrijding-B.2');   

t=NUM(:,18);

[NUM]=xlsread('location_375.xls','2018');
Toutdoor=NUM(:,6)/10;
%Toutdoor=NUM(:,20);

Tout=horzcat(t,Toutdoor);

save Toutdoor Tout
clear NUM RAW TXT t
