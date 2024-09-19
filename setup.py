import os
import json
from setuptools import setup, find_packages

data_files = [('gslogger', ['gslogger/glog.json'])]

# with open(os.path.join(os.path.dirname(__file__), "glogger", "glog.json"), "r", encoding="utf-8") as f:
with open("gslogger/glog.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())

setup(
    name=data['app_title'],
    version=".".join(str(x) for x in data['version_number']),
    # packages=['glogger'],
    # packages=['glogger', 'jinja2'],
    packages=find_packages(),
    data_files=data_files,
    dependency_links=['jinja2'],
    entry_points={
        'console_scripts': [
            'glog = gslogger.glog:main',
        ],
    },
)