from setuptools import setup, find_packages
from io import open

version = '0.0.0.dev0'

with open("README.md", 'rt', encoding='UTF-8') as file:
    long_description = file.read() + '\n\n'

with open("CHANGES.txt", 'rt', encoding='UTF-8') as file:
    long_description += file.read()


setup(name='ogretests',
      version=version,
      description="A framework for loading test environments into databases",
      long_description=long_description,
      classifiers=[
          'Development Status :: 1 - Planning',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Testing',
          ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='testing layers setup',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='https://github.com/regebro/ogretests',
      license="MIT",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'PyYAML',
      ],
      tests_require=[
          'mock',
      ],
      test_suite='tests',
      )
