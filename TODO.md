# TODO

- Test what happens if I attempt to update inverter settings while the inverter is currently offline. If this generates an error without updating the setting, the code will need to be adjusted to retry this update every {update_frequency} settings. (I suspect that it will generate an error, which can be easily handled.)
- Major task: Rather than just using the target of 80%, attempt to use weather forecasts or other reasonable data to guess the amount of charging that would be achieved after 2pm, and only charge the battery up to that point.
