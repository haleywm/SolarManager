# Defines the solarmanager class which will help manage things
import re
import requests
import time
from typing import Optional
import hashlib


class SolarManager:
    url_prefix = "https://openapi-au.growatt.com/"

    def __init__(
        self,
        api_key: str,
        username: str,
        password: str,
        target_percent: int,
        start_time: str,
        stop_time: str,
        update_frequency: int,
        max_delay_time: int,
        verbose: bool,
    ) -> None:
        self.api_key = api_key
        self.username = username
        self.password = password
        self.target_percent = target_percent
        self.start_hour, self.start_minute = self._parse_time(start_time)
        self.stop_hour, self.stop_minute = self._parse_time(stop_time)
        self.update_frequency = update_frequency
        self.max_delay_time = max_delay_time
        self.verbose = verbose

        # Creating a session to use for API requests
        self.session = requests.Session()
        self.session.headers.update({"token": self.api_key})

        self.mix_sn = self.get_mix_sn()

        self.battery_rule_enabled = self.get_grid_charging_enabled()

    def get_mix_sn(self) -> str:
        # In order to do anything, we first need to get the users devices serial number
        # Step 1: List all user power plants. There will typically only be one
        res = self.session.get(self.url_prefix + "v1/plant/list")
        if self.verbose:
            print(res.text)
        time.sleep(10)
        plants = res.json()["data"]["plants"]
        if len(plants) == 0:
            raise SolarError("Unable to find any power plants associated with account")
        elif len(plants) > 1:
            print("Warning: Multiple plants associated with account. Using first one.")

        plant_id = plants[0]["plant_id"]
        print(f"Retrieved plant id {plant_id}")

        res = self.session.get(
            self.url_prefix + "v1/device/list", params={"plant_id": plant_id}
        )
        if self.verbose:
            print(res.text)
        time.sleep(10)

        devices = res.json()["data"]["devices"]

        mix_sn: Optional[str] = None
        for device in devices:
            if device["type"] == 5:
                # Found the correct value
                mix_sn = device["device_sn"]
                assert isinstance(mix_sn, str)

        if mix_sn is None:
            raise SolarError(
                "Unable to find any devices of type 5 associated with plant"
            )

        assert isinstance(mix_sn, str), "Unexpected type returned from JSON"
        print(f"Retrieved device serial number {mix_sn}")

        return mix_sn

    def enable_grid_charging(self) -> None:
        self._adjust_grid_charging(1)

    def disable_grid_charging(self) -> None:
        self._adjust_grid_charging(0)

    def get_grid_charging_enabled(self) -> bool:
        # First, ensure that the right cookies are present
        self.server_login()

        res = self.session.get(
            self.url_prefix + "v1/device/mix/mix_data_info",
            params={"device_sn": self.mix_sn},
        )
        if self.verbose:
            print(res.text)
        time.sleep(10)
        stop_switch_status = res.json()["data"]["forcedChargeStopSwitch1"]
        assert isinstance(stop_switch_status, int)

        return stop_switch_status == 1

    def get_current_charge(self) -> int:
        res = self.session.post(
            self.url_prefix + "v1/device/mix/mix_last_data",
            data={"mix_sn": self.mix_sn},
        )
        if self.verbose:
            print(res.text)
        time.sleep(10)
        charge = res.json()["data"]["soc"]
        assert isinstance(charge, int), "Unexpected type returned from JSON"

        # TODO: Check if data is reasonably up to date

        return charge

    """ def currently_active_period(self) -> bool:
        # Check if the current period is the active period
        # Note that this is based on the local time zone
        current_time = datetime.now()

        if self.start_hour <= self.stop_hour:
            # Start and stop are on the same day

            # Generate start and end times by replacing just the hours and smaller values
            # That way days and months etc don't get in the way
            start_time = current_time.replace(hour=self.start_hour, minute=self.start_minute, second=0, microsecond=0)
            stop_time = start_time.replace(hour=self.stop_hour, minute=self.stop_minute)
            # Only return true if current time is bigger than the start time and smaller than the end time
            return current_time > start_time and current_time < stop_time
        else:
            # Start and stop are on different days
            # Don't need this and I'm sleepy rn
            raise NotImplementedError("Active periods across different days not yet supported") """

    def run_event_loop(self) -> None:
        print(
            f"Starting check cycle, will check battery status every {self.update_frequency} seconds"
        )
        while True:
            current_battery = self.get_current_charge()

            enough_battery = current_battery >= self.target_percent

            if self.verbose:
                print(
                    f"Battery currently at {current_battery}%, target: {self.target_percent}%"
                )

            if enough_battery and self.battery_rule_enabled:
                # It's time to turn off grid charging for the battery
                print(
                    "Battery has sufficient charge, disabling grid charging (during specified times)"
                )
                self.disable_grid_charging()
                self.battery_rule_enabled = False
                print("Grid charging disabled!")

            elif not enough_battery and not self.battery_rule_enabled:
                # The battery level is too low, enable the charging rule
                print(
                    "Battery has insufficient charge, enabling grid charging (during specified times)"
                )
                self.enable_grid_charging()
                self.battery_rule_enabled = True
                print("Grid charging enabled!")

            time.sleep(float(self.update_frequency))

    def server_login(self) -> None:
        # Attempts to log in to the server to generate a login session
        res = self.session.post(
            self.url_prefix + "login",
            data={
                "account": self.username,
                "password": "",
                "validateCode": "",
                "isReadPact": 0,
                "passwordCrc": self.hash_password(self.password),
            },
        )
        if self.verbose:
            print(res.text)
        time.sleep(10)

    def hash_password(self, password: str) -> str:
        hasher = hashlib.md5()
        hasher.update(password.encode())
        result = hasher.hexdigest()

        # Note: If any errors occur, another library suggests that
        # I have to add 'c' if any 10s digit is 0
        # see https://github.com/indykoning/PyPi_GrowattServer/blob/master/growattServer/base_api.py#L15
        # Not currently an issue

        return result

    def _parse_time(self, time: str) -> tuple[str, str]:
        values = re.match(r"^(\d\d):(\d\d)$", time)
        assert (
            values is not None
        ), f"Invalid time string {time}, should be in format DD:DD"

        return (values.group(1), values.group(2))

    def _adjust_grid_charging(self, active: int) -> None:
        res = self.session.post(
            self.url_prefix + "tcpSet.do",
            data={
                "action": "mixSet",
                "serialNum": self.mix_sn,
                "type": "mix_ac_charge_time_period",  # This means we're changing the time period on the inverter to force ac draw
                "param1": 100,  # Charge at full capacity
                "param2": self.target_percent,  # Cutoff charging at the target percent
                "param3": 1,  # Enable drawing from mains
                "param4": f"{self.start_hour}",  # Hour to start period
                "param5": f"{self.start_minute}",  # Minute to start period
                "param6": f"{self.stop_hour}",
                "param7": f"{self.stop_minute}",
                "param8": active,  # If this period should be active. Use the argument
                "param9": 0,
                "param10": 0,
                "param11": 0,
                "param12": 0,
                "param13": 0,
                "param14": 0,
                "param15": 0,
                "param16": 0,
                "param17": 0,
                "param18": 0,
            },
        )
        if self.verbose:
            print(res.text)
        time.sleep(10)

        data = res.json()
        if data["error_code"] != 0:
            raise SolarError(
                f"Error {data["error_code"]} returned by API: {data["error_msg"]}"
            )


class SolarError(Exception):
    pass


class DisconnectedError(SolarError):
    pass
