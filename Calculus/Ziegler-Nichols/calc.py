# Ziegler-Nichols

L = 0.625
A = 20

K = 1.2/A
Ti = 2*L
Td = L/2
Tp = 3.4*L

P = K*Tp
I = K*(1/Ti) 
D = K*(1/Td) 
print(P)
print(I)
print(D)