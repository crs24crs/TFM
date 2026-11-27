import numba as nb
import numpy as np
import math
from tqdm import tqdm
from scipy.special import erfinv
import matplotlib.pyplot as plt

from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

def getE_nodes(dx,nx,phi,E):
    # E field
    for i in range(1,nx-1):
        E[i] = -0.5*(phi[i+1]-phi[i-1])/dx
    E[0]  = -0.5*(phi[1]-phi[nx-2])/dx
    E[-1] = -0.5*(phi[1]-phi[nx-2])/dx

def getE_cells(dx,nx,phi,E):
    # E field
    for i in range(nx-1):
        E[i] = - (phi[i+1]-phi[i])/dx

def move_particlesMC(q_m,dt,dx,nx,Np,pos,vel,E):
    for p in range(Np):
        ip = pos[p]
        i  = math.floor(ip)
        
        E0 = E[i]
        E1 = E[i+1]
        w0 = 1 - (ip-i)
        w1 = (ip-i)
        
        Ep = E0*w0+E1*w1
        
        vel[p] += q_m*Ep*dt
        pos[p] += vel[p]*dt/dx
        if vel[p]*dt/dx>1.0:
            print(vel[p]*dt/dx)
        pos[p]  = pos[p] % (nx-1)

def move_particlesMC2(q_m,dt,dx,nx,Np,pos,vel,E):
    E_temp = np.append(E,E[0])
    for p in range(Np):
        ip = (pos[p] - 0.5) % (nx - 1 )
        i  = math.floor( ip )
        
        # E0 = E[i]
        # E1 = E[i+1]
        E0 = E_temp[i]
        E1 = E_temp[i+1]
        w0 = 1 - (ip-i)
        w1 = (ip-i)
        
        Ep = E0*w0+E1*w1
        
        vel[p] += q_m*Ep*dt
        pos[p] += vel[p]*dt/dx
        pos[p]  = pos[p] % (nx-1)

def move_particlesEC(q_m,dt,dx,nx,Np,pos,vel,E):
    for p in range(Np):
        ip = pos[p]
        i  = math.floor(ip)
        
        Ep = E[i]
        
        vel[p] += q_m*Ep*dt
        pos[p] += vel[p]*dt/dx
        pos[p]  = pos[p] % (nx-1)

def get_density(Np,pos,n):
    for p in range(Np):
        ip = pos[p]
        i  = math.floor(ip)
        n[i]   += 1 - (ip-i)
        n[i+1] += (ip-i)
        
    n[0]  += n[-1]
    n[-1]  = 1.0 * n[0]

def get_matrix(dx,nx):
    
    dx2 = dx*dx
    ####################
    # data for sparse matrix
    data = []
    row  = []
    col  = []
    ####################

    # i
    data.append( -2.0 / dx2 ) 
    row.append(0)
    col.append(0)
    # i+1
    data.append( 1.0 / dx2 )
    row.append(0)
    col.append(0+1)
    # i-1
    data.append( 1.0 / dx2 )
    row.append(0)
    col.append(nx-2)
    for i in range(1,nx-1):
        # internal nodes
        # i
        data.append( -2.0 / dx2 )
        row.append(i)
        col.append(i)
        # i+1
        data.append( 1.0 / dx2 )
        row.append(i)
        col.append(i+1)
        # i-1
        data.append( 1.0 / dx2 )
        row.append(i)
        col.append(i-1)        
    '''
    # internal nodes
    # i,j
    data.append( -2 * (1/(dx**2)) )
    row.append(nx-1)
    col.append(nx-1)
    # i+1,j
    data.append( 1/(dx**2) )
    row.append(nx-1)
    col.append(1)
    # i-1,j
    data.append( 1/(dx**2) )
    row.append(nx-1)
    col.append(nx-2)        
    '''     
    # i,j
    data.append( 1 )
    row.append(nx-1)
    col.append(nx-1)
                    
    #####################
    # construct the sparse coefficient matrix
    A = csr_matrix((data,(row,col)), dtype=float,shape=(nx,nx))
    #####################

    return A

me = 9.1093837E-31
mi = 2.1801714E-25
e  = 1.60217663E-19
eps0= 8.8541878188E-12

n  = 1.0E17
Te = 10.0*e
Ti = 1.0*e

omega_pe  = np.sqrt(n*(e**2)/(me*eps0))
l_debye   = np.sqrt(eps0 * Te/(n*e**2))
c_bar_e   = np.sqrt(8*Te/(np.pi * me))

