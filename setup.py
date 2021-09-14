import setuptools
import re

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

readme = ''
with open('README.rst') as f:
    readme = f.read()

version = ''
with open('src/osu/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

project_urls = {
    "Bug Tracker": "https://github.com/Sheepposu/osu.py/issues",
    "osu.py documentation": "https://osupy.readthedocs.io/en/latest/",
    "osu!api v2 documentation": "https://osu.ppy.sh/docs/index.html",
    "Code examples": "https://github.com/Sheepposu/osu.py/tree/main/examples"
}
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

packages = [
    'src/osu'
]

setuptools.setup(
    name="osu.py",
    version=version,
    packages=packages,
    author="Sheepposu",
    description="API Wrapper for osu!api v2 written in Python.",
    long_description="See the readme on github :)",
    long_description_content_type="text/plain",
    install_requires=requirements,
    project_urls=project_urls,
    classifiers=classifiers,
    python_requires=">=3.8.0",
    license="MIT",
    url="https://github.com/Sheepposu/osu.py",
)
