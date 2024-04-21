import setuptools
import re


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

readme = ''
with open('README.rst') as f:
    readme = f.read()

version = ''
with open('osu/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    
readme = ''
with open('README.rst') as f:
    readme = f.read()

project_urls = {
    "Bug Tracker": "https://github.com/Sheepposu/osu.py/issues",
    "osu.py documentation": "https://osupy.readthedocs.io/",
    "osu!api v2 documentation": "https://osu.ppy.sh/docs/index.html",
    "Code examples": "https://github.com/Sheepposu/osu.py/tree/main/examples"
}
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Intended Audience :: Developers"
]

extra_require = {
    "replay": ["osrparse>=6.0.1,<7"],
    "notifications": ["websockets>=11,<12"],
    "tests": [
        "pytest",
        "pytest-asyncio"
    ]
}

packages = [
    'osu',
    'osu.asyncio',
    'osu.objects',
]

setuptools.setup(
    name="osu.py",
    version=version,
    packages=packages,
    author="Sheepposu",
    description="API Wrapper for osu!api v2 written in Python.",
    long_description=readme,
    install_requires=requirements,
    extras_require=extra_require,
    project_urls=project_urls,
    classifiers=classifiers,
    python_requires=">=3.8.0",
    license="MIT",
    url="https://github.com/Sheepposu/osu.py",
)
