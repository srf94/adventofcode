from distutils.core import setup
from Cython.Build import cythonize


# Build with:
# python setup.py build_ext --inplace

setup(ext_modules=cythonize("vm.pyx"))
