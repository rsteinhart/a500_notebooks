# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
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
#     sideBar: false
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: true
#     toc_position: {}
#     toc_section_display: block
#     toc_window_display: false
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Reading-multiple-months-from-the-cesar-archive" data-toc-modified-id="Reading-multiple-months-from-the-cesar-archive-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Reading multiple months from the cesar archive</a></span><ul class="toc-item"><li><span><a href="#Step-1:-read-in-all-the-file-names-and-return-a-dictionary" data-toc-modified-id="Step-1:-read-in-all-the-file-names-and-return-a-dictionary-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Step 1: read in all the file names and return a dictionary</a></span></li><li><span><a href="#Turn-cabauw-dates-into-datetime-objects" data-toc-modified-id="Turn-cabauw-dates-into-datetime-objects-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Turn cabauw dates into datetime objects</a></span></li><li><span><a href="#Extract-the-data" data-toc-modified-id="Extract-the-data-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Extract the data</a></span></li><li><span><a href="#Write-the-data-out-to-a-netcdf-file" data-toc-modified-id="Write-the-data-out-to-a-netcdf-file-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Write the data out to a netcdf file</a></span></li></ul></li></ul></div>

# %% [markdown]
# # Reading multiple months from the cesar archive
#
# For this example I downloaded 12 months of data from 2014 with three file types
# (all lc1 i.e. gap-filled)
#
# cesar_surface_flux_lc1_t10_v1.0_201402.nc
#
# cesar_surface_meteo_lc1_t10_v1.0_201402.nc
#
# cesar_tower_meteo_lc1_t10_v1.0_201402.nc

# %% [markdown]
# ## Step 1: read in all the file names and return a dictionary
#
# The make_file_dict function returns a dictionary that contains three lists of file names keyed by:
#
#     ['surface_fluxes', 'surface_meteorological', 'tower_meteorological']
#

# %%
from a500.utils.read_cabauw import (make_file_dict,write_dates,
                                    store_months, write_cdf)
from pathlib import Path
root_dir = "/Users/phil/Downloads/data"
root_dir=Path(root_dir)
year = 2014
file_dict=make_file_dict(root_dir,year)

# %% [markdown]
# ## Turn cabauw dates into datetime objects
#
# The write_dates function opens each netcdf file and creates an dictionary with times, location and variable attributes keyed as:
#
#     [filetype](year,month]
#     
#     i.e. ['surface_fluxes'][2014,4]

# %%
keep_months={}
for filetype,file_list in file_dict.items():
    keep_months[filetype]=write_dates(filetype,file_list)

# %% [markdown]
# ## Extract the data
#
# The store_months function takes the keep_months dictionary and
# returns a new dictionary with these keys for each of the three cabauw data files:
#
#     list(full_dict['surface_fluxes'].keys())
#     ['filelist', 'data', 'var_attrs', 'lat', 'lon']
#     
# where filelist points to a list of the 12 filenames, data points to the data dictionary:
#
#     list(full_dict['surface_fluxes']['data'].keys())
#     
#     [(2014, 1),
#      (2014, 2),
#      (2014, 3),
#      (2014, 4),
#      (2014, 5),
#      (2014, 6),
#      (2014, 7),
#      (2014, 8),
#      (2014, 9),
#      (2014, 10),
#      (2014, 11),
#      (2014, 12)]
#
#     list(full_dict['surface_fluxes']['data'][2014,1].keys())
#     ['H', 'UST', 'LE']
#     
#     list(full_dict['surface_meteorological']['data'][2014,1].keys())
#     ['P0', 'TA002', 'Q002', 'F010']
#     
#     list(full_dict['tower_meteorological']['data'][2014,1].keys())
#     ['timevec', 'has_time', 'z', 'F', 'TA', 'TD', 'Q', 'D']
#     
# and var_attrs list the variable attributes
#
#     list(full_dict['tower_meteorological']['var_attrs']['F'].keys())
#     
#         ['units',
#      'long_name',
#      'standard_name',
#      'ancillary_variables',
#      '_FillValue',
#      'cell_methods']
#

# %%
full_dict=store_months(keep_months)

# %% [markdown]
# ## Write the data out to a netcdf file
#
# write_cdf takes the dictionary and produces a netcdf file with
# the following metadata:
#
#

# %%
write_cdf(full_dict,'cabau_2014.nc')

# %%
# !ncdump -h cabau_2014.nc

# %%
