import setuptools

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setuptools.setup(install_requires=requirements,
                 long_description_content_type="text/x-rst")
