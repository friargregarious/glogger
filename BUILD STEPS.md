# steps to take when building and deploying apps

## Introduction

In this guide, we will walk through the process of building and distributing a Python package using Hatchling and Twine.

1. Directory Structure
2. Using my_build_config.py
3. How to use the python environment
4. Building with hatchling
5. Uploading to pypi
6. References

## 0. The Short version

Everytime I want to build a new version of my app, these are the steps.

1. run: `~/my_build_config.py`          # this will generate the configuration files
2. commit changes to git and github     # this will update the github repo
3. run: `hatchling build`               # this will build the package files
4. run: `twine upload dist/vn.n.n/*`    # this will upload the package to pypi
5. run: `mastodon.py`                   # this will post an update status to mastodon

## 1. Directory Structure

```python
GLOGGER     # Project root directory, all tools and configs will be stored here
├── dist    # this is where all the builds will be stored
│   ├── v0.2.63
│   │   ├── gslogger-0.2.63-py2.py3-none-any.whl
│   │   └── gslogger-0.2.63.tar.gz
│   ├── v0.2.65
│   ├── v0.2.68
│   └── v0.2.69
├── src     # everything within this is the package you are deploying
│   └── gslogger            # This is your package directory where your code lives
│       ├── __init__.py     # init file, it is best to have one, even if it's empty.
│       ├── changelog.md    # The changelog for this project
│       ├── extras.py       # extra functions
│       ├── glog.py         # main app module, where the program can be accessed from 
│       ├── jin.py          # this a bastardized jinja templating engine
│       └── version.py      # this is where the app's version number is generated.
├── LICENSE
├── README.md
├── pyproject.toml # this file contains package metadata
└── my_build_config.py # this module collects and writes the build configuration
```

## 2. Using my_build_config.py

To build the package, we use Hatchling. First, we need to run the my_build_config.py file to generate the necessary configuration files.

This app builds a dictionary of conifguration options and outputs them to a toml file.
Many of the options are 

possible outputs include ["Pyproject.toml", "hatch.toml"]
Check with your build tools for which files you will need.
setuptools and hatchling can use a single file Pyproject.toml if all the information is recorded correctly. I will list the needs here.

```python

```

Pyproject.toml
<https://hatch.pypa.io/1.9/config/build/>

```toml
[tool.hatch.build.targets.wheel]
only-include = ["src/foo"]
sources = ["src"]
```

### installing as a script to make your app run from command line

```python
para_dict["project"]["scripts"] = {
    "glog" : 'gslogger.glog:main'
    }
```

will be converted to:

```toml
[project.scripts]
glog = "gslogger.glog:main"
```

### creating entry point so you can install it as a plugin

```python
para_dict["project"]["entry_points"] = {
    "console_scripts": ["glog=src.gslogger.glog:main"]
    }
```

will be converted to:

```toml
[project.entry-points]
console_scripts = [
    "glog = gslogger.glog:main"
]
```

## 3. How to use the python environment

What does `python -m pip install -e`. do?

Let’s break down `python -m pip install -e`.

`python -m pip install -e`. Installs your package into the current active Python environment in editable mode (-e). Installing your package in editable mode, allows you to work on your code and then test the updates interactively in your favorite Python interface. One important caveat of editable mode is that every time you update your code, you may need to restart Python.

If you wish to install the package regularly (not in editable mode) you can use:

'python -m pip install .'

Using python -m when calling pip

Above, you usepython -m to call the version of pip installed into your current active environment. python -m is important to ensure that you are calling the version of pip installed in your current environment.

## 4. Building with hatchling

The command line I use is: 

```cmd
~/hatchling build
```

it's that easy.
as long as you run the my_build_config.py file first, it should work.

```cmd
GLOGGER     # Project root directory, all tools and configs will be stored here
└── dist    # this is where all the builds will be stored
    ├── v0.2.63
    │   ├── gslogger-0.2.63-py2.py3-none-any.whl
    │   └── gslogger-0.2.63.tar.gz
    ├── v0.2.65
    ├── v0.2.68
    └── v0.2.69
```

I want to build the latest version of the app and have the .whl & .tar.gz files automatically dropped in the dist folder specific to the current version.

## 5. Uploading to pypi

we are using twine, it usually asks for a token but I've stored them in a .pypirc file where they are safe.

the command line is:

```cmd
~/python -m twine upload dist/*
```

I want to make a script that will upload my app to pypi but from the latest build folder.


## 6. References & Links

- pypi.org <https://pypi.org/>
- hatchling <https://hatch.pypa.io/>
- twine <https://pypi.org/project/twine/>
- python-package-guide <https://www.pyopensci.org/python-package-guide/tutorials/installable-code.html>
- hatch config https://hatch.pypa.io/1.9/config/build/
- 
