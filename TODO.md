# TODO

- Add code to detect if a request fails due to the session expiring, and run the login process again.
- Add code to detect if the panel has ceased communication, and start re-sending the instruction every 10 minutes until it is recieved. (This may be difficult to test as this problem only occasionally occurs. I could probably manually cause it by turning the wifi off?)
- Major task: Rather than just using the target of 80%, attempt to use weather forecasts or other reasonable data to guess the amount of charging that would be achieved after 2pm, and only charge the battery up to that point.
