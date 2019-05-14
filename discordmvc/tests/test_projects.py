"""
File: test_projects.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Tests the project commands
"""

import os
from tempfile import TemporaryDirectory
from discordmvc.projects import create_project


def test_create():
    """Tests if the create function works successfully"""
    with TemporaryDirectory() as tempdir:
        create_project("test", tempdir)

        assert os.path.exists(os.path.join(tempdir, "test"))
