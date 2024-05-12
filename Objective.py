# ENTIRE FILE GIVES THE TOTAL ERROR AT A GIVEN TIME STEP

import numpy as np
import sys
sys.path.append('/path/to/directory')

# Returns the control cost matrix, R[k], at A GIVEN TIME STEP
def R(wtor:float,wsteer:float,N:int):
    R = np.zeros((5*N,5*N),dtype=float)
    
    for i in range(0,N):
        R[5*i][5*i] = wtor
        R[5*i+1][5*i+1] = wtor
        R[5*i+2][5*i+2] = wtor
        R[5*i+3][5*i+3] = wtor
        R[5*i+4][5*i+4] = wsteer
    
    return R

# N is the number of vehicles in the platoon
# Ratk is the list of radii of curvature of each vehicle in the platoon(1-leader,2-follower,3-follower,...) ----> will get from Route.py
# Returns the state cost matrix, Q[k], at A GIVEN TIME STEP
def Q(wvr:float,wv:float,wtrack:float,wangle:float,N:int):
    Q = np.zeros((9*N+2,9*N+2),dtype=float)
    
    # Coefficient of Xi^2, Yi^2, phi^2
    for i in range(0,N):
        Q[9*i][9*i] = wtrack
        Q[9*i+1][9*i+1] = wtrack
        Q[9*i+4][9*i+4] = wangle

    #Coefficient of Xi,Xref
    for i in range(0,N):
        Q[9*i][9*i+6] = -wtrack
        Q[9*i+6][9*i] = -wtrack
    
    #Coefficient of Yi,Yref
    for i in range(0,N):
        Q[9*i+1][9*i+7] = -wtrack
        Q[9*i+7][9*i+1] = -wtrack

    #Coefficient of phii,phiref
    for i in range(0,N):
        Q[9*i+4][9*i+8] = -wangle
        Q[9*i+8][9*i+4] = -wangle

    #Coefficient of Xref^2,Yref^2,phiref^2
    for i in range(0,N):
        Q[9*i+6][9*i+6] = wtrack
        Q[9*i+7][9*i+7] = wtrack
        Q[9*i+8][9*i+8] = wangle

    #Coefficient of xdot1^2,xdotN^2
    Q[2][2]=wv+wvr
    Q[9*N-7][9*N-7]=wv

    #Coefficient of ydot1^2,ydotN^2
    Q[3][3]=wv+wvr
    Q[9*N-6][9*N-6]=wv

    #Coefficient of xdot1,xdotref
    Q[2][9*N]=-wvr
    Q[9*N][2]=-wvr

    #Coefficient of ydot1,ydotref
    Q[3][9*N+1]=-wvr
    Q[9*N+1][3]=-wvr

    #Coefficient of xdotref^2
    Q[9*N][9*N]=wvr

    #Coefficient of ydotref^2
    Q[9*N+1][9*N+1]=wvr

    #Coefficient of xdoti^2
    for i in range(1,N-1):
        Q[9*i+2][9*i+2]=2*wv

    #Coefficient of ydoti^2
    for i in range(1,N-1):
        Q[9*i+3][9*i+3]=2*wv

    #Coefficient of xdoti,xdoti+1
    for i in range(0,N-1):
        Q[9*i+2][9*i+11]=-wv
        Q[9*i+11][9*i+2]=-wv

    #Coefficient of ydoti,ydoti+1
    for i in range(0,N-1):
        Q[9*i+3][9*i+12]=-wv
        Q[9*i+12][9*i+3]=-wv

    
    return Q
        

