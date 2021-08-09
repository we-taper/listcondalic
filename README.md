# List license information from package specification file

## Conda

For Conda environment:

1. Create an environment specification file. Please follow [this guide](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#exporting-the-environment-yml-file)
   to create this file.
2. Edit the file and remove all unnecessary dependencies (very important, otherwise the
   it is easy to get inundated with too many packages). For example, remove things like `ipython`,
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

## Existing problems

This packages isn't quite clever yet:

- It tries to skip a few packages such as `python`, `setuptools`, `wheel` and `pip`.
  Hopefully, we won't neglect any important packages.
- It only understand very basic package specifications in the conda environment file.
  Complicated package sources will likely create bugs in the result. In particular,
  it does not suppoprt:
  - "." (dot) package, or in general, if you specify a path to a local python package,
    this library will not attempt to analyze the packaged located in that folder. Instead,
    it will be registered as a package named, e.g. ".", and therefore it will report the
    package's licence as `NotFound`.
  - GitHub URL package, for reasons mentioned above.

# GitHub action template

For a pip-based `requirements.txt`:

```yaml
name: Report licence status

on:
  workflow_dispatch:

jobs:
  check-using-pip:
    name: Report using a pip environment
    runs-on: ubuntu-20.04
    steps:
    - uses: actions/checkout@master
    - name: Set up Python 3.7
      uses: actions/setup-python@v1
      with:
        python-version: 3.7
    - name: Install packages and listcondalic
      run: |
        pip install -r requirements.txt
        pip install listcondalic
    - name: Produce report
      run: listcondalic pip requirements.txt
```

For a conda produced `environment.yml`:

```yml
name: Report licence status

on:
  workflow_dispatch:

jobs:
  check-using-conda:
    name: Report using a conda environment
    runs-on: ubuntu-20.04
    steps:
    - uses: actions/checkout@master
    - name: Install conda and prepare the environment
      uses: conda-incubator/setup-miniconda@v2
      with:
        activate-environment: YOUR_ENVIRONMENT_NAME
        environment-file: environment.yml
        python-version: 3.7
        auto-activate-base: false
    - name: Install listcondalic
      shell: 'bash -l {0}' # this is required by the conda action
      run: pip install listcondalic
    - name: Produce report
      shell: 'bash -l {0}' # this is required by the conda action
      run: listcondalic conda environment.yml
```
