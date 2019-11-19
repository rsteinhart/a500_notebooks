import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import seaborn as sns

import glob, os, sys
import numpy as np
import xarray as xr


def plot_2d_surface(time, f_name):
    with xr.open_zarr(var_list[time]) as zf:
        qr_map = np.array(np.nansum(zf['QR'][:], axis=0))
        qr_map[qr_map < 1e-3] = np.nan

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

    ax = fig.add_subplot(111)

    cmap = sns.cubehelix_palette(n_colors=8, start=0, rot=.2, as_cmap=True)
    mx, my = np.meshgrid(np.arange(1536), np.arange(512))
    ax.contourf(mx, my, qr_map, cmap=cmap)

    fig_name = f"../png/2d_field_{time:04d}.png"
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

    plot_2d_surface(698, var_list[698])
