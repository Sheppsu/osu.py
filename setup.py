import setuptools

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

readme = ''
with open('README.rst') as f:
    readme = f.read()

setuptools.setup(install_requires=requirements,
                 long_description=readme,
                 long_description_content_type="text/x-rst")
