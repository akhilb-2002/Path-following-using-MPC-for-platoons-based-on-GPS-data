import sys
sys.path.append('/path/to/directory')
import Objective
import Prediction
import numpy as np
import csv

N=2

# Vehicle parameters
m=2000
Cd=0.3
rho=1.225
Afront=2.2
Aside=1.5
Jvehicle=3000
a=1.5
b=1.5
Cx=1.2
Cy=1.2
Jtire=10
Rtire=0.3


parameters = [m,Cd,rho,Afront,Aside,Jvehicle,a,b,Cx,Cy,Jtire,Rtire]
x1=[0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,2,2,1,1]#Size 22



phiiniforall=np.zeros((N,1),dtype=float)

udummy=np.array([100,100,100,100,10,100,100,100,100,10])#Size 10

xnext =Prediction.stepoverall(0.1,udummy,x1,parameters,phiiniforall,N)

print(xnext)

import casadi as ca

# Create a 9x1 matrix filled with zeros
statesnext = ca.MX.zeros(9, 1)

print(statesnext)
# Change the value of statesnext[0][0]
statesnext = ca.vertcat(1,2,3,4,5,6,7,8,9)  # Replace 'new_value' with the value you want to set

print(statesnext) 