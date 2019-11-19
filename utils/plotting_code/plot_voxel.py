import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
 
import os, glob

from mpl_toolkits.mplot3d import Axes3D
from skimage import measure

# prepare some coordinates
x, y, z = np.indices((8, 8, 8))

# draw cuboids in the top left and bottom right corners
cube1 = (x < 3) & (y < 3) & (z < 3)
cube2 = (x >= 5) & (y >= 5) & (z >= 5)
link = abs(x - y) + abs(y - z) + abs(z - x) <= 1 

# combine the objects into a single boolean array
voxels = cube1 | cube2 | link

voxels[cube1] = 2
voxels[cube2] = 1
voxels[link] = 1
voxels = measure.label(voxels, connectivity=1)
print(voxels)

# set the colors of each object
colors = np.empty(voxels.shape, dtype=object)
colors[voxels == 1] = 'red'
colors[voxels == 2] = 'green'

# and plot everything
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(voxels, facecolors=colors, edgecolor='k')

plt.tight_layout(pad=0.5)
figfile = 'png/{}.png'.format(os.path.splitext(__file__)[0])
print('\t Writing figure to {}...'.format(figfile))
plt.savefig(figfile,bbox_inches='tight', dpi=180, \
                facecolor='w', transparent=True)
