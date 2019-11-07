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
# <div class="toc"><ul class="toc-item"><li><span><a href="#Process-Daily-Data" data-toc-modified-id="Process-Daily-Data-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Process Daily Data</a></span><ul class="toc-item"><li><span><a href="#Test-Calcs-(Single-Year)" data-toc-modified-id="Test-Calcs-(Single-Year)-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Test Calcs (Single Year)</a></span></li><li><span><a href="#Process-All-Years" data-toc-modified-id="Process-All-Years-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Process All Years</a></span></li><li><span><a href="#Create-a-subset-of-the-data" data-toc-modified-id="Create-a-subset-of-the-data-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Create a subset of the data</a></span></li></ul></li></ul></div>
# %% [markdown]
# # Process Daily Data
#
# Concatenate the raw data csv files into a single dataframe for all years,
# doing some quality control.  We'll be focussing on the YVR airport station.
#
# * Start with a single year to develop the code
#
# * Write a function so
# %%
from pathlib import Path

import pandas as pd

# %%
import context

# %%

# %% [markdown]
# ## Test Calcs (Single Year)

# %%
station = "YVR"
stn_id = 51442
year = 2013
datafile = context.raw_dir / Path(f"weather_daily_{station}_{stn_id}_{year}.csv")

# %%
df_in = pd.read_csv(datafile, skiprows=24, index_col=0, parse_dates=True)
df_in.head()

# %% [markdown]
# Some years, such as 2013, have a chunk of missing data at the beginning or end because the data is split into two different files where the Environment Canada station ID changed partway through the year.
#
# To make sure these rows don't mess things up for concatenation later, we will simply discard any rows where all the measurements are missing (the measurements go from column `'Data Quality'` to the final column).
#
# Note that we are specifying the 'Data Quality' column by its name, not its column number

# %%
# Create a series which is True for any row that has at least one non-null measurement
# and False otherwise

not_null = df_in.loc[:, "Data Quality":].notnull().any(axis=1)
not_null.head()

# %%
# Extract the subset of df_in where the not_null Series is True
data = df_in[not_null]
data.head()

# %% [markdown]
# To make life easier, let's also remove the degree symbol from the column names, using the string method `replace` and a [list comprehension](https://jakevdp.github.io/WhirlwindTourOfPython/11-list-comprehensions.html)

# %%
# Create list of column names with degree symbols removed
columns = [nm.replace("\xb0", "") for nm in data.columns]
columns

# %%
# Update the column names in the DataFrame
data.columns = columns
data.head()


# %% [markdown]
# ## Process All Years
#
# Let's consolidate the above code into a function and then use it to process each year and concatenate the years into a single DataFrame.

# %%
def process_data(datafile, skiprows=24):
    """Process data for a single year."""
    df_in = pd.read_csv(datafile, skiprows=24, index_col=0, parse_dates=True)

    # Create a series which is True for any row that has at least one
    # non-null measurement and False otherwise
    not_null = df_in.loc[:, "Data Quality":].notnull().any(axis=1)

    # Extract the subset of df_in where the not_null Series is True
    data = df_in[not_null]

    # Create list of column names with degree symbols removed
    columns = [nm.replace("\xb0", "") for nm in data.columns]

    # Update the column names in the DataFrame
    data.columns = columns

    return data


# %%
# Test the function on the data file from above
test = process_data(datafile)
test.head()

# %% [markdown]
# - First, concatenate all the data from the first set of years.
#   - *Note: The YVR data from 1937 is a bit wonky, so we'll exclude it here.*
# - Then, concatenate the data from recent years

# %%
# Initialize an empty DataFrame
data_all = pd.DataFrame()

# Early data (1938 to mid 2013)
stn_id_early = 889
years_early = range(1938, 2014)

# Recent data (mid 2013 to 2017)
stn_id_recent = 51442
years_recent = range(2013, 2020)

# Loop over station IDs and years, using Python's zip function
for stn, years_list in zip([stn_id_early, stn_id_recent], [years_early, years_recent]):
    for year in years_list:
        filename = context.raw_dir / Path(f"weather_daily_{station}_{stn}_{year}.csv")
        data_in = process_data(filename)

        # Use the append method to append the new data
        data_all = data_all.append(data_in)

# %%
data_all.head(2)

# %%
data_all.tail(2)

# %%
data_all.shape

# %%
# Save the full set of concatenated data to file
year_min, year_max = data_all["Year"].min(), data_all["Year"].max()
savefile = (context.processed_dir 
             / Path(f"weather_daily_{station}_{year_min}-{year_max}_all.csv"))
print(f"Saving to {savefile}")
data_all.to_csv(savefile)

# %% [markdown]
# ## Create a subset of the data
#
# For demos we'll use a subset of the data columns and rename some of them for convenience.

# %%
# Extract subset with columns of interest and rename some columns

columns = [
    "Year",
    "Month",
    "Day",
    "Mean Temp (C)",
    "Max Temp (C)",
    "Min Temp (C)",
    "Total Rain (mm)",
    "Total Snow (cm)",
    "Total Precip (mm)",
]

cols_dict = {
    "Mean Temp (C)": "T_mean (C)",
    "Max Temp (C)": "T_high (C)",
    "Min Temp (C)": "T_low (C)",
    "Total Rain (mm)": "Rain (mm)",
    "Total Snow (cm)": "Snow (cm)",
}
data_subset = data_all[columns].rename(columns=cols_dict)
data_subset.index.name = "Date"
data_subset.head()

# %%
savefile2 = context.processed_dir / Path(f"weather_{station}.csv")
print(f"Saving to {savefile2}")
data_subset.to_csv(savefile2)

# %%
