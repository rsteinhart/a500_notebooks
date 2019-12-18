# %% [markdown]
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#FOJ-simple-mixed-layer-model" data-toc-modified-id="FOJ-simple-mixed-layer-model-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>FOJ simple mixed layer model</a></span></li><li><span><a href="#Simple-integrator-model" data-toc-modified-id="Simple-integrator-model-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Simple integrator model</a></span></li><li><span><a href="#Dry-LES-model" data-toc-modified-id="Dry-LES-model-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Dry LES model</a></span></li><li><span><a href="#All-on-the-same-graph" data-toc-modified-id="All-on-the-same-graph-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>All on the same graph</a></span></li><li><span><a href="#Time-history-of-boundary-layer-heights" data-toc-modified-id="Time-history-of-boundary-layer-heights-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Time history of boundary layer heights</a></span></li></ul></div>

# %% [markdown]
# # FOJ simple mixed layer model

# %%
import numpy as np
import pdb
import scipy.integrate as integrate
from matplotlib import pyplot as plt

# %%
def tend(y, t, F0, gamma, rho_star, wh, Cp):
    
    """
    y = intial theta, initial height, initial del theta

    """
    
    y[0] = ((1+k)*F0) / (y[1]*Cp* rho_star) # theta = mean temperature
    y[1] = (k*F0) / (rho_star*Cp*y[2]) +wh # inversion height
    y[2] = ((y[1] - wh)*gamma) - y[0] # del theta = inversion jump
    

    return y[0],y[1],y[2]


# %%
Hs0 = 300. # surface sensible heat flux
the_lambda = 100. # used in calculating the blackadar length scale

# set up the environment
ztop = 1000. # height of fi
dz = 10. # change in height level

# set time
tf = 3*3600 # final time length
dtout = 600 # interval length of time that we're using
tspan = np.arange(0.,tf,dtout) # create a time span array to integrate over

# choose an intial theta value for each mid-layer level
zh = np.arange(dz/2,(ztop-dz/2),dz)
theta_i = 290 + 0.01*zh
#theta_i = 290 + 0.01*zf

# the number of half levels 
nz = len(zh) # this is 99 (because we have 100 levels)
zh.shape


# %%
# Constants
rho_star = 1.2
Cp = 1004.
k = 0.4
gamma = 10/1000 # K/m
F0 = 60
zf = np.arange(0.,ztop,dz)
#zh = np.arange(dz/2,(ztop-dz/2),dz)
l = the_lambda/(1 + the_lambda/(k*zf[1:-1])) # Blackadar master lengthscale
wh = 0 # this is the subsidence rate ... try for different values

#initial values:
yi = [301.75,400, 1]

# %%
# yi = intial h, initial theta, del theta
the_prof=integrate.odeint(tend, yi, tspan,(F0, gamma, rho_star, wh, Cp))
the_prof.shape

# %%
# mean theta 
mean_theta = np.empty_like(the_prof[0:,0])
mean_theta[0] = the_prof[0,0]
inv_height = np.empty_like(the_prof[0:,1])
inv_height[0] = the_prof[0,1]
del_theta = np.empty_like(the_prof[0:,2])
del_theta[0] = the_prof[0,2]

for i in range(1,18):
    mean_theta[i] = the_prof[i,0]+the_prof[0,0]
    inv_height[i] = the_prof[i,1]+the_prof[0,1]
    del_theta[i] = the_prof[i,2]+the_prof[0,2]

# %%
# if you have subsidence it means that you'll have a steady state inversion which 
# explains why you have lasting inversions in highs

# %%
fig,ax=plt.subplots(1,1,figsize=(10,8))
for i2 in range(0,18):
    x4 = mean_theta[i2]+del_theta[i2]+gamma*0.5*inv_height[i2]
    y4 = inv_height[i2]*1.5
    ax.plot([mean_theta[i2],mean_theta[i2], mean_theta[i2]+del_theta[i2],x4],
         [0,inv_height[i2],inv_height[i2],y4])
ax.set(xlabel=r'$\overline{\theta}$ (K)',ylabel='height (m)',title = 'First order jump mixed layer model');


# %% [markdown]
# # Simple integrator model

# %%
def dthdt(theta, t, zf, zh, l, Fth0):
    """
     theta tendency for ODE solver used to calculate deepening of surf-heated BL.
     Arguments   Size   Units  Description
       t          1       s    time
       theta     nz     K    at half-levels zh (here nz is length of zh)
     Parameters
       zf      (nz+1)   m    height of flux levels
       zh          nz   m    height of half (thermo) levels
       l       (nz-1)   m    Blackadar lengthscale at heights z(2)-z(nz)
       Fth0         1   K m/s  Constant surface theta flux
     Output
       tend        nz   m    tendency d(theta)/dt at the half-levels
       K       (nz-1)   m2/s  eddy diffusivity at interior flux levels
       Fth     (nz+1)   K m/s  theta flux at flux levels
    """
    Fth=np.empty_like(zf)
    g = 9.8
    thetaref = np.mean(theta)
    dthdz = np.diff(theta)/np.diff(zh)

