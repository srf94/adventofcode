from distutils.core import setup
from Cython.Build import cythonize


# Run:
# python setup.py build_ext --inplace

setup(
    ext_modules = cythonize("vm.pyx")
)
