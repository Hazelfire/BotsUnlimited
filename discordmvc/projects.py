"""
File: projects.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Project commands
"""

import os
import pkg_resources


def create_project(name, directory):
    """Creates a project with a given name

    :name: name of the project

    """
    full_path = os.path.join(directory, name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        relpath = "templates/__main__.py"
        filepath = pkg_resources.resource_filename(__name__, relpath)
