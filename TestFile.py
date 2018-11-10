import numpy as np

# L = 10
# T = 10

# Kp = 1.2*T/L
# Ti = 2*L
# Td = 0.5*L

# P = Kp
# I = Kp/Ti
# D = Kp*Td

# print('M1: ' + str(P) + ',' + str(I) + ',' + str(D))


# L = 2.2
# A = 10

# K = 1.2/A
# P = 3.4*L 
# I = K/(2*L) 
# D = K*L/2

# resposta em Frequência
Gr = 2
h = 0.5

#a = (3.68-1.6)/2 #z
#a = (7.88-4.38)/2 #x
#a = (3.078+6.083)/2
#Kcr = (4*Gr/(np.pi*a))*(np.sqrt(1 + (h/a)**2) + h/a)
#Pcr = (80.140-79.91)*2 # z
#Pcr = (66.45-66.69)*2 # x
#Pcr = (62.84-62.641)*2

#z
#Kcr = 3
#Pcr = (22.15-18.79)

#y
#Pcr = (20.052-16.23)

#x
#Pcr= (39.54 - 36.67)

# Kp = 0.6*Kcr
# Ti = 0.5*Pcr
# Td = 0.125*Pcr

# P = Kp
# I = Kp/Ti
# D = Kp*Td


# print('PID: '+str(P) + ',' + str(I) + ',' + str(D))

# Kp = 0.45*Kcr
# Ti = (1/1.2)*Pcr

# P = Kp
# I = Kp/Ti

# print('PI: '+str(P) + ',' + str(I))

#################### test  beteria

# resposta em Frequência
Gr = (1221-1123)/2
h =  4

a = (44.48-35.89)/2 #z
#a = (7.88-4.38)/2 #x
#a = (3.078+6.083)/2
Kcr = (4*Gr/(np.pi*a))*(np.sqrt(1 + (h/a)**2) + h/a)
Pcr = (38.18-35.21) # z
#Pcr = (66.45-66.69)*2 # x
#Pcr = (62.84-62.641)*2

#z
#Kcr = 3
#Pcr = (22.15-18.79)

#y
#Pcr = (20.052-16.23)

#x
#Pcr= (39.54 - 36.67)

Kp = 0.6*Kcr
Ti = 0.5*Pcr
Td = 0.125*Pcr

P = Kp
I = Kp/Ti
D = Kp*Td


print('PID: '+str(P/(P/2)) + ',' + str(I/(P/2)) + ',' + str(D/(P/2)))

Kp = 0.45*Kcr
Ti = (1/1.2)*Pcr

P = Kp
I = Kp/Ti

print('PI: '+str(P) + ',' + str(I))


#################### test  sem beteria

# resposta em Frequência
Gr = (1221-1123)/2
h =  4

a = (45-38.1)/2 #z
#a = (7.88-4.38)/2 #x
#a = (3.078+6.083)/2
Kcr = (4*Gr/(np.pi*a))*(np.sqrt(1 + (h/a)**2) + h/a)
Pcr = (32.79-29.97) # z
#Pcr = (66.45-66.69)*2 # x
#Pcr = (62.84-62.641)*2

#z
#Kcr = 3
#Pcr = (22.15-18.79)

#y
#Pcr = (20.052-16.23)

#x
#Pcr= (39.54 - 36.67)

Kp = 0.6*Kcr
Ti = 0.5*Pcr
Td = 0.125*Pcr

P = Kp
I = Kp/Ti
D = Kp*Td


print('PID: '+str(P) + ',' + str(I) + ',' + str(D))

Kp = 0.45*Kcr
Ti = (1/1.2)*Pcr

P = Kp
I = Kp/Ti

print('PI: '+str(P) + ',' + str(I))