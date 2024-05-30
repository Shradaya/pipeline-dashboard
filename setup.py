import os
from setuptools import setup, find_packages

env = os.getenv('ENV', 'dev')

requirements_file = f'requirements.{env}.txt'

with open(requirements_file) as f:
    requirements = f.read().splitlines()

setup(
    name='Dash_Postgres_Project',  
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements
)