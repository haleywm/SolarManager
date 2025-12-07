# SolarManager

This is a project to assist in some minor tweaks that I would like to make to my Growatt SPH Inverter + Battery.

Currently the project is capable of regularly connecting to the API, checking the current battery charge level, and if it is below the required level, enabling the "Charge battery from grid" setting to run between the given times, and then disabling it again once the battery is charged. This is helpful, because otherwise, if the charge limit is set to less than 100%, the battery will then stop charging from the panels and excess solar power will simply flow to the grid.

It also has an option to gather some useful statistics from the API data, and post this to a webhook URL. This can be used to, for example, monitor the state of the solar system through a separate utility such as homeassistant, with this script handling all actual Growatt API calls.

## Usage

Download a copy of this repository. You'll need to either generate a docker container using the provided Containerfile, or you can install the latest version of [Python](https://www.python.org/) (Code built and tested using Python 3.13.9), and install the requirements with `pip install -U -r requirements.txt`.

Before building or running the code, first make a copy of `example_config.toml` at `config.toml` and fill in your account details and API key, and then adjust any other variables in the config to your liking.

If the webhook functionality is required, then be sure to enable it, and provide a valid URL.

You can now run the program with `python main.py`. If you would like to specify a different config file location than `config.toml`, you can instead use `python main.py path/to/config.toml`. Have fun!

Note that this code works by updating the "Battery First" element of the settings. The first time period will be set and enabled/disabled as necessary, while the second two elements will be cleared. If you wish to set additional battery first times not managed by this software, use the "Battery First1" element, which allows you to specify up to 3 additional timeslots.

## Sources

I didn't use any other Growatt interaction libraries in my code, as I found that many of them interacted with outdated endpoints for the SPH. I have based my code mostly on the API documentation at https://www.showdoc.com.cn/262556420217021/1494053950115877. In addition, I found that the `http(s)://test.growatt.com/v1/mixSet` endpoint didn't function, and would just return an empty value without updating the requested value. I ended up working around this by exploring network requests sent by the browser when manually updating the settings, and found that this worked almost identically to the API, however it requires username+password authentication rather than the API key used by the official API, which is why my script requires both an API key and also a username+password combination.
