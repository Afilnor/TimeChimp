from setuptools import setup, find_packages
from os import path

from timechimp.version import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    author='Florian Dauphin',
    author_email='dauphin.florian@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    description='TimeChimp API Python SDK',
    download_url='https://github.com/Afilnor/TimeChimp/archive/refs/heads/master.zip',
    install_requires=[
        "requests",
        "pytest"
    ],
    keywords=[
        'timechimp'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='timechimp',
    packages=find_packages(exclude=("tests",)),
    platforms=['any'],
    python_requires='>=3.6',
    url='https://github.com/Afilnor/TimeChimp',
    version=__version__,
)