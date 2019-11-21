import matplotlib
import context


from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation as anima

import numpy as np
import click
import json
from pathlib import Path

import xarray as xr

import seaborn as sns
from skimage import measure
from joblib import Parallel, delayed

matplotlib.use("Agg")


def plot_3d_surface(qn_map, qr_map):

    mcl = measure.marching_cubes_lewiner
    verts, faces, _, _ = mcl(qn_map, level=1e-3, allow_degenerate=False, step_size=2)
    # ---- Plotting
    fig = plt.figure(1, figsize=(28, 4))
    fig.clf()
    sns.set_context("paper")
    sns.set_style(
        "ticks",
        {
            "axes.grid": True,
            "axes.linewidth": "0.75",
            "grid.color": "0.75",
            "grid.linestyle": ":",
            "legend.frameon": True,
        },
    )

    plt.rc("text", usetex=True)
    plt.rc("font", family="Serif")

    ax = fig.add_subplot(111, projection="3d")

    cmap = sns.cubehelix_palette(n_colors=8, start=2.4, rot=0.2, as_cmap=True)
    ax.plot_trisurf(
        verts[:, 0],
        verts[:, 1],
        faces,
        verts[:, 2],
        cmap=cmap,
        edgecolor="0.4",
        lw=0.05,
    )
    ax.azim = 80
    ax.elev = 45

    ax.set_zlim3d(0, 192 / 2)

    mx, my = np.meshgrid(np.arange(1536), np.arange(512))
    cmap = sns.cubehelix_palette(n_colors=8, start=0, rot=0.2, as_cmap=True)
    ax.contourf(mx, my, qr_map, cmap=cmap)

    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    return fig, ax


@click.command()
@click.argument("config_json", type=click.File("r"), nargs=1)
def main(config_json):
    """
    make a 3d plot of a model output field
    where CONFIG_JSON is the path to a config.json file
    """
    config_dict = json.load(config_json)
    namelist = config_dict["namelist"][0]
    zarr_files = list(context.data_dir.glob(namelist))
    the_file = zarr_files[0]
    with xr.open_zarr(str(the_file)) as zf:
        qn_map = np.array(zf["QN"][:]).swapaxes(0, 2)
        qr_map = np.array(np.nansum(zf["QR"][:], axis=0))


if __name__ == "__main__":
    main()
    # # File paths
    # print(context.data_dir)
    # zarr_file = list(context.data_dir.glob("BOMEX*zarr"))
    # with open("config.json", "w") as out:
    #     out_dict = {"contents": "namelist is a list of globbalble file names"}
    #     out_dict["namelist"] = ["BOMEX*zarr"]
    #     out_dict["config_version"] = "1.0"
    #     json.dump(out_dict, out, indent=4)
    # # with xr.open_zarr(str(zarr_file)) as zf:
    # #     qn_map = np.array(zf["QN"][:]).swapaxes(0, 2)
    # #     qr_map = np.array(np.nansum(zf["QR"][:], axis=0))

    # #     qr_map[qr_map < 1e-3] = np.nan
    # #     print(f"shapes for qn: {qn_map.shape} and qr: {qr_map.shape}")
    # #     fig, ax = plot_3d_surface(qn_map, qr_map)
    # #     fig_name = f"outfig.png"
    # #     print(f"Writing figure to {fig_name}")
    # #     fig.savefig(
    # #         fig_name, bbox_inches="tight", dpi=120, facecolor="w", transparent=True
    # #     )

    # # with Parallel(n_jobs=12, backend="multiprocessing") as Pr:
    # #     Pr(delayed(plot_3d_surface)(time, fn) for time, fn in enumerate(var_list))
