# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: -language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Download-Environment-Canada-Daily-Data" data-toc-modified-id="Download-Environment-Canada-Daily-Data-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Download Environment Canada Daily Data</a></span><ul class="toc-item"><li><span><a href="#Set-the-context-for-this-notebook" data-toc-modified-id="Set-the-context-for-this-notebook-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Set the context for this notebook</a></span></li><li><span><a href="#Station-Inventory" data-toc-modified-id="Station-Inventory-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Station Inventory</a></span></li><li><span><a href="#Info-for-Selected-Station" data-toc-modified-id="Info-for-Selected-Station-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Info for Selected Station</a></span><ul class="toc-item"><li><span><a href="#Download-Data" data-toc-modified-id="Download-Data-1.3.1"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Download Data</a></span></li></ul></li></ul></li></ul></div>
# %% [markdown]
# # Download Environment Canada Daily Data
#
# can skip this and download directly from this dropbox link:
#
# [a500_data.zip](https://www.dropbox.com/s/1bganh60983pges/a500_pandas_data.zip?dl=0)
#
# unzip this to create the folder data in the same pandas folder as this notebook.
# %%
from pathlib import Path

import pandas as pd
import requests

# %% [markdown]
# ## Set the context for this notebook
#
# Importing the context module will check to see whether
# `data/processed` and `data/raw` exist and complain if
# it can't find them

# %% {"scrolled": true}
import context

# %% [markdown]
# ## Station Inventory
#
# * Instructions: copy and paste this url into a browser: (ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/)
#
# * To get the station inventory (1.3 Mbyte csv file), copy and paste this url into
#   a browser (`%20` is the blank space character)
#
#   ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
#
#   We have saved a copy in `data/Station Inventory EN .csv`

# %%
#
# note that whitespace (blanks, tabs, newlines) in a tuple are discarded
# so we can split a long string up like this:
#
f = (
    "ftp://client_climate@ftp.tor.ec.gc.ca/Pub/"
    "Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv"
)


# %%
inventory_file = context.data_dir / "Station Inventory EN.csv"
inventory = pd.read_csv(inventory_file, skiprows=3)

# Rename some of the columns to more convenient labels
cols_dict = {
    "TC ID": "Airport Code",
    "Station ID": "Env Canada ID",
    "Latitude (Decimal Degrees)": "Latitude (deg)",
    "Longitude (Decimal Degrees)": "Longitude (deg)",
}
inventory = inventory.rename(columns=cols_dict)

print(inventory.shape)
inventory.head()

# %% [markdown]
# ## Info for Selected Station
#
# To download data for Vancouver Airport station (airport code YVR), we need the ID codes used by Environment Canada for this station.  Here is how we find the numerical code 'YVR'.
# Note that it has changed at some point from 889 to 51442

# %%
station = "YVR"

# Extract the inventory row(s) corresponding to this station
station_info = inventory[inventory["Airport Code"] == station]
station_info


# %% [markdown]
# ### Download Data
#
# First, define a function to download the CSV data using the Environment Canada API:

# %%
def download_daily_raw(env_canada_id, year, savefile="test.csv", verbose=True):
    """Download CSV file of daily data for selected station and year"""

    # URL endpoint and query parameters
    url_endpoint = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html"
    params = {
        "format": "csv",
        "stationID": env_canada_id,
        "Year": year,
        "Month": "01",
        "Day": "01",
        "timeframe": "2",
        "submit": " Download Data",
    }

    # Send GET request
    response = requests.get(url_endpoint, params=params)

    # Download CSV file
    if verbose:
        print(f"Saving to {savefile}")
    with open(savefile, "wb") as f:
        f.write(response.content)

    return None


# %% [markdown]
# *Note: The code below uses [f-strings](https://realpython.com/python-f-strings/) to substitute variable values into a string*

# %%
# Early data (1937 to mid 2013)
stn_id_early = 889  # station id for YVR airport
years_early = range(1937, 2014)

for year in years_early:
    savefile = context.raw_dir / Path(f"weather_daily_{station}_{stn_id_early}_{year}.csv")
    download_daily_raw(stn_id_early, year, savefile=savefile)

# %%
# Recent data (mid 2013 to 2019)
stn_id_recent = 51442
years_recent = range(2013, 2020)

for year in years_recent:
    savefile = (context.raw_dir / 
                Path(f"weather_daily_{station}_{stn_id_recent}_{year}.csv"))
    download_daily_raw(stn_id_recent, year, savefile=savefile)
