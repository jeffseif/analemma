from setuptools import setup

from analemma import __author__
from analemma import __email__
from analemma import __program__
from analemma import __url__
from analemma import __version__


setup(
    author=__author__,
    author_email=__email__,
    install_requires=["python-dateutil"],
    name=__program__,
    packages=[__program__],
    platforms="all",
    setup_requires=[
        "setuptools",
    ],
    url=__url__,
    version=__version__,
)
