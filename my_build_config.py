# import setuptools
import os
from setuptools import find_packages
from pathlib import Path
import toml, json
try:
    from src.gslogger import __version__, __author__, __author_email__
except ImportError:
    from gslogger import __version__, __author__, __author_email__

"""
GLOGGER # This is your project directory
├── src
│   └── gslogger # This is your package directory where your code lives
│       ├── __init__.py
│       ├── changelog.md
│       ├── extras.py
│       ├── glog.py
│       ├── jin.py
│       └── version.py
├── LICENSE
├── README.md
└── pyproject.toml # this file contains package metadata
"""

try:
    here = Path(__file__).parent.resolve()  # GLOGGER/

    # these are the target files we're building
    targets = [
        here / "pyproject.toml",
        # here / "hatchling.toml",
    ]

    # delete all files found in targets
    for target in targets:
            if target.exists():
                target.unlink(missing_ok=True)

    # pkg_path = (here / "src" / "gslogger").parent
    pkg_path = here / "src" / "gslogger"

    _findlist = [str(fp) for fp in pkg_path.glob("*.py")]
    mod_list = [fn.split("\\")[-1] for fn in _findlist if not fn.startswith("__")]

    app_config = json.loads((here / "glog.json").read_text(encoding="utf-8"))

    # print(f"Keys in app_config: {app_config.keys()}")

    app_name = app_config["app"]["app_title"].lower()

    # base build parameters
    para_dict = {
        "build-system": {
            "requires": ["hatchling"],
            "build-backend": "hatchling.build",
        }
    }

    # long description is found in the root of para_dict and not under [project]

    # long description text
    README = (here / "README.md").read_text(encoding="utf-8")

    para_dict["long_description"] = README
    para_dict["long_description_content_type"] = "text/markdown"


    # building the [project] section
    para_dict["project"] = {
        "authors": [
            {
                "name": __author__,
                "email": __author_email__,
            },
        ],
        "name": app_name,
        "version": __version__,
        "description": "Greg's Simple Changelog Generator",
        "readme": {"file" : "README.md", "content-type" : "text/markdown"},
        "keywords": ["project", "changelog", "development"],
        "url": "https://github.com/friargregarious/glogger",
        "requires_python": ">=3.11.0,<4",
        "package_dir": {"": str(pkg_path)},
        "packages": find_packages(),
        # "py_modules" : mod_list,
        # "include_package_data" : True,
        "project_urls": {
            "repository": "https://github.com/friargregarious/glogger",
            "PyPI": "https://pypi.org/project/gslogger/",
            "Bug Reports": "https://github.com/friargregarious/glogger/issues",
            "Funding": "https://paypal.me/friargreg?country.x=CA&locale.x=en_US",
            "Say Thanks!": "https://mastodon.social/@gregarious",
        },
    }
    
        # "scripts": ['glog'],
    para_dict["project"]["scripts"] = {
        "glog" : 'gslogger.glog:main'
        }
    

    para_dict["project"]["entry_points"] = {
        "console_scripts": ["glog=src.gslogger.glog:main"]
    }

    para_dict["project"]["classifiers"] = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        # f"License-file :: {str((here / 'LICENSE').resolve())}",
        # f"License-text :: {(here / 'LICENSE').read_text(encoding='utf-8')}",
    ]


    # [tool.setuptools.packages.find]
    # where = ["src"]

    # [tool.setuptools.package-data]
    # mypkg = ["*.txt", "*.rst"]
    para_dict["tool"] = {
        "setuptools": {
            "packages": {"find": {"where": ["src"]}},
            "package-data": {"gslogger": ["*.md"]},
        },
    }

    # redirects the .whl & .tar.gz files to a custom build directory
    save_directory = str(here / "dist" / __version__)
    para_dict["tool"] = {"hatch": {"build" : {"directory" : save_directory}}}

    for target in targets:
        target.write_text(toml.dumps(para_dict), encoding="utf-8")

    print(f"Success building configs! \n{'\n'.join(map(str, targets))}")
except Exception as e:
    print(f"ERROR Building Configs: {e}")

def get_parameters():
    return para_dict


