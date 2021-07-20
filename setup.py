import setuptools

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setuptools.setup(install_requires=requirements)
