# import setuptools
from setuptools import find_packages
from pathlib import Path
import toml, json
from src.gslogger import __version__, __author__, __author_email__

'''
GLOGGER # This is your project directory
├── src
│   └── gslogger # This is your package directory where your code lives
│       ├── ch-logs
│       │   └── log_store.json
│       ├── __about__.py
│       ├── __init__.py
│       ├── changelog.md
│       ├── extras.py
│       ├── glog.json
│       ├── glog.py
│       ├── jin.py
│       └── version.py
├── LICENSE
├── README.md
└── pyproject.toml # this file contains package metadata
'''

here = Path(__file__).parent.resolve() # GLOGGER/
print(f"here: {here}")
pkg_path = list(here.glob("src/**/glog.py"))[0].parent

_findlist = [str(fp) for fp in pkg_path.glob("*.py")]
mod_list = [fn.split("\\")[-1] for fn in _findlist if not fn.startswith("__")]

app_config = json.loads( 
                        list(here.glob("src/**/glog.json"))[0].read_text(encoding="utf-8")
                        )

print(f"Keys in app_config: {app_config.keys()}")

app_name = app_config['app']['app_title'].lower()

# long description text
README =  (here / "README.md").read_text(encoding="utf-8")

# base build parameters
para_dict = {
    "build-system": {
        "requires": ["hatchling"],
        "build-backend": "hatchling.build",}
    }

para_dict["project"] = {
    "authors":[{"name" : __author__, "email" : __author_email__,}, ],
    "name" : app_name,
    "version" : __version__,
    "description" : "Greg's Simple Changelog Generator",
    "long_description" : README,
    "long_description_content_type" : "text/markdown", 
    "keywords" : ["project", "changelog", "development"],
    "url" : "https://github.com/friargregarious/glogger",
    "requires_python" : '>=3.11.0,<4',
    "package_dir" : {'': str(pkg_path)},
    "packages" : find_packages(),
    "py_modules" : mod_list,
    "include_package_data" : True,
    "entry_points" : {'console_scripts' : ["glog=gslogger.glog:main"]},
    "project_urls": {
        "Bug Reports": "https://github.com/friargregarious/glogger/issues",
        "Funding": "https://paypal.me/friargreg?country.x=CA&locale.x=en_US",
        "Say Thanks!": "https://mastodon.social/@gregarious",
        },
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


targets = [
    (here / "pyproject.toml"),
    (here / "hatchling.toml"),
]

for target in targets:
    target.write_text(toml.dumps(para_dict), encoding="utf-8")

def get_parameters():
    return para_dict
