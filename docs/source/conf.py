# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

path = os.path.join(Path(os.path.abspath('.')).parent.parent)
sys.path.insert(0, path)


# -- Project information -----------------------------------------------------

project = 'osu.py'
copyright = '2024, Sheppsu'
author = 'Sheppsu'

# The full version, including alpha/beta/rc tags
release = version = '3.2.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    "sphinx.ext.intersphinx"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

language = 'en'

intersphinx_mapping = {
    'py': ('https://docs.python.org/3', None),
}

add_module_names = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

master_doc = 'index'

autodoc_default_options = {
    "imported-members": True
}

from sphinx.application import Sphinx
from typing import List
import re


TYPE_RE = re.compile(r'(:py)?:class:`([a-zA-Z_][a-zA-Z0-9_.]*)`')


def autodoc_process_docstring(app: Sphinx, what: str, name: str, obj: object, options: dict, lines: List[str]):
    if what != "class":
        return

    # Reformat attribute docs
    is_attribute = False
    i = 0
    while i < len(lines):
        if lines[i].startswith("**Attributes**"):
            lines[i] = ""
            is_attribute = True
            i += 1

        if is_attribute and len(lines[i]) != 0 and not lines[i].startswith("    "):
            attr = lines[i].split()
            attr_name, attr_type = (attr[0], " ".join(attr[1:])) if len(attr) > 1 else (attr[0], None)

            lines[i] = f".. py:attribute:: {attr_name[:-1]}"

            if attr_type is not None:
                # account for types that take up multiple lines
                while i + 1 < len(lines) and len(lines[i + 1]) > 0 and not lines[i + 1].startswith("    "):
                    attr_type += lines.pop(i + 1)

                attr_type = re.sub(TYPE_RE, r"\2", attr_type)
                lines.insert(i + 1, f"    :type: {attr_type}")
                i += 1

            lines.insert(i + 1, "")
            i += 1

        i += 1


def setup(app):
    app.connect("autodoc-process-docstring", autodoc_process_docstring)
