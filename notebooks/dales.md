---
jupyter:
  jupytext:
    cell_metadata_filter: -all
    formats: ipynb,md
    notebook_metadata_filter: all,-language_info,-toc,-latex_envs
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.2.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
  latex_envs:
    LaTeX_envs_menu_present: true
    autoclose: false
    autocomplete: true
    bibliofile: biblio.bib
    cite_by: apalike
    current_citInitial: 1
    eqLabelWithNumbers: true
    eqNumInitial: 1
    hotkeys:
      equation: meta-9
    labels_anchors: false
    latex_user_defs: false
    report_style_numbering: false
    user_envs_cfg: false
  toc:
    base_numbering: 1
    nav_menu: {}
    number_sections: false
    sideBar: false
    skip_h1_title: true
    title_cell: Table of Contents
    title_sidebar: Contents
    toc_cell: true
    toc_position:
      height: calc(100% - 180px)
      left: 10px
      top: 150px
      width: 323.594px
    toc_section_display: false
    toc_window_display: false
---

<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Optimum-links" data-toc-modified-id="Optimum-links-1">Optimum links</a></span></li><li><span><a href="#Links:" data-toc-modified-id="Links:-2">Links:</a></span></li><li><span><a href="#Settiing-up-your-environment" data-toc-modified-id="Settiing-up-your-environment-3">Settiing up your environment</a></span></li><li><span><a href="#Running-helloworld" data-toc-modified-id="Running-helloworld-4">Running helloworld</a></span></li><li><span><a href="#Running-the-cblcoarse-case" data-toc-modified-id="Running-the-cblcoarse-case-5">Running the cblcoarse case</a></span></li><li><span><a href="#Running-other-cases" data-toc-modified-id="Running-other-cases-6">Running other cases</a></span></li></ul></div>


# Introduction LES on optimum


## Optimum links

* Read https://www.optimum.eos.ubc.ca/Docs/

## Links:

1. [Software carpentry lesson on bash](https://swcarpentry.github.io/shell-novice/)

1. [Dales student manual](http://www.srderoode.nl/Students/dales_course_instructions_v2017.pdf)

1. [Dales general intro](http://www.srderoode.nl/pubs/getting_started_with_DALES41.pdf)

1. [Dales namoption overview](http://www.srderoode.nl/pubs/Namoptions.pdf)

1. [Dales github repo (ubc fork)](https://github.com/phaustin/dales)

1. [Dales publication](https://www.geosci-model-dev.net/3/415/2010/)



<!-- #region -->
## Settiing up your environment

On optimum -- first copy my .bashrc to your home directory:

```
cp ~paustin/.bashrc ~/.bashrc
```

refresh the paths executing the following at your bash prompt:

```
. ~/.bashrc
```

## Running helloworld

If this works, you should be in the conda environment "work" and be able to run git.  Use git to clone dales into a folder called `repos` and check out the ubc branch:

```
mkdir -p ~/repos
cd ~/repos
git clone https://github.com/phaustin/dales.git
cd dales
git checkout -b ubc origin/ubc
```

To start, compile and run [helloword.f90](https://github.com/phaustin/dales/blob/ubc/cases/helloworld/helloworld.f90)
following the instructions
at the [github readme](https://github.com/phaustin/dales/tree/ubc/cases/helloworld)

You should see output like:

```
(work) [paustin@n037 build]$ mpiexec -n 20 ~/bin/helloworld
mpiexec -n 20 ~/bin/helloworld
Hello, World! I am process  1 of 20 on n037.
Hello, World! I am process  2 of 20 on n037.
Hello, World! I am process  3 of 20 on n037.
Hello, World! I am process  4 of 20 on n037.
```




<!-- #endregion -->

## Running the cblcoarse case



<!-- #region -->
I'll assume your user name is `myname`.  You should have a directory on `/scratch/paustin/myname` to store your runs.  Copy the cblcoarse case
to that directory:

```
cp ~/repos/dales/cases/cblcoarse /scratch/paustin/myname/.
cd /scratch/paustin/myname/cblcoarse
Iqsub 0.5 1 20  #(arguments: 0.5 hours with 1 node with 20 cores)
mpiexec -n 2 /home/paustin/paustin/bin/dales_standard
```

This should produce 2 netcdf files: `profiles.001.nc` and `tmser.001.nc`

To copy these to your local machine use scp.

```
scp -r myname@optimum.eos.ubc.ca:/scratch/paustin/myname/*.nc .
```

Alternatively, you can copy them to the directory `~/public_html` and 
view/download them with a browser at https://www.optimum.eos.ubc.ca/~myname/

<!-- #endregion -->

## Running other cases

<!-- #region -->
Running other cases is similar, as long as they use the standard driver file, 
[moduser.f90](https://github.com/phaustin/dales/blob/ubc/cases/standard/moduser.f90) which
comments out user-defined forcing and radiation routines.  To customize these, as with, for
example this case that uses user-defined [radiation](https://github.com/phaustin/dales/blob/ubc/cases/dycoms_rf02/moduser.f90), you need to
tell cmake to copy over the correct moduser.f90 by defining the [case](https://github.com/phaustin/dales/blob/ubc/CMakeLists.txt#L71):

```
cmake -Dcase=dycoms_rf02
```
<!-- #endregion -->

```python

```