#  We use the convective limit (Ri -> inf) of eddy diffusivity formula
#   K = l^2*|du/dz|*sqrt(1-16Ri) ~ l^2*sqrt(-16*db/dz) (unstable)
#  We take K=0 for stable stratification.

    dbdz = (g/thetaref)*dthdz
    dbdz[dbdz>0] = 0
    K = l**2.*np.sqrt(-16*dbdz)
    Fth[1:-1] = -K*dthdz
    Fth[0] = Fth0
    Fth[-1] = 0
    tend = -np.diff(Fth)/np.diff(zf)
    # tend = d_theta/dz
#    pdb.set_trace()
    return tend


# %%
tf = 3*3600
dtout = 600
dz = 10.
ztop = 1000.
the_lambda = 100.
Hs0 = 300.
zh = np.arange(dz/2,(ztop-dz/2),dz)
thetai = 290 + 0.01*zh

tspan = np.arange(0.,tf,dtout)
zf = np.arange(0.,ztop,dz)
nz = len(zh)

rhoref = 1.2
Cp = 1004.
Fth0 = Hs0/(rhoref*Cp)

#  Specify Blackadar master lengthscale for interior flux points for use in
#  ODE solver.

k = 0.4
l = the_lambda/(1 + the_lambda/(k*zf[1:-1]))

# the_prof2=integrate.odeint(dthdt, thetai, tspan,(zf, zh, l, Fth0))
# plt.close('all')
# fig,ax = plt.subplots(1,1,figsize=(8,8))
# for item in the_prof:
#     ax.plot(item,zh)
# plt.show()

# %% [markdown]
# # Dry LES model

# %%
from a500.utils.ncdump import ncdump
from netCDF4 import Dataset
# import sys
# import a500

def make_theta(temp,press):
    """
      temp in K
      press in Pa
      returns theta in K
    """
    p0=1.e5
    Rd=287.  #J/kg/K
    cpd=1004.  #J/kg/K
    theta=temp*(p0/press)**(Rd/cpd)
    return theta

case_name='case_60_10.nc'
#
#  look at the first ensemble member
#
ensemble='c1'
with Dataset(case_name,'r') as ncin:
    #
    # grab the group variables
    #
    group = ncin.groups[ensemble]
    temp=group.variables['TABS'][...]
    press=ncin.variables['press'][...]
    z=ncin.variables['z'][...]
mean_temp=temp.mean(axis=(3,2))


fig,ax=plt.subplots(1,1,figsize=(10,8))
for i in np.arange(0,temp.shape[0],3):
    theta = make_theta(mean_temp[i,:],press)
    ax.plot(theta,z)
out=ax.set(xlabel=r'$\overline{\theta}$ (K)',ylabel='height (m)',
       title=f'LES dry run for realization {ensemble}:  surface flux=60 $W\,m^{-2}$, $\Gamma$=10 K/km')
ax.grid(True, which='both')

# %%

# %%

# %%

# %%

# %%

# %% [markdown]
# # All on the same graph

# %%
fig,ax=plt.subplots(1,1,figsize=(10,8))
for i2 in range(0,18):
    x4 = mean_theta[i2]+del_theta[i2]+gamma*0.5*inv_height[i2]
    y4 = inv_height[i2]*1.5
    ax.plot([mean_theta[i2],mean_theta[i2], mean_theta[i2]+del_theta[i2],x4],
         [0,inv_height[i2],inv_height[i2],y4],
            color = "green",
           label = "mixed layer model")
ax.set(xlabel=r'$\overline{\theta}$ (K)',ylabel='height (m)',
       title = 'FOJ model, dry LES model and simple integrator model');

for item in the_prof2:
    ax.plot(item,zh, color ="blue",
           label="simple integrator")

for i in np.arange(0,temp.shape[0],3):
    theta = make_theta(mean_temp[i,:],press)
    ax.plot(theta,z, color="red",
           label="dry LES")
    


# %%

# %% [markdown]
# # Time history of boundary layer heights

# %%
dry_les_inv = np.genfromtxt("zstore.csv", delimiter=',')
dry_les_time = np.genfromtxt("day_frac.csv", delimiter=',')


# %%
fig,ax=plt.subplots(1,1,figsize=(10,8))
ax.plot((tspan/3600),inv_height, label = "mixed layer model")
ax.plot(dry_les_time*10, dry_les_inv, label = "dry LES model")
ax.set(xlabel='Time (hours)',ylabel='Height (m)',
       title = 'Time history of boundary layer heights');
ax.legend()

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%
