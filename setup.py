import io
import re
from setuptools import setup

with io.open('lcls2widgets/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name="lcls2widgets",
    version=version,
    description='LCLS2 Widgets',
    long_description='The package used at LCLS-II for guis for AMI and OM',
    author='Seshu Yamajala',
    author_email='',
    url='http://github.com/slac-lcls/lcls2widgets',
    packages=["lcls2widgets"],
    package_data={},
    install_requires=['numpy', 'pyzmq', 'pyqtgraph', 'asyncqt'],
    classifiers=[
        'Development Status :: 1 - Planning'
        'Environment :: Other Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    zip_safe=False,
)
