import numpy as np

# +
#
# for LCL_calc
#

pa2hPa=1.e-2
hPa2pa=1.e2
Tp = 273.16
#triple point in kelvin
Tc = 273.15
#0 deg C in Kelvin
eps = 0.622
# Rd/Rv
phi0 = 9155.80612
#lv0/Tp  (J/kg/K
es0 = 6.112 #hPa
p0 = 1.e5  #Pa
lv0 = 2.501e6  #J/kg
# J/kg
Rv = 461.50
# J/kg/K
Rd = 287.04
# J/kg/K
cpv = 1870.
# Heat capacity of water vapor (J/kg/K)
cl = 4190.
# Heat capacity of liquid water (J/kg/K)
cpd = 1005.7
# Heat capacity of dry air (J/kg/K)
delta = (1 - eps)/eps  
#Thompkins 2.33 for Tv
g0 = 9.8
# m/s^2
D = 2.36e-5
# Diffusivity m^2/s^1
rhol = 1000.

psfc=100. #kPa

# +
#
# for equation solver
#

Q_ft = -1.0*(1/(24*3600)) 
#K/s
Gamma = 5.0/1000 
#K m^-1
theta_0 = 298 
#K
theta_sfc = 301 
#K
A = 0.41
Cd = 0.001
V = 5 
#m/s
tau = 15*60 
#s
epsilon = 0.61
theta_sfc = 302 
#K GUESS
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

#
# GUESSES
#
q_sfc = 0.25
q_ft = 3 #free-tropospheric water vapour mixing ratio just above the BL inversion
q_bl = 8
r = 8

P0 = [297, 16, 350, 1.8, 1.8]

