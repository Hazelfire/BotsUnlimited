"""
File: test_cli.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Integration tests for the discord cli
"""

import os
from tempfile import TemporaryDirectory
from click.testing import CliRunner

from discordmvc.cli import cli


def check_result(result):
    """Check whether a click result is a success

    :result: click result

    """
    assert result.exit_code == 0
    assert result.exception is None


def test_create_project():
    """Tests the create command"""
    with TemporaryDirectory() as tempname:
        runner = CliRunner()
        result = runner.invoke(cli, ["create", "test", "-d", tempname])
        check_result(result)
        assert os.path.exists(os.path.join(tempname, "test"))


def test_invalid_command():
    """Tests whether an invalid command will throw an error"""
    runner = CliRunner()
    result = runner.invoke(cli, ["invalid"])
    assert result.exit_code == 2
