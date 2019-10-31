"""
define the path to important folders without having
to install anything -- just do:

import context

then the path for the data directory is

context.data_dir

"""
import sys
from pathlib import Path
path=Path(__file__).resolve()   #this file
this_dir = path.parent  #this folder
data_dir = this_dir / 'data'
