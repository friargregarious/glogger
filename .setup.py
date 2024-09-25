import json
from setuptools import setup, find_packages
import pathlib
import tomllib as tom

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

data_files = [
    (
        'gslogger', [
            'gslogger/glog.toml',
            'gslogger/template.md', 
            'gslogger/template_sections.md',
            'gslogger/changelog.md', 
            ]
        )
    ]

data = tom.load(here / "gslogger" / "gslog.toml")

setup(
    name=data['app_title'],
    version=".".join(str(x) for x in data['version_number']),
    description="Greg's Simple Changelog Generator",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/friargregarious/glogger",
    author="Friar Gregory Denyes",
    author_email="greg.denyes@gmail.com",
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: Apache Software License",
            # "License-Expression: MIT AND (Apache-2.0 OR BSD-2-Clause)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
        ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    keywords="project, changelog, development",
    packages=find_packages(),
    python_requires=">=3.10, <4",
    install_requires=['jinja2'],        # List your package dependencies here
    # package_data={
    #     "data": ["gslogger/glog.json"],
    # },
   
    data_files=data_files,
    # dependency_links=['jinja2'],
    entry_points={
        'console_scripts': [
            'glog = gslogger.glog:main',
        ],
    },

    project_urls={
        "Bug Reports": "https://github.com/friargregarious/glogger/issues",
        "Funding": "https://paypal.me/friargreg?country.x=CA&locale.x=en_US",
        "Say Thanks!": "https://mastodon.social/@gregarious",
        "Source": "https://github.com/friargregarious/glogger",
    },
)