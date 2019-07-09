from setuptools import setup, find_packages

setup(
    name="BotsUnlimited",
    version="0.1",
    packages=["botsunlimited"],
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest"
    ],
    install_requires=[
        "discordmvc @ git+https://github.com/Hazelfire/discordmvc",
        "discordpy",
        "jinja2",
        "sqlalchemy"
    ],
)
