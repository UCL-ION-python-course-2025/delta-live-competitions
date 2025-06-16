import os
import pathlib
import sys

# Path hack to allow us to run individual competitor main files and
# tournaments without changing the imports
here = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(here))
sys.path.append(os.path.join(here, "competitor_code"))
