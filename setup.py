from setuptools import setup, find_packages

setup(
    name = "a500",
    packages=find_packages(),
    entry_points={
          'console_scripts': [
              'killprocs = a500.utils.killprocs:main',
              'pyncdump = a500.utils.ncdump:main'
          ]
    },

)
