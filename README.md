Convenience library for hyper-parameters management for deep learning development projects.
 
## Pre-requisites

- Python 3.7 or higher

## Why use hparams?

Hparams is a library mainly designed to make Deep learning development and experimentation easy to manage and track:
  
- Specify all run parameters (number of GPUs, model parameters, train parameters, etc) in one `.cfg` file.  
- Hparams evaluates any expression used as "value" in the `.cfg` file. "value" can be any basic python object `(floats, strings, lists, etc)` or any python basic expression `(1/2, max
(3, 7), etc.)` as long as the evaluation does not require any library importations or does not rely on other values from the `.cfg`.
- Hparams saves the configuration of previous runs for reproducibility, resuming training, etc.  
- All hparams are saved by name, and re-using the same name will recall the old run instead of making a new one.  
- The `.cfg` file is split into sections for readability, and all parameters in the file are accessible as class attributes in the codebase for convenience.  
- The HParams object keeps a global state throughout all the scripts in the code, so it can be imported and used in all scripts.

## Installation

```
pip install --upgrade git+https://github.com/Rayhane-mamah/hparams
```

## How to use?

### Config file basics

Hparams library parses a `.cfg` file (by default `hparams.cfg`) and makes its arguments accessible within a python project.

A basic `hparams.cfg` looks like follows:

```ini
[run]
name = some_run_name
some_other_run_param = some_value
...

[some_other_section]
some_other_param = some_other_value
...

```

#### Notes:

- `run.name` parameter is mandatory in any `.cfg` to be read by hparams library.
- Any argument in `hparams.cfg` can be accessed in code with `hparams.section_name.argument_name`.

### Basic usage

In the entrypoint script of the project, instantiate the hparams object:

```python
from hparams import HParams
...

# The object name of HParams IS NOT the same as the run.name.
# Signature: HParams(project_path (location of the .cfg file), hparams_filename (without extension), name (name of the hparams object))
hparams = HParams('.', name="some_object_name")
...
# Use some parameter from the hparams.cfg file
print(hparams.some_other_run_param)
```

The above command creates a global instance of the hparams file and remembers it by `name`. In any other script where one wants to use the hparams, it's possible to simple load the
 instantiated hparams by name:
 
 ```python
from hparams import HParams
...

# Load an already instantiated HParams object.
hparams = HParams.get_hparams_by_name("some_object_name")
...
# Use some parameter from the hparams.cfg file
print(hparams.run.name)
print(hparams.some_other_section.some_other_param)
```

Instantiating an hparams object anywhere in the project saves the read `.cfg` file (by default `hparams.cfg`), makes a saved copy of the `.cfg` under `logs-<run.name>/hparams-<run
.name>.cfg`. This saved copy is loaded in future runs instead of `hparams.cfg` as long as the `run.name` argument in `hparams.cfg` is kept the same. We use this copying process for
 safety of future execution, reproducibility and for mistakes minimization.
 
To restart an already existing `run.name`, then one should remove the saved copy:

```bash
rm -r logs-<run.name>
```

### Beyond the default config file

It is also possible to instantiate the hparams object from a different `.cfg` file:

```python
from hparams import HParams

# Do not define the extension in the hparams_filename
hparams = HParams('.', hparams_filename='some_other_cfg_name', name='some_object_name')
```

### GCS backup

If your code is saving tensorboard files, model checkpoints or other files to GCS and you want hparams to also back itself up to a GCS bucket:

```python
from hparams import HParams

# Define both the gcs project name and the gcs bucket path
hparams = HParams('.', gcs_backup_project='some_project_name', gcs_backup_bucket='some_bucket_path', name='some_name')
```

The GCS integration of hparams is a simple backup copy. Your local version is always the True one, and the gcs version is its replica.