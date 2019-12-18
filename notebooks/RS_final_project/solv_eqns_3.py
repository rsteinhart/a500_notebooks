# %% [markdown]
# # 1D !!MOIST!! column with LCL

# %%
import numpy as np
import scipy.integrate as integrate
from matplotlib import pyplot as plt
from scipy.integrate import odeint
import pandas as pd
from LCL_calc import calc_lcl
import constants as c

#import pdb
#pdb.set_trace()

# %% [markdown]
# #### Solving the system of equations for the 1D dry moisture model
# Humidity and diagnostic jump removed and LCL is high, dry column

# %%
def solve_equations(P,t, Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, Q_bl, q_sfc, q_ft, q_bl, LCL):
    
    r=8 # GUESS
    thetav_BL = P[0]*(1+0.61*r)  
    
    F_theta = Cd*V*(theta_sfc - P[0])
    delta_theta = theta_0 + Gamma*P[2] - P[0]
    delta_q = q_ft - P[1]
    F_q = Cd*V*(q_sfc - P[1])
    delta_theta_v = (theta_0 + Gamma*P[2])*(1 + epsilon*q_ft)- thetav_BL
    F_B = F_theta + epsilon*P[0]*F_q
    w_e = A*F_B/delta_theta_v
    w_FT = Q_ft/Gamma
    w_m = (-P[2]-LCL)/tau
    
    #LCL = calc_lcl(q_bl,theta,c.psfc)
    LCL = 400
    
    #
    # EQUATIONS
    #
    P[0] = Q_bl + (1/P[2])*(w_e*delta_theta + F_theta)
    P[1] = (1/P[2])*(w_e*delta_q + F_q)
    P[2] = w_FT + w_e + w_m

    return(P[0], P[1], P[2], delta_theta, delta_q)

# %%
# #result=pd.DataFrame.from_records(prof1,columns=['theta','q_bl','h', 'deltheta', 'delq'])

# q_bl = result['q_bl']
# theta = result['theta']
# lcl_h = calc_lcl(q_bl,theta,c.psfc)

# #print(lcl_h)

# %% [markdown]
# Calling and running above functions with desired inputs
#
# * needs cleaning*

# %%
#
# INPUTS
#
Q_ft = -1.0*(1/(24*3600)) #K/s
Gamma = 5.0/1000 #K m^-1
theta_0 = 298 #K
theta_sfc = 301 #K
A = 0.41
Cd = 0.001
V = 5 #m/s
tau = 15*60 #s
epsilon = 0.61
#var_init = []

theta_sfc = 302 #K GUESS
Q_bl = -1

#
# set up solution for ODEs
#

tf = 3*3600
dtout = 3600
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
P0 = [300, 16, 400, 0.1, 0.1]

#
# GUESSES
#
q_sfc = 0.25
q_ft = 3 #free-tropospheric water vapour mixing ratio just above the BL inversion
q_bl = 8
LCL = 10000

prof1 = odeint(solve_equations, P0, tspan, (Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, -1, q_sfc, q_ft, q_bl, LCL))
prof3 = odeint(solve_equations, P0, tspan, (Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, -3, q_sfc, q_ft, q_bl, LCL))
prof5 = odeint(solve_equations, P0, tspan, (Q_ft, Gamma, theta_0, theta_sfc, A, Cd, V, tau, epsilon, -5, q_sfc, q_ft, q_bl, LCL))
#prof1 = prof1.T
prof1.shape


# %%
#print(prof1[:,1])

# %% [markdown]
# #### Make theta profile

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

result=pd.DataFrame.from_records(prof1,columns=['theta','q_bl','h', 'deltheta', 'delq'])
#display(result)
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


# %% [markdown]
# #### Make q profile

# %%
def make_prof_q(df_out,gamma):
    #
    #  construct a vertical (theta, height) profile with the correct Delta theta jump
    #  using four points
    #
    profile=[(df_out['q_bl'],0),
             (df_out['q_bl'],df_out['h']),
             (df_out['q_bl'] - df_out['delq'],df_out['h']),
             (df_out['q_bl'] - df_out['delq'] - gamma*df_out['h'],df_out['h'])]
    xvals=[item[0] for item in profile]
    yvals=[item[1] for item in profile]
    return xvals,yvals

result=pd.DataFrame.from_records(prof1,columns=['theta','q_bl','h', 'deltheta', 'delq'])
#display(result)
result['time']=tspan/24./3600.
out=result.to_dict(orient='records')

fig,ax = plt.subplots(1,1,figsize=(10,10))
for count,row in enumerate(out):
    if np.mod(count,3) == 0:
        qvals,heightvals=make_prof_q(row,Gamma)
        ax.plot(qvals,heightvals)
        
out=ax.set(xlabel='q_BL (g/kg)',ylabel='height (m)',
           title=(f'Single column moist model '
                  f'$Q_BL = {-1} K/day$ and $\Gamma$={Gamma} K/km'))
ax.grid(True,which='both')

# %%

# %%

# %%
