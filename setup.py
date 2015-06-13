from __future__ import absolute_import
from setuptools import setup, find_packages

setup(name='elb-log',
      version='0.1.0',
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'elb-logs=elb_logs.cli:main',
          ],
      },
      install_requires=[
          'jmespath',
          'python-dateutil',
          'click',
          'boto3'
      ],
      packages=find_packages(exclude=['tests*']),)
