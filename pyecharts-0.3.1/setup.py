# coding=utf-8

import os
from setuptools import setup, find_packages

try:
    from jupyterpip import cmdclass
except ImportError:
    import pip
    import importlib

    pip.main(['install', 'jupyter-pip'])
    cmdclass = importlib.import_module('jupyterpip').cmdclass


__title__ = 'pyecharts'
__description__ = 'Python echarts, make charting easier'
__url__ = 'https://github.com/chenjiandongx/pyecharts'
__author_email__ = 'chenjiandongx@qq.com'
__license__ = 'MIT'

__requires__ = ['pillow',
                'jinja2',
                'future',
                'jupyter-pip>=0.3.1']

__keywords__ = ['Echarts',
                'charts',
                'plotting-tool']

__jupyter_echarts__ = 'pyecharts/templates/js/echarts'

# Load the package's _version.py module as a dictionary.
here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, __title__, '_version.py')) as f:
    exec(f.read(), about)

setup(
    name=__title__,
    version=about['__version__'],
    description=__description__,
    url=__url__,
    author=about['__author__'],
    author_email=__author_email__,
    license=__license__,
    packages=find_packages(exclude=('test',)),
    keywords=__keywords__,
    install_requires=__requires__,
    zip_safe=False,
    include_package_data=True,
    cmdclass=cmdclass(__jupyter_echarts__, enable="echarts/main"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
