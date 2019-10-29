# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   latex_envs:
#     LaTeX_envs_menu_present: true
#     autoclose: false
#     autocomplete: true
#     bibliofile: biblio.bib
#     cite_by: apalike
#     current_citInitial: 1
#     eqLabelWithNumbers: true
#     eqNumInitial: 1
#     hotkeys:
#       equation: meta-9
#     labels_anchors: false
#     latex_user_defs: false
#     report_style_numbering: false
#     user_envs_cfg: false
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: true
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: true
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Read-ncfile-names-into-a-dictionary" data-toc-modified-id="Read-ncfile-names-into-a-dictionary-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Read ncfile names into a dictionary</a></span><ul class="toc-item"><li><span><a href="#Read-all-attributes-and-get-thetav" data-toc-modified-id="Read-all-attributes-and-get-thetav-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Read all attributes and get thetav</a></span></li></ul></li><li><span><a href="#make-a-plot" data-toc-modified-id="make-a-plot-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>make a plot</a></span></li></ul></div>

# %%
from netCDF4 import Dataset
from matplotlib import pyplot as plt
import context
import a500
from a500.utils.ncdump import ncdump

# %% [markdown]
# # Read ncfile names into a dictionary

# %%
the_files = list(context.data_dir.glob('*.nc'))
file_dict = {item.name:item for item in the_files}
print(list(file_dict.keys()))

# %% [markdown]
# ## Read all attributes and get thetav

# %%
filename=file_dict['profiles.001.nc']
with Dataset(filename,'r',format="NETCDF4") as prof_nc:
    print(f"opening {filename.name}")
    all_attributes = ncdump(prof_nc,verbose=False)
    print(list(prof_nc.variables))
    print(list(prof_nc.dimensions))
    thetav = prof_nc.variables['thv'][0,:]
    height = prof_nc.variables['zm'][...]

# %% [markdown]
# # make a plot

# %%
fig, ax = plt.subplots(1,1,figsize=(6,6))
ax.set(xlabel='thetav (K)',ylabel='height (m)')
ax.grid(True)
ax.plot(thetav,height);

# %%
