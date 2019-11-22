import site
import sys
from pathlib import Path

curr_dir = Path(__file__).parent.resolve()  # pandas
root_dir = curr_dir.parent
data_dir = curr_dir / "data"
print(f"in context.py, setting root_dir to {root_dir}")
processed_dir = data_dir / "processed"
if not processed_dir.is_dir():
    print(
        f"in context.py, was expecting to find {processed_dir}"
        f"but it seems to be missing, have you run 10-pandas1?"
    )
raw_dir = data_dir / "raw"
if not raw_dir.is_dir():
    print(
        f"in context.py, was expecting to find {raw_dir}"
        f"but it seems to be missing, have you run 10-pandas1?"
    )
sys.path.insert(0, str(root_dir))
sep = "*" * 30
site.removeduppaths()
print(
    (
        f"{sep}\ncontext imported. Front of path:\n"
        f"{sys.path[0]}\n{sys.path[1]}\n{sep}\n"
    )
)
