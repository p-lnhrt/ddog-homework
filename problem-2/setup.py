import setuptools

import ddog

setuptools.setup(
    name='ddog',
    version=ddog.__version__,
    author='Pierre LIENHART',
    author_email='pierre.lienhart@gmail.com',
    description='Datadog data science homework - Problem 2',
    packages=setuptools.find_packages(exclude=['*.tests'])
)