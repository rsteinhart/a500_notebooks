# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.7.3
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
#   nbsphinx:
#     execute: never
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: true
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: true
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: true
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Learning-objectives" data-toc-modified-id="Learning-objectives-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Learning objectives</a></span></li><li><span><a href="#Folder-setup" data-toc-modified-id="Folder-setup-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Folder setup</a></span><ul class="toc-item"><li><span><a href="#Subfolder-creation" data-toc-modified-id="Subfolder-creation-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Subfolder creation</a></span></li></ul></li><li><span><a href="#Pandas-dataframes-vs.-numpy-arrays" data-toc-modified-id="Pandas-dataframes-vs.-numpy-arrays-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Pandas dataframes vs. numpy arrays</a></span></li><li><span><a href="#Intro-to-Pandas" data-toc-modified-id="Intro-to-Pandas-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Intro to Pandas</a></span></li><li><span><a href="#Why-Pandas?" data-toc-modified-id="Why-Pandas?-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Why Pandas?</a></span></li><li><span><a href="#Reading-a-CSV-file" data-toc-modified-id="Reading-a-CSV-file-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Reading a CSV file</a></span><ul class="toc-item"><li><span><a href="#The-pathlib-module" data-toc-modified-id="The-pathlib-module-6.1"><span class="toc-item-num">6.1&nbsp;&nbsp;</span>The pathlib module</a></span></li></ul></li><li><span><a href="#Data-at-a-Glance" data-toc-modified-id="Data-at-a-Glance-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Data at a Glance</a></span><ul class="toc-item"><li><span><a href="#Number-of-rows-and-columns:" data-toc-modified-id="Number-of-rows-and-columns:-7.1"><span class="toc-item-num">7.1&nbsp;&nbsp;</span>Number of rows and columns:</a></span></li><li><span><a href="#Simple-Summary-Statistics" data-toc-modified-id="Simple-Summary-Statistics-7.2"><span class="toc-item-num">7.2&nbsp;&nbsp;</span>Simple Summary Statistics</a></span></li></ul></li><li><span><a href="#Exercise" data-toc-modified-id="Exercise-8"><span class="toc-item-num">8&nbsp;&nbsp;</span>Exercise</a></span><ul class="toc-item"><li><span><a href="#Data-Overview" data-toc-modified-id="Data-Overview-8.1"><span class="toc-item-num">8.1&nbsp;&nbsp;</span>Data Overview</a></span></li><li><span><a href="#Bonus-exercises" data-toc-modified-id="Bonus-exercises-8.2"><span class="toc-item-num">8.2&nbsp;&nbsp;</span>Bonus exercises</a></span></li></ul></li></ul></div>
# %% [markdown]
# # Reading & Summarizing CSV Data
#
# Credit: the notebooks in this folder are lightly modified versions of work by Jennifer Walker presented
# at the EOAS python workshop in October, 2018: https://github.com/jenfly/eoas-python
#
#
# %%
from pathlib import Path

import pandas

# %% [markdown]
# ## Learning objectives
#
# * Learn how to read, process and write data in csv/xlsx/tabular format using pandas
#
# * In parts 2 and parts 3:
#
#   * Learn how to download tabular data from websites with a "restful api":
#     - https://stackoverflow.com/questions/671118/what-exactly-is-restful-programming
#
#   * Learn how to clean data by filtering missing values, renaming columns, and writing out
#     processed files for further work
# %% [markdown]
# ## Folder setup
#
# As our project grows more complicated, it's good to have a central
# module that keeps track of important files and sets your scripts
# up so that they can import functions and classes from you modules.
# If you were planning to distribute your project using conda, then
# you would need to write an installation script, which is a fair
# amount of work.   At this stage, it's easier and more flexible to
# store that information in a file that travels along with your notebook.
# We set the "context" for this notebook by importing:
# [context_pandas1.py](context.py)
#

# %%
import context
# %% [markdown]
# ### Subfolder creation
#
# Subsequent notebooks are going to need a place to put raw and processed data.
# We create those folders in the cell below

# %% {"scrolled": true}
processed_dir =  Path("data/processed")
raw_dir = Path("data/raw")
#print(list(raw_dir.glob("*")))
# %% [markdown]
# ## Pandas dataframes vs. numpy arrays
#
# * Dataframes are **column oriented**, arrays are **row oriented**
# * Array items are all of the same dtype (i.e. numpy.float32), dataframe columns can
#   have different types (e.g.strings vs. integers)
# * Dataframe columns can be indexed by name (e.g. "Total area of basin") or by integer index
# * Dataframe rows can be indexed by number of by a special index (e.g. postal code)
# * Dataframe objects have dozens of methods to summarize and manipulate the data they hold, making
#   them similar in features to a lightweight relational database.

