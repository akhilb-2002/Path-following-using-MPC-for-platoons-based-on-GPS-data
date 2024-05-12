import casadi as cas

def check(x):
    return x[0][0]*x[1][0]

Ainit= [1,1]
Binti= [1,1]
Qvalue= [[1,1],[1,1]]
opti = cas.Opti()
# Create a CasADi matrix variable (example)
A=opti.variable(2,1)
B=opti.variable(2,1)
B[0]=A[0]+2


Q=cas.DM(Qvalue)
R=cas.DM(Q)

f=A.T@Q@A+B.T@R@B

opti.set_initial(A,Ainit)

opti.minimize(f)

p=A
opti.subject_to(check(p)<=0)

opti.solver('ipopt')

sol = opti.solve()
print(sol.value(A))
print(sol.value(B))
print(sol.value(f))


