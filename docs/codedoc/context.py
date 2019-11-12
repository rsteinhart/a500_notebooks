from pathlib import Path
import sys

this_dir = Path(__file__).parent
root_dir = this_dir.parents[2]  # a500_notebooks

sys.path.insert(0, str(root_dir))
sep = "*" * 30
print(f"{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n{sys.path[1]}\n{sep}\n")
