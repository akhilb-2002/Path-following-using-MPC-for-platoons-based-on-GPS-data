import numpy as np
import casadi

def xdotstep(Ts:float, xdotnow:float, Fxf:float, Fxr:float, Fyf:float, delta:float, Cd:float, A:float, rho:float, m:float,ydotnow:float, phidotnow:float):
    xdotnext = xdotnow + Ts*((ydotnow*phidotnow+ 2*Fxf*np.cos(delta)-2*Fyf*np.sin(delta)+Fxr)/m - (Cd*rho*A*xdotnow**2)/(2*m))
    return xdotnext

def ydotstep(Ts:float, ydotnow:float, Fxf:float, Fyf:float, Fyr:float, delta:float, m:float,xdotnow:float, phidotnow:float):
    ydotnext = ydotnow + Ts*((2*Fxf*np.sin(delta)+2*Fyf*np.cos(delta) -  xdotnow*phidotnow)/m + 2*Fyr/m)
    return ydotnext

def phidotstep(Ts:float, phidotnow:float, Fxf:float, Fyf:float, Fyr:float, a:float, b:float, delta:float, Jvehicle:float):
    phidotnext = phidotnow + Ts*((a*Fyf*np.cos(delta)+a*Fxf*np.sin(delta))/Jvehicle - (b*Fyr)/Jvehicle)
    return phidotnext

def Xstep(Ts:float, Xnow:float, xdot:float, ydot:float, phi:float):
    Xnext = Xnow + Ts*(xdot*np.cos(phi)-ydot*np.sin(phi))
    return Xnext

def Ystep(Ts:float, Ynow:float, xdot:float, ydot:float, phi:float):
    Ynext = Ynow + Ts*(xdot*np.sin(phi)+ydot*np.cos(phi))
    return Ynext

def phistep(Ts:float, phinow:float, phidot:float):
    phinext = phinow + Ts*phidot
    return phinext

        
#parameters in order -> m,A,rho,Cd,Jveh,a,b
def stepoverall(Ts:float, otherstates:np.array,N:int,inputs:np.array, parameters:np.array):

    m = parameters[0]
    A = parameters[1]
    rho = parameters[2]
    Cd = parameters[3]
    Jveh = parameters[4]
    a = parameters[5]
    b = parameters[6]
    
    X=casadi.MX.zeros(N,1)
    Y=casadi.MX.zeros(N,1)
    xdot=casadi.MX.zeros(N,1)
    ydot=casadi.MX.zeros(N,1)
    phi=casadi.MX.zeros(N,1)
    phidot=casadi.MX.zeros(N,1)

    for i in range(0,N):
        X[i] = otherstates[6*i]
        Y[i] = otherstates[6*i+1]
        xdot[i] = otherstates[6*i+2]
        ydot[i] = otherstates[6*i+3]
        phi[i] = otherstates[6*i+4]
        phidot[i] = otherstates[6*i+5]

    Xnext = casadi.MX.zeros(N,1)
    Ynext = casadi.MX.zeros(N,1)
    xdotnext = casadi.MX.zeros(N,1)
    ydotnext = casadi.MX.zeros(N,1)
    phinext = casadi.MX.zeros(N,1)
    phidotnext = casadi.MX.zeros(N,1)

    for i in range(0,N):
        Fxf = inputs[5*i]
        Fxr = inputs[5*i+1]
        Fyf = inputs[5*i+2]
        Fyr = inputs[5*i+3]
        delta = inputs[5*i+4]
        
        xdotnext[i] = xdotstep(Ts,xdot[i],Fxf,Fxr,Fyf,delta,Cd,A,rho,m,ydot[i],phidot[i])
        ydotnext[i] = ydotstep(Ts,ydot[i],Fxf,Fyf,Fyr,delta,m,xdot[i],phidot[i])
        phidotnext[i] = phidotstep(Ts,phidot[i],Fxf,Fyf,Fyr,a,b,delta,Jveh)
        
        Xnext[i] = Xstep(Ts,X[i],xdotnext[i],ydotnext[i],phi[i])
        Ynext[i] = Ystep(Ts,Y[i],xdotnext[i],ydotnext[i],phi[i])
        phinext[i] = phistep(Ts,phi[i],phidotnext[i])

    otherstatesnext = casadi.MX.zeros(6*N,1)
 
    for i in range(0,N):
        otherstatesnext[6*i] = Xnext[i]
        otherstatesnext[6*i+1] = Ynext[i]
        otherstatesnext[6*i+2] = xdotnext[i]
        otherstatesnext[6*i+3] = ydotnext[i]
        otherstatesnext[6*i+4] = phinext[i]
        otherstatesnext[6*i+5] = phidotnext[i]


    return otherstatesnext



