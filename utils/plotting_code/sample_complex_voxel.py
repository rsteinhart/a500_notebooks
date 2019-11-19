import os, glob

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import xarray as xr 

from mpl_toolkits.mplot3d import Axes3D
from skimage import measure

def save_sample_field():
    with xr.open_dataset('scratch/field.nc', 'r') as f:
        Z = f['core'][:64, :, :]
        Z = np.add.reduceat(
            np.add.reduceat(
            np.add.reduceat(Z, np.arange(0, Z.shape[0], 1), axis=0),
                            np.arange(0, Z.shape[1], 4), axis=1),
                            np.arange(0, Z.shape[2], 4), axis=2)

        np.save('scratch/sub_field.npy', np.array(Z))
        return Z
    raise("File error")

try:
    sub_field = np.load('scratch/sub_field.npy')
except:
    sub_field = save_sample_field()

# ax.voxel assumes (x, y, z) dimension
sub_field = np.transpose(sub_field, (2, 1, 0))
print(sub_field.shape)

sub_field = np.array(sub_field, dtype=np.bool_)
voxels = measure.label(sub_field, connectivity=3)

uids, counts = np.unique(voxels, return_counts=True)
print(f'{len(uids)} uids ({sum(counts <=2)} noise)')

uids_sorted = uids[np.argsort(-counts)]

n_color = 16
cmap = sns.color_palette('Paired', n_color).as_hex()
# set the colors of each object
colors = np.empty(voxels.shape, dtype=object)
for c_, i in enumerate(uids_sorted[:n_color]):
    colors[voxels == i] = cmap[c_]
for i in uids_sorted[n_color:]:
    colors[voxels == i] = 'gray'

# and plot everything
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(voxels, facecolors=colors, 
            edgecolor='k', 
            linewidth=0.2)

plt.tight_layout(pad=0.5)
figfile = '../png/{}.png'.format(os.path.splitext(__file__)[0])
print('\t Writing figure to {}...'.format(figfile))
plt.savefig(figfile,bbox_inches='tight', dpi=180, \
                facecolor='w', transparent=True)
