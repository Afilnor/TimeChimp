from setuptools import setup, find_packages
import sys

sys.path.insert(0, '.')
from timechimp._version import __version__

REQUIREMENTS = [
    line.strip().split()[0]
    for line in open("requirements.txt").readlines()
]

with open('README.md', encoding='utf-8') as f:
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
    install_requires=[REQUIREMENTS],
    keywords=['timechimp'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='timechimp',
    packages=find_packages(exclude=("tests", "docs")),
    platforms=['any'],
    python_requires='>=3.6',
    url='https://github.com/Afilnor/TimeChimp',
    version=__version__,
)
