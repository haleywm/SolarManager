# Development Notes

The Growatt server library isn't great, only endpoints actively used by the developer are updated, the endpoints used for getting proper data from my inverter (the Growatt SPH, frequently referred to as the API as the mix). I think it'll be easier to just run my own requests through the requests library and call it a day.

https://www.showdoc.com.cn/262556420217021/6129764434976910 is a valuable resource which documents the modern API calls in English. Interface Display > Equipment Related > SPH is where most of the useful stuff is. For almost all of these requests, the 'token' header must be set to your API key.

Endpoints that I'll need:

- `/v1/device/mix/mix_last_data`: This will get me most of the useful data that I'll need to monitor.
    - It contains the key `"soc"`, which states the current battery charge in percent.
    - `"ppv"` contains the power being produced by the panels, presumably in milliwatts?
    - `"pdischarge1"` and `"pcharge1"` contain the current power going in or out of the battery (one will be 0, the other will have the value in milliwatts).
    - `"pacToUserR"` and `"pacToGridR"` appear to document the power coming in or out from the grid, untested though. I assume they work the same as the battery values, though.
    - It also contains the keys `"lost"` and `"calendar"`, which can be used to determine if the device is currently communicating, and acknowledging if this is not the case. There's also a bunch of error values that could be looked at for further error detection. 
        - NOTE: Initial testing suggests that lost is always true even when it's working.
        - Instead, lets use the calendar values. These tend to fall within the last few minutes.
- `/v1/device/mix/mix_data_info`: This will let me check the current settings for the battery.
    - `"wchargeSOCLowLimit2"` appears to store the maximum battery percentage when in "Battery First" mode.
    - I assume that `"forcedChargeTimeStart1"` and `"forcedChargeTimeStop1"` would hold the first configured time period, but the API also likes to report this value as 0 most of the time. `"forcedChargeStopSwitch1"` will be 1 if the time period is enabled, or 0 if disabled. There are another 5 of these values for additional periods, I would prefer to not touch them.
- `/v1/mixSet`: This will let me update the settings on the device.
    - It's best that I just read the documentation for this parameter. Passing a `type` of "mix_ac_charge_time_period" will allow me to overwrite all of the "Battery First" settings at one. I will then need to provide 18 parameters.
    - Interestingly the given type here only overwrites the first 3 times, and there's no documented type for overwriting the second 3 values. I guess if someone wants to set additional times unused by the code then that can go there.
    - In my code, I'll have to be able to generate two versions of this. One which sets the first time period as on, and goes from the earliest grid draw time to the latest, and the remaining time periods off. Then, a second one with all time periods off. They can share the settings for the earlier values about what to do in battery first mode.

Example data dumps can be found in the `examples/` folder. There will be .gitignored for now because of the likelihood of PII in them.
