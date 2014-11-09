from distutils.core import setup
import tec

setup(name='tec',
      version=tec.__version__,
      author='Joshua Ryan Smith',
      author_email='joshua.r.smith@gmail.com',
      packages=['tec','tec/models'],
      url='https://github.com/jrsmith3/tec',
      description='A python package for simulating vacuum thermionic energy conversion devices.',
      install_requires=[
      	'numpy',
      	'scipy',
      	'matplotlib',
      	],
	  test_suite='nose.collector',
      tests_require=['nose'],
      license='',
      zip_safe=False)