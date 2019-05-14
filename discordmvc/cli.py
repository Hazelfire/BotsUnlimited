"""
File: cli.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Main cli for discordmvc
"""

import click
from discordmvc.projects import create_project


@click.group()
def cli():
    """Main cli group"""
    pass


@cli.command()
@click.argument("name")
@click.option("-d", "--directory")
def create(name, directory):
    """Creates a discordmvc project

    :name: the name of the project
    :directory: Optional directory for the project

    """
    create_project(name, directory)
