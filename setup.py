#from setuptools import setup, find_packages
from distutils.core import setup
from glob import glob
import shutil
try:
    import py2exe
except ImportError:
    py2exe_available = False
else:
    py2exe_available = True

setup(
    name='666 Luftballons',
    version='0.2',
    author="Gin 'n Pythonic (Thijs Jonkman & Jeroen Vloothuis)",
    author_email='jeroen.vloothuis@xs4all.nl',
    description='A action based puzzle game',
    license='GPL',
    packages=('lib',),
    windows=[{
        'script': '666luftballons.py'
        }]
)

shutil.copytree('data', 'dist/data')
