%% Calculo dasa Dimens�es roda de rea��o 
clc
clear

Isat = 0.5; %kg*m^2 -> Solidworks
rpm = 2200; % rota��o de posi��o est�tica -> menor velocidade e menor ru�do
rpmmax = 26500;
s = 0.2; %dist�ncia entre os motores
m = 1.22; %Massa do sat�lite

rho = 7860; % Densidade do a�o
hr = 10.5/1000; % espessuda do disco: valor que procuro
hdisk = 2/1000; % espessura dos raios da roda de rea��o
rdisk =  30/1000; %Raio interno da roda de rea��o desenhada
rw = 37/1000; % Raio da roda de rea��o desenhada
irwsolid =  157755.02/(1000*1000*1000); % Momento de in�rcia fornecido pelo Solidworks da roda de rea��o

%wrw = 2*pi*rpm/60; % Velocidade angular da roda de rea��o

Htot = 2*(Isat + m*(s/2)^2)*1; 

Hperrw = Htot/3

Hrw =  irwsolid * rpm

Hrwc = rpm * rho * pi /2*(hr*(rw^4-rdisk^4)+hdisk*rdisk^4)

vmaxsat =  irwsolid * rpmmax / Hperrw;

vmaxgs = 360*vmaxsat/60;

Kmax = (1/2)*(Hrw^2)/irwsolid

%% Calculo dasa Dimens�es roda de rea��o 
clc
clear

Isat = 0.5; %kg*m^2 -> Solidworks
rpm = 2200; % rota��o de posi��o est�tica -> menor velocidade e menor ru�do
rpmmax = 26500;
s = 0.2; %dist�ncia entre os motores
m = 1.22; %Massa do sat�lite

rho = 7860; % Densidade do a�o
hr = 30/1000; % espessuda do disco: valor que procuro
hdisk = 2/1000; % espessura dos raios da roda de rea��o
rdisk =  14.2/1000; %Raio interno da roda de rea��o desenhada
rw = 26/1000; % Raio da roda de rea��o desenhada
irwsolid =  157755.02/(1000*1000*1000); % Momento de in�rcia fornecido pelo Solidworks da roda de rea��o

%wrw = 2*pi*rpm/60; % Velocidade angular da roda de rea��o

Htot = 2*(Isat + m*(s/2)^2)*1; 

Hperrw = Htot/3

Hrw =  irwsolid * rpm

Hrwc = rpm * rho * pi /2*(hr*(rw^4-rdisk^4)+hdisk*rdisk^4)

vmaxsat =  irwsolid * rpmmax / Hperrw;

vmaxgs = 360*vmaxsat/60;

Kmax = (1/2)*(Hrw^2)/irwsolid

