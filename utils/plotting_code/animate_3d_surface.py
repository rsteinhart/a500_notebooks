import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation as anima

import numpy as np
import glob, os, sys

from netCDF4 import Dataset as nc

import seaborn as sns
from skimage import measure

def plot_clouds_trisurf(file):
    with nc(file, 'r') as nc_file:
        qn_map = np.array(nc_file['QN'][:]).swapaxes(0, 2)[:, :, :180]

        mcl = measure.marching_cubes_lewiner
        verts, faces, _, _ = mcl(
            qn_map, 
            level=1e-3,
            allow_degenerate=False,
            step_size=4
        )

    fig = plt.figure(1, figsize=(20, 6), tight_layout=True)
    fig.clf()
    sns.set_context('paper')
    sns.set_style('ticks', 
        {
            'axes.grid': False,
            'axes.linewidth': '0.75',
            'grid.color': '0.75',
            'grid.linestyle': u':',
            'legend.frameon': True,
        })
    plt.rc('text', usetex=True)
    plt.rc('font', family='Serif')

    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel(r'x')
    ax.set_ylabel(r'y')
    ax.set_zlabel(r'z')

    cmap = sns.diverging_palette(220, 20, n=7, as_cmap=True)
    ax.plot_trisurf(
        verts[:, 0], verts[:, 1], faces, verts[:, 2],
        cmap=cmap, 
        edgecolor='k', 
        lw=0.2
    )

    def animate(ii):
        ax.azim = ii
    
    animated_field = anima.FuncAnimation(
        fig, 
        animate, 
        frames=180,
        interval=15,
    )

    writer = anima.ImageMagickWriter(
        fps=15, 
        bitrate=6400, 
        codec="libx264"
    )
    animated_field.save('animated_field.mp4', writer=writer)

if __name__ == '__main__':
    file_name = 'GATE_1920x1920x512_50m_1s_ent_comp_0000042900.nc'
    file = f'/newtera/loh/data/GATE/variables/{file_name}'
    
    plot_clouds_trisurf(file)
