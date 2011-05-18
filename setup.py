import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES


NAME = 'dfuzz'
VERSION = '0.5'

srcdir = 'dfuzz'

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
long_description = f.read().strip()
f.close()

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)


for dirpath, dirnames, filenames in os.walk(srcdir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        data_files.append([dirpath,
            [os.path.join(dirpath, f) for f in filenames]])

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
long_description = f.read().strip()
f.close()

# put data files to the same path as sources
for scheme in INSTALL_SCHEMES.values(): 
    scheme['data'] = scheme['purelib'] 

setup(name=NAME,
    version=VERSION,
    description='dfuzz - automated daemon fuzzer',
    long_description=long_description,
    author='Richard Marko',
    author_email='rissko@gmail.com',
    url='http://github.com/sorki/dfuzz',
    scripts=['dfuzz/dfuzz', 'dfuzz/incident_viewer'],
    package_dir={'dfuzz': 'dfuzz'},
    packages=packages,
    data_files=data_files,
    test_suite='dfuzz.tests.test.get_suite',

    zip_safe=False,

    # TODO (minor): add classifiers
    classifiers=['Development Status :: 4 - Beta',
               'Operating System :: OS Independent',
               'Programming Language :: Python',]
    )
