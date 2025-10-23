# SolarManager

This is a project to assist in some minor tweaks that I would like to make to my Growatt SPH Inverter + Battery.

Currently the project is capable of regularly connecting to the API, checking the current battery charge level, and if it is below the required level, enabling the "Charge battery from grid" setting to run between the given times, and then disabling it again once the battery is charged. This is required, because otherwise, if the charge limit is set to less than 100%, the battery will then stop charging from the panels and excess solar power will simply flow to the grid.

There are future cleanups and new features planned, see [TODO.md](TODO.md) for further details.
