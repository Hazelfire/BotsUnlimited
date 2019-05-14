import click
from click.testing import CliRunner


def test_click_passes_arguments():
    """Testing how click passes arguments"""

    @click.command()
    @click.argument("argument")
    @click.option("-o", "--option")
    def main(argument, option):
        assert argument == "arg1"
        assert option == "opt1"

    runner = CliRunner()

    result = runner.invoke(main, ["arg1", "-o", "opt1"])
    assert result.exception is None
    assert result.exit_code == 0
