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
# <div class="toc"><ul class="toc-item"></ul></div>

# %%
import context
from a500.utils.data_read import download
import a500
from pathlib import Path
from netCDF4 import Dataset

from bs4 import BeautifulSoup
import requests

url="https://clouds.eos.ubc.ca/~phil/docs/atsc500/data/dales"
ext = 'nc'

def listFD(url, ext=''):
    page = requests.get(url).text
    print(page)
    soup = BeautifulSoup(page, 'html.parser')
    return [node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

file_dict={}
for the_file in listFD(url, ext):
    print(the_file)
    out=download(the_file,root=url,dest_folder=a500.data_dir)
    file_dict[the_file] = a500.data_dir / the_file



# %%
import time
time.sleep(5)

# %%
file_dict

# %%
from a500.utils import ncdump
fieldfile=file_dict['fielddump.000.000.001.nc']
with Dataset(fieldfile,'r') as nc_in:
    ncdump.ncdump(nc_in)

# %%
with Dataset(fieldfile,'r') as nc_in:
    var_dict = {}
    var_list = ['qt','w','zt','yt','xt','time']
    for a_var in var_list:
        var_dict[a_var] = nc_in.variables[a_var][...]

# %%
var_dict

# %%
