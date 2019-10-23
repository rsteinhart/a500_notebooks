"""
loop throught the notebooks in the
file notebooks.json  and first convert from py:percent
to ipynb using jupytext, then run and convert to html
using jupyter nbconvert

The notebooks are assumend to be in the folder  context.notebooks_dir
and the output file context.this_dir / Path('html_files') is created
to hold the html versions of the notebooks
"""

from pathlib import Path
import json
import context
from jupytext.cli import jupytext
import context
import pdb
import subprocess

in_file="notebooks.json"
with open(in_file,'r') as input:
    notebooks_dict=json.load(input)
print(f"processing these notebooks: {notebooks_dict}")

all_notebooks=[]
for key, notebooklist in notebooks_dict.items():
    all_notebooks.extend(notebooklist)

html_dir = context.this_dir / Path('html_files')
html_dir.mkdir(parents=True, exist_ok=True)
for a_notebook in all_notebooks:
    the_notebook = Path(context.notebook_dir / a_notebook).with_suffix('.py')
    the_output = the_notebook.with_suffix('.ipynb')
    the_command = [str(the_notebook),'--to','notebook','--output',str(the_output)]
    jupytext(the_command)
    to_html = ['jupyter','nbconvert','--ExecutePreprocessor.timeout=900','--to',
               'html','--output-dir',str(html_dir),'--execute',str(the_output)]
    ret=subprocess.call(to_html)
    print(f"converting {the_output}")
    if ret != 0:
        print(f"hit a problem, conversion failed")
