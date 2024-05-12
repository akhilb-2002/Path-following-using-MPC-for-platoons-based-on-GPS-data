import numpy as np
import casadi 

# Local velocity along x-axis prediction
def xdotstep(Ts: float,xdotnow: float, Fxfr: float, Fxfl: float, Fxrr: float, Fxrl: float,Fyfl:float,Fyfr:float,m: float,Cd: float,rho: float,Afront: float,delta:float, ydot:float,phidot:float)->float :
    xdotnext = xdotnow + Ts*((Fxfr+Fxfl)*np.cos(delta)/m  - (Fyfr+Fyfl)*np.sin(delta)/m + (Fxrr+Fxrl)/m - (Cd*rho*Afront*xdotnow**2)/(2*m) + ydot*phidot)
    return xdotnext

# Local velocity along y-axis prediction
def ydotstep(Ts: float,ydotnow: float, Fyfr: float, Fyfl: float, Fyrr: float, Fyrl: float,Fxfl:float,Fxfr:float,m: float,Cd: float,rho: float,Aside: float,delta:float, xdot:float,phidot:float)->float :
    ydotnext = ydotnow + Ts*((Fyfr+Fyfl)*np.cos(delta)/m + (Fyrr+Fyrl)/m - (Fxfr+Fxfl)*np.sin(delta)/m - (Cd*rho*Aside*ydotnow**2)/(2*m) - xdot*phidot)
    return ydotnext

# Local angular velocity prediction
def phidotstep(Ts: float, phidotnow: float, Fyfr: float, Fyfl: float, Fyrr: float, Fyrl: float,Fxfl:float,Fxfr:float,m: float,Cd: float,rho: float,Aside: float,delta:float, xdot:float,ydot:float,J:float,a:float, b:float)->float :
    #phidotnext = phidotnow + Ts*((a*Fxfl+a*Fxfr)*np.sin(delta)/J + (a*Fyfl+a*Fyfr)*np.cos(delta)/J - (Cd*rho*Aside*a*ydot**2)/(4*J) + (Cd*rho*Aside*b*ydot**2)/(4*J) - (b*Fyrl+b*Fyrr)/J)
    phidotnext = phidotnow + Ts*((a*Fxfl+a*Fxfr)*np.sin(delta)/J + (a*Fyfl+a*Fyfr)*np.cos(delta)/J  - (b*Fyrl+b*Fyrr)/J)
    return phidotnext

# Angular velocity of each wheel prediction
def wistep(Ts: float, wflnow: float,wfrnow:float,wrlnow:float,wrrnow:float, Tfl:float ,Tfr:float,Trl:float,Trr:float, Cx:float, Jtire:float,Rtire:float,xdot:float):
    wflnext = wflnow + Ts*(Tfl/Jtire - Cx*(Rtire*wflnow/xdot-1)*Rtire/Jtire)
    wfrnext = wfrnow + Ts*(Tfr/Jtire - Cx*(Rtire*wfrnow/xdot-1)*Rtire/Jtire)
    wrlnext = wrlnow + Ts*(Trl/Jtire - Cx*(Rtire*wrlnow/xdot-1)*Rtire/Jtire)
    wrrnext = wrrnow + Ts*(Trr/Jtire - Cx*(Rtire*wrrnow/xdot-1)*Rtire/Jtire)
    
    output= np.array([wflnext,wfrnext,wrlnext,wrrnext])
    return output

# Local angular position prediction
def phistep(Ts: float,phinow: float, phidot: float)->float :
    phinext = phinow + Ts*phidot
    return phinext

# Global position along x-axis prediction
def Xstep(Ts: float,Xnow: float, xdot: float,ydot:float, phi:float)->float :
    Xnext = Xnow + Ts*(xdot*np.cos(phi)-ydot*np.sin(phi))
    return Xnext

# Global position along y-axis prediction
def Ystep(Ts: float,Ynow: float, xdot: float,ydot:float, phi:float)->float :
    Ynext = Ynow + Ts*(xdot*np.sin(phi)+ydot*np.cos(phi))
    return Ynext

# Forces on each wheel prediction
def forces(delta: float, Rtire:float,xdot:float,ydot:float,a:float,b:float,phidot:float,Cx:float,Cy:float):
    Fxfl = Cx*(Rtire*phidot/xdot-1)
    Fxfr = Cx*(Rtire*phidot/xdot-1)
    Fxrl = Cx*(Rtire*phidot/xdot-1)
    Fxrr = Cx*(Rtire*phidot/xdot-1)
   
    Fyfl = Cy*(delta - (ydot+phidot*a)/xdot)
    Fyfr = Cy*(delta - (ydot+phidot*a)/xdot)
    Fyrl = Cy*(-(ydot-phidot*b)/xdot)
    Fyrr = Cy*(-(ydot-phidot*b)/xdot)

    output=np.array([Fxfl,Fxfr,Fxrl,Fxrr,Fyfl,Fyfr,Fyrl,Fyrr])

    return output

# Overall step prediction for each vehicle in the platoon
# States-> X,Y,phi,xdot,ydot,phidot,wfl,wfr,wrfl,wrr
# Input-> Tfl,Tfr,Trl,Trr,delta
# Parameters-> m,Cd,rho,Afront,Aside,J,a,b,Cx,Cy,Jtire,Rtire

