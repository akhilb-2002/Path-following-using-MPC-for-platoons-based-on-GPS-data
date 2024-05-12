import numpy as np
import sys
sys.path.append('/path/to/directory')


def Tmin(Fxfmin:float, Fxrmin:float, Fyfmin:float,Fyrmin:float,deltafmin:float,N:int):
    Tmin = np.zeros((5*N,1),dtype=float)     
    for i in range(0,N):
        Tmin[5*i] = Fxfmin
        Tmin[5*i+1] = Fxrmin
        Tmin[5*i+2] = Fyfmin
        Tmin[5*i+3] = Fyrmin
        Tmin[5*i+4] = deltafmin
    return Tmin

def Tmax(Fxfmax:float, Fxrmax:float, Fyfmax:float,Fyrmax:float,deltafmax:float,N:int):
    Tmax = np.zeros((5*N,1),dtype=float)    
    for i in range(0,N):
        Tmax[5*i] = Fxfmax
        Tmax[5*i+1] = Fxrmax
        Tmax[5*i+2] = Fyfmax
        Tmax[5*i+3] = Fyrmax
        Tmax[5*i+4] = deltafmax
    return Tmax

# Cmin<=MX
# Cmin -> 2(N-1) x 1
# M -> 2(N-1) x (6*N+2)
# X -> (6*N+2)x 1
def M(N:int):
    M = np.zeros((2*(N-1),6*N+2),dtype=float)
    for i in range(0,N-1):
        M[2*i][6*i] = 1
        M[2*i][6*i+6] = -1
        M[2*i+1][6*i+1] = 1
        M[2*i+1][6*i+7] = -1
    
    return M

def Cmin(epsilonmin:float,deltamin:float,N:int)-> np.array:
    Cmin = np.zeros((2*N-2,1),dtype=float)
    for i in range(0,N-1):
        Cmin[2*i] = epsilonmin
        Cmin[2*i+1] = deltamin
    return Cmin

    

# checks if the entire platoon is in the route
# Xcoord is the list of x coordinates of the platoon
# Ycoord is the list of y coordinates of the platoon
# N is the number of vehicles in the platoon    
def checkoncurve(Xcoord:list,Ycoord:list,N:int,R:float):
    # R is the radius of curvature of the route
    checksum=0
    for i in range(0,N):
        if (Xcoord[i]**2 + (Ycoord[i])**2 == R**2):
            checksum=checksum+1

    return checksum
        #If checksum=N, then all vehicles are on the curve
    
def phidotcheck(phidotlist:list,xdotlist:list,N:int,R:float):
    checksum=0
    for i in range(0,N):
        if (phidotlist[i]*R==xdotlist[i]):
            checksum=checksum+1

    return checksum
        #If checksum=N, then all vehicles are on the curve in the right direction