# %% [markdown]
# ## Intro to Pandas
#
# - `pandas` = [Python Data Analysis Library](https://pandas.pydata.org/)
# - Best book: [Python for data analysis](https://github.com/wesm/pydata-book) by Wes McKinney
# - Jennifer Walker's [Pandas cheatsheet](pandas-cheatsheet.ipynb)
# - Library for working with **labelled** tabular data (1-D and 2-D)
#   - Data formats include: comma separated values (CSV) and other text files, Excel spreadsheets, HDF5, [and others](https://pandas.pydata.org/pandas-docs/stable/io.html)
# - With `pandas` you can do pretty much everything you would in a spreadsheet, plus a whole lot more!

# %% [markdown]
# > If you're working with higher dimensional data and/or netCDF files, check out the excellent [xarray library](http://xarray.pydata.org/en/stable/), which brings the labelled data power of `pandas` to N-dimensional arrays

# %% [markdown]
# ## Why Pandas?
# - Working with large data files and complex calculations
# - Dealing with messy and missing data
# - Merging data from multiple files
# - Timeseries analysis
# - Automate repetitive tasks
# - Combine with other Python libraries to create beautiful and fully customized visualizations

# %% [markdown]
# ## Reading a CSV file
#
# We'll be working with the file `weather_YVR.csv` in the `data` sub-folder.
# - Environment Canada daily weather measurements at Vancouver Airport from 1938-2017.

# %% [markdown]
# Now let's read the CSV file into our notebook with the function `read_csv` from the `pandas` library.
# - To access functions in the library, we use dot notation again: `pandas.read_csv()`
# - Our input to the read_csv function is the file path as a string: `'data/weather_YVR.csv'`
#
# We'll store the data as a dataframe called `weather`.

# %% [markdown]
# ### The pathlib module
#
# The cell below constructs a [Path object](https://realpython.com/python-pathlib/).  Note the
# direction of the "/" separator.  This would not be the way that we would
# specify a file on windows (that would be 'data\weather_YVR.csv' -- Path objects
# hide this complexity by understanding whether we are working on windows, linux or macos and
# just doing the right thing.

# %%
weather_file = Path("data/weather_YVR.csv")  #subfolder

# %%
weather = pandas.read_csv(weather_file)
#dir(weather)

# %% [markdown] {"slideshow": {"slide_type": "skip"}}
# > Pro Tips!
# - Try typing `pandas.re` and then press Tab and select `read_csv` from the auto-complete options
# - Auto-complete even works for file paths inside a string!

# %%
weather.head()

# %% [markdown]
# - Only the first 30 and last 30 rows are displayed (but the data is all there in our `weather` variable)
# - You may notice some weird `NaN` values&mdash;these represent missing data (`NaN` = "not a number")

# %% [markdown]
# What type of object is `weather`?

# %%
type(weather)

# %% [markdown]
# - `weather` is a **DataFrame**, a data structure from the `pandas` library
#   - A DataFrame is a 2-dimensional array (organized into rows and columns, like a table in a spreadsheet)

# %% [markdown]
# - When we display `weather`, the integer numbers in bold on the left are the DataFrame's **index**
#   - In this case, the index is simply a range of integers corresponding with the row numbers

# %%
weather

# %% [markdown]
# For large DataFrames, it's often useful to display just the first few or last few rows:

# %%
weather.

# %% [markdown] {"slideshow": {"slide_type": "fragment"}}
# The `head` method returns a new DataFrame consisting of the first `n` rows (default 5)
#
#
# > Pro Tips!
# > - To display the documentation for this method, you can run the command `weather.head?` in your Jupyter notebook
# > - To see other methods available for the DataFrame, type `weather.` followed by Tab for auto-complete options

# %% [markdown]
# First two rows:

# %%
weather.iloc[100,2]

# %%
# Last four rows:

# %%
weather.tail(4)

# %% [markdown]
# ## Data at a Glance
#
# `pandas` provides many ways to quickly and easily summarize your data:
#  - How many rows and columns are there?
#  - What are all the column names and what type of data is in each column?

# %% [markdown]
# - Numerical data: What is the average and range of the values?
# - Text data: What are the unique values and how often does each occur?
# - How many values are missing in each column or row?

# %% [markdown]
# ### Number of rows and columns:

# %%
weather.shape

# %%
# - The DataFrame `weather` has 29190 rows and 10 columns
# - The index does not count as a column
# - Notice there are no parentheses at the end of `weather.shape`
# - `shape` is a **data attribute** of the variable `weather`

# %%
type(weather.shape)

