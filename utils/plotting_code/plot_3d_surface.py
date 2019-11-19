import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation as anima

import glob, os, sys
import numpy as np

import xarray as xr

import seaborn as sns
from skimage import measure
from joblib import Parallel, delayed

def plot_3d_surface(time, f_name):
    with xr.open_zarr(var_list[time]) as zf:
        qn_map = np.array(zf['QN'][:]).swapaxes(0, 2)
        qr_map = np.array(np.nansum(zf['QR'][:], axis=0))

        qr_map[qr_map < 1e-3] = np.nan

        mcl = measure.marching_cubes_lewiner
        verts, faces, _, _ = mcl(
            qn_map, 
            level=1e-3,
            allow_degenerate=False,
            step_size=2
        )

    #---- Plotting
    fig = plt.figure(1, figsize=(28, 4))
    fig.clf()
    sns.set_context("paper")
    sns.set_style("ticks",
        {
            'axes.grid': True, 
            'axes.linewidth': '0.75',
            'grid.color': '0.75',
            'grid.linestyle': u':',
            'legend.frameon': True,
        })

    plt.rc('text', usetex=True)
    plt.rc('font', family='Serif')

    ax = fig.add_subplot(111, projection='3d')

    cmap = sns.cubehelix_palette(n_colors=8, start=2.4, rot=.2, as_cmap=True)
    ax.plot_trisurf(
        verts[:, 0], verts[:, 1], faces, verts[:, 2],
        cmap=cmap,
        edgecolor='0.4',
        lw=0.05
    )
    ax.azim = 80
    ax.elev = 45

    ax.set_zlim3d(0, 192/2)

    mx, my = np.meshgrid(np.arange(1536), np.arange(512))
    cmap = sns.cubehelix_palette(n_colors=8, start=0, rot=.2, as_cmap=True)
    ax.contourf(mx, my, qr_map, cmap=cmap)

    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    fig_name = f"../png/frames_r_{time:04d}.png"
    print('\t Writing figure to {}...'.format(fig_name))
    plt.savefig(
        fig_name,
        bbox_inches='tight',
        dpi=120,
        facecolor='w',
        transparent=True)

if __name__ == '__main__':
    # File paths 
    data = '/Howard16TB/data/loh/BOMEX_SWAMP'
    var_list = sorted(glob.glob(f'{data}/variables/*.zarr'))

    with Parallel(n_jobs=12, backend='multiprocessing') as Pr:
        Pr(delayed(plot_3d_surface)(time, fn)
            for time, fn in enumerate(var_list))
