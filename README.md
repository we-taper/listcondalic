# List license information from package specification file

## Conda

For Conda environment:

1. Create an environment specification file. Please follow [this guide](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#exporting-the-environment-yml-file)
   to create this file.
2. Edit the file and remove all unnecessary dependencies (very important, otherwise the
   it is easy to get inundated with too much packages). For example, remove things like `ipython`,
   `ipykernel`, which are used for purpose other than the library itself.
3. Install this package.
4. Run:

```bash
listcondalic conda environment.yml > output.json
```

Here `environment.yml` should be the environment specification file.
The package licence information will be saved at `output.json`.

## Pip

Note: We use [liccheck](https://pypi.org/project/liccheck/) internally to produce the analysis.

1. Create your package specification file (e.g. `requirements.txt`) 
   including all the packages required.
   [pipreqs](https://pypi.org/project/pipreqs/) is a good helping tool for this as well.
2. Install this package
3. Run:

```bash
listcondalic pip requirements.txt > output.json
```

The package licence information will be saved at `output.json`.
