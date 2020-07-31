import setuptools
import subprocess
import os


with open("README.md", "r") as fh:
    long_description = fh.read()

if not os.path.exists('sps/version.py'):
  vers = subprocess.check_output(['git','describe','--tags','--abbrev=0','--always']).decode('utf-8').strip()
  print(vers)
  with open('sps/version.py', 'a') as the_file:
          the_file.write('__version__ = "{}"\n'.format(vers))

setuptools.setup(
  name = 'sps',
  version = "1.0",
  author="Daniele Michilli",
  author_email="danielemichilli@gmail.com",
  description="Classifier for single-pulse searches in the fast radio timing field of Astronomy",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/danielemichilli/SpS",
  packages=setuptools.find_packages(),
  classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ),
  python_requires='>=3.6',
  install_requires=[
        'cython>=0.28.3',
        'matplotlib>=2.2.2',
        'numpy>=1.14.3',
        'pandas>=0.23.0',
        'scipy>=0.19.1',
        'astropy>=2.0.2',
        'tables',
      ],
  scripts=['single_pulse_searcher.py']
)
