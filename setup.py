import json
from setuptools import setup

with open("glogger/glog.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())

setup(
    name=data['app_title'],
    version=".".join(str(x) for x in data['version_number']),
    packages=['glogger'],
    # packages=['glogger', 'jinja2'],
    dependency_links=['jinja2'],
    entry_points={
        'console_scripts': [
            'glog = glogger.glog:main',
        ],
    },
)