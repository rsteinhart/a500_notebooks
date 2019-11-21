import sys
from pathlib import Path

path = Path(__file__).resolve()  # this file
this_dir = path.parent  # this folder
root_dir = this_dir.parents[1]
data_dir = root_dir / Path("data")
