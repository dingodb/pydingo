#!/usr/bin/env python
#

import os

import setuptools

long_desc = """# dingodb

dingodb is a SDK for  vector database DingoDB, .
"""


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "r", encoding="utf-8") as fh:
        return fh.read()


setuptools.setup(
    name="dingodb",
    version=read("dingodb/__version__").strip(),
    description="dingodb is dingodb sdk",
    license="Proprietary License",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://www.dingodb.com/",
    project_urls={
        "Homepage": "https://www.dingodb.com/",
        "Documentation": "https://dingodb.readthedocs.io/en/latest/",
    },
    author="DingoDB",
    author_email="dingodb@zetyun.com",
    keywords="dingodb",
    packages=setuptools.find_packages(),
    install_requires=read("requirements.txt"),
    extras_require={
    },
    include_package_data=True,
    python_requires=">=3.7",
    entry_points={
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