def step(Ts: float,states: np.array,inputs: np.array,parameters: np.array,phiini:float,R:float):
    # States
    X = states[0]
    Y = states[1]
    xdot = states[2]
    ydot = states[3]
    phidot = states[4]
    wfl = states[5]
    wfr = states[6]
    wrl = states[7]
    wrr = states[8]
    # Inputs
    Tfl = inputs[0]
    Tfr = inputs[1]
    Trl = inputs[2]
    Trr = inputs[3]
    delta = inputs[4]
    # Parameters
    m = parameters[0]
    Cd = parameters[1]
    rho = parameters[2]
    Afront = parameters[3]
    Aside = parameters[4]
    J = parameters[5]
    a = parameters[6]
    b = parameters[7]
    Cx = parameters[8]
    Cy = parameters[9]
    Jtire = parameters[10]
    Rtire = parameters[11]

    # First, update angular velocities of wheels
    wflnext= wistep(Ts,wfl,wfr,wrl,wrr,Tfl,Tfr,Trl,Trr,Cx,Jtire,Rtire,xdot)[0]
    wfrnext= wistep(Ts,wfl,wfr,wrl,wrr,Tfl,Tfr,Trl,Trr,Cx,Jtire,Rtire,xdot)[1]
    wrlnext= wistep(Ts,wfl,wfr,wrl,wrr,Tfl,Tfr,Trl,Trr,Cx,Jtire,Rtire,xdot)[2]
    wrrnext= wistep(Ts,wfl,wfr,wrl,wrr,Tfl,Tfr,Trl,Trr,Cx,Jtire,Rtire,xdot)[3]

    # Also, update forces on each wheel
    Fxfl = forces(delta,Rtire,xdot,ydot,a,b,phidot,Cx,Cy)[0]
    Fxfr = forces(delta,Rtire,xdot,ydot,a,b,phidot,Cx,Cy)[1]
    Fxrl = forces(delta,Rtire,xdot,ydot,a,b,phidot,Cx,Cy)[2]
    Fxrr = forces(delta,Rtire,xdot,ydot,a,b,phidot,Cx,Cy)[3]
    Fyfl = forces(delta,Rtire,xdot,ydot,a,b,phidot,Cx,Cy)[4]
    Fyfr = forces(delta,Rtire,xdot,ydot,a,b,phidot,Cx,Cy)[5]
    Fyrl = forces(delta,Rtire,xdot,ydot,a,b,phidot,Cx,Cy)[6]
    Fyrr = forces(delta,Rtire,xdot,ydot,a,b,phidot,Cx,Cy)[7]

    # Next, update local velocities, angular velocities
    xdotnext = xdotstep(Ts,xdot,Fxfr,Fxfl,Fxrr,Fxrl,Fyfl,Fyfr,m,Cd,rho,Afront,delta,ydot,phidot)
    ydotnext = ydotstep(Ts,ydot,Fyfr,Fyfl,Fyrr,Fyrl,Fxfl,Fxfr,m,Cd,rho,Aside,delta,xdot,phidot)

    # Next, update local angular velocity
    #phidotnext = phidotstep(Ts,phidot,Fyfr,Fyfl,Fyrr,Fyrl,Fxfl,Fxfr,m,Cd,rho,Aside,delta,xdotnext,ydotnext,J,a,b)
    phidotnext = xdotnext/R

    # Global position predictions, angular position predictions
    phinext = phistep(Ts,phiini,phidot)
    Xnext = Xstep(Ts,X,xdot,ydot,phiini)
    Ynext = Ystep(Ts,Y,xdot,ydot,phiini)
    
    statesnext= casadi.MX.zeros(9,1) 
    # Statesnext has to be a casadi matrix

    statesnext= casadi.vertcat(Xnext,Ynext,xdotnext,ydotnext,phidotnext,wflnext,wfrnext,wrlnext,wrrnext)

    return statesnext,phinext

# Overall step prediction for entire platoon

def stepoverall(Ts, ubarnow, xbarnow, parameters, phiniforall, R,N):
    xbarnext = casadi.MX.zeros(11 * N, 1)
    phinext = casadi.MX.zeros(N, 1)
    #xbarnext = np.zeros((11 * N, 1), dtype=float)
    #phinext = np.zeros((N, 1), dtype=float)
    
    for i in range(0, N):
        states = xbarnow[9 * i:9 * i + 9]
        inputs = ubarnow[5 * i:5 * i + 5]
        dumarray = step(Ts, states, inputs, parameters, phiniforall[i][0],R)[0]
        
        for j in range(0, 9):
            xbarnext[9 * i + j] = dumarray[j]
        
        phinext[i] = step(Ts, states, inputs, parameters, phiniforall[i][0],R)[1]
    
    for i in range(0, N - 1):
        xbarnext[9 * N + 2 * i] = xbarnow[9 * N + 2 * i]
        xbarnext[9 * N + 2 * i + 1] = xbarnow[9 * N + 2 * i + 1]
    
    xbarnext[11 * N - 2] = xbarnow[11 * N - 2]
    xbarnext[11 * N - 1] = xbarnow[11 * N - 1]
    
    return xbarnext, phinext

