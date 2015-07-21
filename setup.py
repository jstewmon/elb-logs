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
          'jmespath~=0.7',
          'python-dateutil~=2.4',
          'click~=4.0',
          'boto3~=1.0'
      ],
      packages=find_packages(exclude=['tests*']),)
