%--------------------------------------------------------------------------
% Atividade Acadêmica de Controle Moderno - 2018/1 Prof. Samuel Lessinger
% Laboratório 1
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Inicialização do script
%--------------------------------------------------------------------------
format shorteng    % Define formato curto de dados
clear
clc             % Limpa todos os dados da tela

%--------------------------------------------------------------------------

load('C:\Users\Gpiaia\Google Drive\Eng. de Controle e Automacao\TCC\Code\Calculus\Matlab\ModeloSatelite.mat')

K = 0.002;
IX = 6645861.83/10^9;
IY = 12785011.68/(10^9);
IZ = 6645861.83/10^9;

Ra = 0.225;
La = 74.4*10^-6;

Kw = 60*2*pi/2200;
Kt = Kw/0.00684;

I = 1;
Bm = Kt*I/2200;
Br = Bm;
Jm = 16307/10^9;
Jr = 163076/10^9;

cimotor_11 = 0;
cimotor_12 = 0;
cimotor_13 = 0; 
cimotor_14 = 0;

ciobserv_11 = 0;
ciobserv_12 = 0;
ciobserv_13 = 0;
ciobserv_14 = 0;

%--------------------------------------------------------------------------
% Define as matrizes
%-------------------------------------------------------------------------

A = ModeloSatelite.A

B = ModeloSatelite.B

C = ModeloSatelite.C

D = ModeloSatelite.D
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Posto da matriz do sistema
%--------------------------------------------------------------------------
disp('Posto da matriz do sistema');
PA = rank(A)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Autovalores da matriz do sistema
%--------------------------------------------------------------------------
disp('Autovalores da matriz do sistema');
AVA = eig(A)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Observalidade da Matriz
%--------------------------------------------------------------------------
disp('Observalidade');
OB = obsv(A, C)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Controlabilidade da Matriz
%--------------------------------------------------------------------------
disp('Controlabilidade');
CTRL = ctrb(A, B)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Posto da matriz de observabilidade
%--------------------------------------------------------------------------
disp('Posto da matriz de observabilidade');
POB = rank(OB)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Posto da matriz de controlabilidade
%--------------------------------------------------------------------------
disp('Posto da matriz de controlabilidade');
PCTRL = rank(CTRL)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Projeto do LQR
%--------------------------------------------------------------------------
disp('LQR')
%Q = [1   0
%     0   1];
%Q = [1  1
%     0  0];
%Q = [1  1
%     1  1];
Q = C'*C;

R = [1];

[kc] = lqr(A, B, Q, R)
%--------------------------------------------------------------------------
% Determinação do compensador estático de referência (matriz F)
%--------------------------------------------------------------------------
G = (C*inv((-(A-B*kc)))*B);
F = inv(G)
%--------------------------------------------------------------------------
%--------------------------------------------------------------------------
% Projeto do LQG
%--------------------------------------------------------------------------
disp('LQG')
qw = [1 0 0 0
      0 1 0 0
      0 0 1 0
      0 0 0 1];

rv = [1];

S = care(A',C', qw, rv);
L = S*C'*inv(rv)
%--------------------------------------------------------------------------