####################
# mesh def.
nx = 201 # number of nodes Ncells + 1
xmin = 0.0
xmax = 10.0E-3
dx = (xmax - xmin)/(nx-1)
x = np.linspace(xmin,xmax,nx)
####################

dt = 1E-12
Nt = 1000

Nppc = 100
Np   = Nppc*(nx-1)
w    = n*dx/Nppc

pos_i = np.zeros(Np)
vel_i = np.zeros(Np)
pos_e = np.zeros(Np)
vel_e = np.zeros(Np)

pos_i[:Np] = (nx-1)*np.random.rand(Np)
vel_i[:Np] = np.sqrt(2.0*Ti/mi)*erfinv(2.0*np.random.rand(Np)-1.0)

pos_e[:Np] = (nx-1)*np.random.rand(Np)
vel_e[:Np] = np.sqrt(2.0*Te/me)*erfinv(2.0*np.random.rand(Np)-1.0)

print(dx/l_debye,dt*omega_pe,c_bar_e*dt/dx)

ne      = np.zeros(nx)
ni      = np.zeros(nx)
phi     = np.zeros(nx)
rhs     = np.zeros(nx)
E_nodes = np.zeros(nx)
E_cells = np.zeros(nx-1)

mom_e = np.zeros(Nt)
mom_i = np.zeros(Nt)
ene_e = np.zeros(Nt)
ene_i = np.zeros(Nt)
ene_f = np.zeros(Nt)

A = get_matrix(dx,nx)
####################
# # rhs vector
# b = np.zeros(nx)
# for i in range(nx):
#     b[i] = np.cos(2.0*np.pi*x[i]/(xmax - xmin))
# b[nx-1] = 0.0 
####################     
            
get_density(Np,pos_e,ne)
get_density(Np,pos_i,ni)
#####################
# solve problem
rhs       = e*(ne-ni)/eps0*w/dx
rhs[nx-1] = 0.0
phi       = spsolve(A,rhs)
#####################
getE_cells(dx,nx,phi,E_cells)
getE_nodes(dx,nx,phi,E_nodes)

# plt.figure()
# plt.plot(x,ne*w/dx)
# plt.plot(x,ni*w/dx)
# plt.plot(x,-e*(ne-ni)*w/dx)

# plt.figure()
# plt.plot(x,phi)

# plt.figure()
# plt.plot(x,E_nodes)

# plt.show()

# plt.figure()
# plt.plot(E_nodes)
# plt.plot(E_cells)
# plt.show()

for t in tqdm(range(Nt)): #
    
    ne = ne*0.0
    ni = ni*0.0

    for i in range(nx-1):
        ene_f[t] += 0.5*eps0*E_cells[i]*E_cells[i]*dx

    for p in range(Np):
        mom_e[t] += me*vel_e[p]
        mom_i[t] += mi*vel_i[p]
        ene_e[t] += 0.5*me*vel_e[p]*vel_e[p]
        ene_i[t] += 0.5*mi*vel_i[p]*vel_i[p] 

    move_particlesMC(-e/me,dt,dx,nx,Np,pos_e,vel_e,E_nodes)
    move_particlesMC(+e/mi,dt,dx,nx,Np,pos_i,vel_i,E_nodes)

    #move_particlesMC2(-e/me,dt,dx,nx,Np,pos_e,vel_e,E_cells)
    #move_particlesMC2(+e/mi,dt,dx,nx,Np,pos_i,vel_i,E_cells)

    #move_particlesEC(-e/me,dt,dx,nx,Np,pos_e,vel_e,E_cells)
    #move_particlesEC(+e/mi,dt,dx,nx,Np,pos_i,vel_i,E_cells)

    get_density(Np,pos_e,ne)
    get_density(Np,pos_i,ni)
    #####################
    # solve problem
    rhs       = e*(ne-ni)/eps0*w/dx
    rhs[nx-1] = 0.0
    phi       = spsolve(A,rhs)
    #####################
    getE_cells(dx,nx,phi,E_cells)
    getE_nodes(dx,nx,phi,E_nodes)

plt.figure()
# plt.plot(mom_e)
# plt.plot(mom_i)
plt.plot( (mom_e + mom_i - (mom_e[0] + mom_i[0])) / (mom_e[0] + mom_i[0]),color='k')

plt.figure()
plt.plot( (ene_e + ene_i + ene_f/w - (ene_e[0] + ene_i[0] + ene_f[0]/w)) / (ene_e[0] + ene_i[0] + ene_f[0]/w),color='k')
#plt.plot(ene_e/e/Np)
#plt.plot(ene_i/e/Np)
#plt.plot(ene_f/e/Np/w)

plt.figure()
plt.plot(ene_e/e/Np)

plt.show()


