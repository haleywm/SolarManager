# SolarManager

This is a project to assist in some minor tweaks that I would like to make to my Growatt SPH Inverter + Battery.

Currently the project is capable of regularly connecting to the API, checking the current battery charge level, and if it is below the required level, enabling the "Charge battery from grid" setting to run between the given times, and then disabling it again once the battery is charged. This is required, because otherwise, if the charge limit is set to less than 100%, the battery will then stop charging from the panels and excess solar power will simply flow to the grid.

## Usage

Download a copy of this repository. You'll need to either generate a docker container using the provided Containerfile, or you can install the latest version of [Python](https://www.python.org/) (Code built and tested using Python 3.13.9), and install the requirements with `pip install -U -r requirements.txt`.

Before building or running the code, first make a copy of `example_config.toml` at `config.toml` and fill in your account details and API key, and then adjust any other variables in the config to your liking.

You can now run the program with `python main.py`. If you would like to specify a different config file location than `config.toml`, you can instead use `python main.py path/to/config.toml`. Have fun!
