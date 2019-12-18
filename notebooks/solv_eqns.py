# %%
import numpy as np
import scipy.integrate as integrate
from matplotlib import pyplot as plt
from scipy.integrate import odeint
import pandas as pd

import pdb
pdb.set_trace()

# %%
def solve_equations(P,t, Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, Q_bl, q_sfc, q_ft, q_bl, LCL):
    F_theta = Cd*V*(theta_sfc -P[0])
    #w_e = A*(Cd*V*(theta_sfc-P[0]) + epsilon*P[0]*Cd*V*(q_sfc - P[1]))/((theta_0 + Gamma*P[2])*(1 + epsilon*q_ft)- P[0])
    
    #delta_theta = theta_0 + Gamma*P[2] - P[0]
    delta_theta=0
    
    #delta_q = q_ft - P[1]
    delta_q=0
    
    F_q = Cd*V*(q_sfc - P[1])
    delta_theta_v = (theta_0 + Gamma*P[2])*(1 + epsilon*q_ft)- P[0]
    F_B = F_theta + epsilon*P[0]*F_q
    w_e = A*F_B/delta_theta_v
    w_FT = Q_ft/Gamma
    w_m = 0 #dry model
    #w_m = (-P[2]-LCL)/tau
    
    #
    # EQUATIONS
    #
    P[0] = Q_bl + (1/P[2])*(w_e*delta_theta + F_theta)
    P[1] = (1/P[2])*(w_e*delta_q + F_q)
    P[2] = w_FT + w_e + w_m

    return(P[0], P[1], P[2], delta_theta)

# %%
#
# INPUTS
#
Q_ft = -1.0 #K day^-1
Gamma = 5.0 #K km^-1
theta_0 = 298 #K
theta_sfc = 301 #K
A = 0.41
Cd = 0.001
V = 5 #m/s
tau = 15 #min
epsilon = 0.61
#var_init = []

theta_sfc = 302 #K GUESS
Q_bl = -1

#
# set up solution for ODEs
#
tf = 6*24*3600
dtout = 600
tspan = np.arange(0.,tf,dtout)

dz = 10.
ztop = 1000.
zf = np.arange(0.,ztop,dz)

# dtout=30.  #minutes
# tf=48   #hours
# dtout=dtout*60.
# tf=tf*3600.
# tspan = np.arange(0.,tf,dtout)

#Q_bl = [-1, -2, -3, -4, -5, -6]
#Q_bl = [-1]
P0 = [250, -1, 400, 0.1]

#
# GUESSES
#
q_sfc = 0.25
q_ft = 3 #free-tropospheric water vapour mixing ratio just above the BL inversion
q_bl = 8
LCL = 5000

prof1 = odeint(solve_equations, P0, tspan, (Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, -1, q_sfc, q_ft, q_bl, LCL))
prof3 = odeint(solve_equations, P0, tspan, (Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, -3, q_sfc, q_ft, q_bl, LCL))
prof5 = odeint(solve_equations, P0, tspan, (Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, -5, q_sfc, q_ft, q_bl, LCL))
#prof1 = prof1.T
prof1.shape


# %%
#
# PLOT
#
zh = np.arange(0,1000,1000/4)
zh.shape
#zh = np.arange(dz/2,(ztop-dz/2),dz)

fig,ax = plt.subplots(1,1,figsize=(8,8))
for item in prof1:
    ax.plot(item, zh)
plt.show()
prof1.shape

# %%
#Q_bl = [1, 2, 3, 4, 5, 6]
plt.plot(tspan/(24*3600), prof1[:,0], 'b', label = 'Q_bl = -1');
plt.plot(tspan/(24*3600), prof3[:,0], 'g', label = 'Q_bl = -3');
plt.plot(tspan/(24*3600), prof5[:,0], 'm', label = 'Q_bl = -5');
plt.legend();
plt.xlabel('Time [days]');
plt.ylabel('theta BL [K]');


# %%
def make_prof(df_out,gamma):
    #
    #  construct a vertical (theta, height) profile with the correct Delta theta jump
    #  using four points
    #
    profile=[(df_out['theta'],0),
             (df_out['theta'],df_out['h']),
             (df_out['theta'] + df_out['deltheta'],df_out['h']),
             (df_out['theta'] + df_out['deltheta'] + gamma*0.2*df_out['h'],1.2*df_out['h'])]
    xvals=[item[0] for item in profile]
    yvals=[item[1] for item in profile]
    return xvals,yvals

result=pd.DataFrame.from_records(prof1,columns=['theta','q_bl','h', 'deltheta'])
result['time']=tspan/24./3600.
out=result.to_dict(orient='records')

fig,ax = plt.subplots(1,1,figsize=(10,10))
for count,row in enumerate(out):
    if np.mod(count,3) == 0:
        thetavals,heightvals=make_prof(row,Gamma)
        ax.plot(thetavals,heightvals)
        
out=ax.set(xlabel=r'$\theta (K)$',ylabel='height (m)',
           title=(f'Single column moist model '
                  f'$Q_BL = {-1} K/day$ and $\Gamma$={Gamma} K/km'))
ax.grid(True,which='both')

# %%
#print(prof1[1:])
theta_bl = prof1[:,0]
q_bl = prof1[:,1]
height_bl = prof1[:,2]
#theta_bl.shape
#print(theta_bl)

plt.plot(tspan/(24*3600), theta_bl, 'b', label = 'Q_bl = -1');
#plt.plot(tspan/(24*3600), prof3[:,0], 'g', label = 'Q_bl = -3');

# %%
fig,ax=plt.subplots(1,1,figsize=(10,8))
for i2 in range(0,864):
    x4 = theta_bl[i2]
    y4 = height_bl[i2]
    ax.plot(x4,y4)
ax.set(xlabel=r'theta (K)',ylabel='height (m)',title = ' ');

# %%

# %%
# mean theta 
mean_theta = np.empty_like(prof1[0:,0])
mean_theta[0] = prof1[0,0]
inv_height = np.empty_like(prof1[0:,2])
inv_height[0] = prof1[0,2]
q_bl = np.empty_like(prof1[0:,1])
q_bl[0] = prof1[0,1]

for i in range(1,18):
    mean_theta[i] = prof1[i,0]+prof1[0,0]
    q_bl[i] = prof1[i,1]+prof1[0,1]
    inv_height[i] = prof1[i,2]+prof1[0,2]

# %%
fig,ax=plt.subplots(1,1,figsize=(10,8))
for i2 in range(0,864):
    x4 = mean_theta[i2]+Gamma*0.5*inv_height[i2]
    y4 = inv_height[i2]*1.5
    ax.plot([mean_theta[i2],mean_theta[i2], mean_theta[i2],x4],
         [0,inv_height[i2],inv_height[i2],y4])
ax.set(xlabel=r'$\overline{\theta}$ (K)',ylabel='height (m)',title = ' ');

# %%
fig,ax=plt.subplots(1,1,figsize=(10,8))
ax.plot((tspan/3600),inv_height, label = "mixed layer model")
#ax.plot(dry_les_time*10, dry_les_inv, label = "dry LES model")
ax.set(xlabel='Time (hours)',ylabel='Height (m)',
       title = 'Time history of boundary layer heights');
ax.legend();

# %%
