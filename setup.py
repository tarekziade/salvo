from setuptools import setup, find_packages
from salvo import __version__
import sys

install_requires = ["molotov"]
description = ""

for file_ in ("README", "CHANGES", "CONTRIBUTORS"):
    with open("%s.rst" % file_) as f:
        description += f.read() + "\n\n"


classifiers = [
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
]

setup(
    name="salvo",
    version=__version__,
    url="https://github.com/tarekziade/salvo",
    packages=find_packages(),
    long_description=description,
    description="Simple HTTP Load tester",
    author="Tarek Ziade",
    author_email="tarek@ziade.org",
    include_package_data=True,
    zip_safe=False,
    classifiers=classifiers,
    install_requires=install_requires,
    test_suite="unittest.collector",
    entry_points="""
      [console_scripts]
      salvo = salvo.run:main
      """,
)
