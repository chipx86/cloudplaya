#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

from cloudplaya import VERSION


PACKAGE_NAME = 'cloudplaya'


setup(name=PACKAGE_NAME,
      version=VERSION,
      license='MIT',
      description='Python module and command line client for '
                  'Amazon Cloud Player',
      entry_points={
          'console_scripts': [
            'cloudplaya = cloudplaya.main:main',
          ],
      },
      packages=find_packages(),
      install_requires=[
          'mechanize>=0.2.5',
          'requests>=0.13.2',
      ],
      maintainer='Christian Hammond',
      maintainer_email='chipx86@chipx86.com',
      url='http://github.com/chipx86/cloudplaya/',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development',
      ]
)
