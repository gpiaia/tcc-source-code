%% Calculo dasa Dimensões roda de reação 
clc
clear

Isat = 0.5; %kg*m^2 -> Solidworks
rpm = 2200; % rotação de posição estática -> menor velocidade e menor ruído
rpmmax = 26500;
s = 0.2; %distância entre os motores
m = 1.22; %Massa do satélite

rho = 7860; % Densidade do aço
hr = 10.5/1000; % espessuda do disco: valor que procuro
hdisk = 2/1000; % espessura dos raios da roda de reação
rdisk =  30/1000; %Raio interno da roda de reação desenhada
rw = 37/1000; % Raio da roda de reação desenhada
irwsolid =  157755.02/(1000*1000*1000); % Momento de inércia fornecido pelo Solidworks da roda de reação

%wrw = 2*pi*rpm/60; % Velocidade angular da roda de reação

Htot = 2*(Isat + m*(s/2)^2)*1; 

Hperrw = Htot/3

Hrw =  irwsolid * rpm

Hrwc = rpm * rho * pi /2*(hr*(rw^4-rdisk^4)+hdisk*rdisk^4)

vmaxsat =  irwsolid * rpmmax / Hperrw;

vmaxgs = 360*vmaxsat/60;

Kmax = (1/2)*(Hrw^2)/irwsolid

%% Calculo dasa Dimensões roda de reação 
clc
clear

Isat = 0.5; %kg*m^2 -> Solidworks
rpm = 2200; % rotação de posição estática -> menor velocidade e menor ruído
rpmmax = 26500;
s = 0.2; %distância entre os motores
m = 1.22; %Massa do satélite

rho = 7860; % Densidade do aço
hr = 30/1000; % espessuda do disco: valor que procuro
hdisk = 2/1000; % espessura dos raios da roda de reação
rdisk =  14.2/1000; %Raio interno da roda de reação desenhada
rw = 26/1000; % Raio da roda de reação desenhada
irwsolid =  157755.02/(1000*1000*1000); % Momento de inércia fornecido pelo Solidworks da roda de reação

%wrw = 2*pi*rpm/60; % Velocidade angular da roda de reação

Htot = 2*(Isat + m*(s/2)^2)*1; 

Hperrw = Htot/3

Hrw =  irwsolid * rpm

Hrwc = rpm * rho * pi /2*(hr*(rw^4-rdisk^4)+hdisk*rdisk^4)

vmaxsat =  irwsolid * rpmmax / Hperrw;

vmaxgs = 360*vmaxsat/60;

Kmax = (1/2)*(Hrw^2)/irwsolid