# %%
# The data in the `shape` attribute is stored as a **tuple**, which is similar to a list.
#
# - Items in a tuple are enclosed in `()` instead of `[]`
# - Tuples are immutable - you can't modify individual items inside a tuple

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# - Within a column of a DataFrame, the data must all be of the same type
# - We can find out the names and data types of each column from the `dtypes` attribute:

# %%
weather.dtypes

# %% [markdown]
# In a `pandas` DataFrame, a column containing text data (or containing a mix of text and numbers) is assigned a `dtype` of `object` and is treated as a column of strings.
#
# `int64` and `float64` are integer and float, respectively.
# - The 64 at the end means that they are stored as 64-bit numbers in memory
# - These data types are equivalent to `int` and `float` in Python (`pandas` is a just a bit more explicit in how it names them)

# %% [markdown]
# If we just want a list of the column names, we can use the `columns` attribute:

# %% {"scrolled": true, "slideshow": {"slide_type": "-"}}
weather.columns

# %% [markdown]
# ### Simple Summary Statistics
#
# The `describe` method computes simple summary statistics and returns them as a DataFrame:

# %%
weather.describe()

# %% [markdown]
# The `describe` method is a way to quickly summarize the averages, extremes, and variability of each numerical data column.

# %% [markdown]
# You can look at each statistic individually with methods such as `mean`, `median`, `min`, `max`,`std`, and `count`

# %%
weather.mean()

# %% [markdown]
# ## Exercise
#
# For this exercise, we will explore data about countries around the world, combined from multiple sources by the [Gapminder foundation](https://www.gapminder.org/about-gapminder/).

# %% [markdown]
# Gapminder is an independent Swedish foundation that fights devastating misconceptions about global development and promotes a fact-based world view through the production of free teaching and data exploration resources.

# %% [markdown]
# ### Data Overview
#
# The columns of `data/gapminder_world_data_2018.csv` are:
#
# | Column                | Description                        |
# |-----------------------|------------------------------------|
# | country               | Country name                       |
# | population            | Population in the country |
# | region                | Continent the country belongs to   |
# | sub_region            | Sub regions as defined by          |
# | income_group          | Income group [as specified by the world bank](https://datahelpdesk.worldbank.org/knowledgebase/articles/378833-how-are-the-income-group-thresholds-determined)                  |
# | life_expectancy       | The average number of years a newborn child would <br>live if mortality patterns were to stay the same |
# | gdp_per_capita         | GDP per capita (in USD) adjusted <br>for differences in purchasing power|
# | children_per_woman    | Number of children born to each woman|
# | child_mortality       | Deaths of children under 5 years <br>of age per 1000 live births|
# | pop_density           | Average number of people per km$^2$|

# %% [markdown]
# > You may want to refer to the [Pandas cheatsheet](pandas-cheatsheet.ipynb) as you work through the exercises.
#
# **a)** Read the file `data/gapminder_world_data_2018.csv` into a new DataFrame `world` and display the first 10 rows.

# %% [markdown]
# **b)** How many rows and columns does `world` have?

# %% [markdown]
# **c)** Display the names and data types of each column.

# %% [markdown]
# **d)** Display summary statistics with the `describe` method. What are the lowest and highest populations? How about lowest/highest population densities? Any guesses which countries these might be? (We'll find out the answers in Lesson 4!)

# %% [markdown]
# ### Bonus exercises
#
# **e) Data wrangling - dealing with header rows**
#
# The file `data/raw/weather_YVR_1938.csv` contains the daily weather data for 1938, in the original format downloaded from Environment Canada. Open this file in the JupyterLab CSV viewer to see what it looks like.
#
# > Note that the CSV viewer isn't able to parse the data correctly because of the extra header rows at the beginning.
#
# - Now try reading the file into your notebook with `pandas.read_csv` and see what happens.
#
# If you look at the documentation for `pandas.read_csv`, you'll see a `skiprows` input buried amongst a few dozen other inputs for this function. This input tells `read_csv` how many rows to skip at the beginning of the file.
# - Try reading `data/raw/weather_YVR_1938.csv` again, but this time using a value of `24` for the `skiprows` keyword argument, and display the first 5 rows of the resulting DataFrame.

# %% [markdown]
# **f) Importing a library from a `.py` file**
#
# In the pandas folder, you'll see a file called `ecweather.py`. It is a Python *module*, which is a library contained in a single `.py` file (as opposed to a package, which is multiple `.py` files bundled together).
#
# You can import a library from a local `.py` file with the same syntax as any other library. The library name is just the file name minus the `.py` extension, so to import this library the syntax is:
# ```python
# import ecweather
# ```
#
# - Import `ecweather` into your notebook, and call the function `ecweather.welcome()` to test it. If everything worked ok, it should print a welcome message.
#
