"""
define the path to important folders without having
to install anything -- just do:

import contenxt

then the path for the data directory is

context.data_dir

"""
from pathlib import Path
path=Path(__file__).resolve()   #this file
this_dir = path.parent  #this folder
if this_dir.name == 'python':
    notebooks_dir = this_dir.parent
else:
    notebooks_dir = this_dir
root_dir = notebooks_dir.parent
data_dir = root_dir / Path('data')
test_dir = root_dir / Path('test_data')
map_dir = root_dir / Path('map_data')
print(f"through {__file__}")



