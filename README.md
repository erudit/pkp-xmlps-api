# Python API to PKP XML Parsing Service

# Requirements

* Python 3.*
    * installing [Anaconda Python distribution](https://www.continuum.io/downloads) is a convenient way to have a locally and easily disposable Python 3 environment

# Configuration

* PKP XML Parsing Service account
    1. get your username and password on the service website
    2. create a `conf.py` file at the root of the project
    3. copy the USER_EMAIL and PASSWORD parameters from `settings.py`

# Usage

* *These examples assume Python 3 as your default Python interpreter on your system.*
* *These examples assume you current working directory is the root of the project*
```
$ cd pkp-xmlps-api
```

## Submit

```
$ python api.py submit --help
```

### Single file

* invoke the API on the command line, passing the path to the file you want to parse with the PKP XML Parsing Service.
```
$ python xmlps.py submit path/to/my/data/file.doc
```

### Multiple files

* place your files in a directory
    * they can be in any subdirectories
    * **WARNING** : all `.pdf`, `.doc`, `.docx` and `.odt` files will be submitted
* invoke the submit command on the command line and give the directory path
    * *default directory is `data/` at the root of the project*
```
$ python xmlps.py submit path/to/my/data
```

## Retrieve

```
$ python api.py submit --help
```

File and directory parameter behavior same as `submit` command (same default directory also).

### Single file

```
$ python xmlps.py retrieve path/to/my/data/file.doc
```

### Multiple files
```
$ python xmlps.py retrieve path/to/my/data
```

## Parse

```
$ python api.py parse --help
```

Submits and retrieves the result.

File and directory parameter behavior same as `submit` command (same default directory also).

By default waits 60 seconds between submission and retrieval commands.
Default can be changed in the `conf.py` (see *Configuration* section before) or
overrided manually with the  
Ex.: for a 2 minutes (120 seconds) wait between commands
```
$ python xmlps.py parse --wait 120
```
