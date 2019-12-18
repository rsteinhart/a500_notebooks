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


# %% [markdown]
# #### Solving the system of equations for the 1D dry moisture model

# %%
def solve_equations(P,t, Q_bl):
    
    thetav_BL = P[0]*(1+0.61*c.r) 
    LCL = calc_lcl(q_bl,c.theta_0,c.psfc)
    
    F_theta = c.Cd*c.V*(c.theta_sfc - P[0])
    delta_theta = c.theta_0 + c.Gamma*P[2] - P[0]
    delta_q = c.q_ft - P[1]
    F_q = c.Cd*c.V*(c.q_sfc - P[1])
    delta_theta_v = (c.theta_0 + c.Gamma*P[2])*(1 + c.epsilon*c.q_ft)- thetav_BL
    F_B = F_theta + c.epsilon*P[0]*F_q
    w_e = c.A*F_B/delta_theta_v
    w_FT = c.Q_ft/c.Gamma
    w_m = (-P[2]-LCL)/c.tau
    
    #
    # ODE EQUATIONS
    #
    P[0] = Q_bl + (1/P[2])*(w_e*delta_theta + F_theta)
    P[1] = (1/P[2])*(w_e*delta_q + F_q)
    P[2] = w_FT + w_e + w_m

    return(P[0], P[1], P[2], delta_theta, delta_q)

# %% [markdown]
# Calling and running above functions with desired inputs

# %%
#prof1 = odeint(solve_equations, c.P0, c.tspan, -1)
#prof3 = odeint(solve_equations, c.P0, c.tspan, -3)
#prof5 = odeint(solve_equations, c.P0, c.tspan, -5)

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

# result=pd.DataFrame.from_records(prof1,columns=['theta','q_bl','h', 'deltheta', 'delq'])
# #display(result)
# result['time']=c.tspan/24./3600.
# out=result.to_dict(orient='records')

# fig,ax = plt.subplots(1,1,figsize=(10,10))
# for count,row in enumerate(out):
#     if np.mod(count,3) == 0:
#         thetavals,heightvals=make_prof(row,c.Gamma)
#         ax.plot(thetavals,heightvals)       
        
# out=ax.set(xlabel=r'$\theta (K)$',ylabel='height (m)',
#            title=(f'Single column moist model '
#                   f'$Q_(BL) = {-1} K/day$ and $\Gamma$={c.Gamma*1000} K/km'))


# ax.grid(True,which='both')

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

# result=pd.DataFrame.from_records(prof1,columns=['theta','q_bl','h', 'deltheta', 'delq'])
# #display(result)
# result['time']=c.tspan/24./3600.
# out=result.to_dict(orient='records')

# fig,ax = plt.subplots(1,1,figsize=(10,10))
# for count,row in enumerate(out):
#     if np.mod(count,3) == 0:
#         qvals,heightvals=make_prof_q(row,c.Gamma)
#         ax.plot(qvals,heightvals)
        
# out=ax.set(xlabel='q_BL (g/kg)',ylabel='height (m)',
#            title=(f'Single column moist model '
#                   f'$Q_BL = {-1} K/day$ and $\Gamma$={c.Gamma*1000} K/km'))
# ax.grid(True,which='both')
