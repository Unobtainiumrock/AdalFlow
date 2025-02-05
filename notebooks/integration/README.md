# Some Important Pieces Regarding Development of Notebooks
- If you are making changes to the Adalflow library and want to ensure that those new changes are reflected in the notebooks, you must do the following:


## Delete the Dist Folder

Ensure that you've deleted the existing `dist` folder at `adalflow/dist`

```bash
cd adalflow
rm -rf dist/
```

## Re-Build

Re-build using poetry, while inside of `/adalflow`

```bash
cd adalflow
poetry build
```

If done successfully, you should see a `dist/` folder

## Kernel Setup (Optional)

If you didnt' already set up a kernel for jupyter notebook to work with, then run the following:

```bash
poetry run python -m ipykernel install --user --name my-project-kernel
```

## Notebook Setup

Inside of the notebook, we want to ensure that there aren't any previously installed `adalflow` libraries conflicting with us trying to use the newly modified build.

Add a cell at the top of your `*.ipynb` notebook file containing the following:

```python
import glob
import os
import subprocess

# Figure out the correct path to adalflow/dist, relative to *this* notebook
dist_folder = os.path.abspath(os.path.join(os.getcwd(), "../../adalflow/dist"))
# ↑ Adjust '../../' depending on your folder structure

whl_files = glob.glob(os.path.join(dist_folder, '*.whl'))
if whl_files:
    # Sort files by modification time so we get the newest .whl
    whl_files.sort(key=os.path.getmtime, reverse=True)
    latest_whl = whl_files[0]

    subprocess.run(["pip", "uninstall", "-y", "adalflow"], check=True)
    subprocess.run(["pip", "install", "--no-cache-dir", latest_whl], check=True)
else:
    print(f"No .whl file found in {dist_folder}. Ensure you have built the package.")
```

## If There's Still Problems

Be sure to interrupt or restart your Jupyter kernel. Sometimes certain variables and packages are still in memory from previous cell runs.
