import tomllib
import argparse
from pathlib import Path
from SolarManager import SolarManager


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config",
        type=Path,
        help="Location of the config file. Default: config.toml",
        default="config.toml",
        nargs="?",
    )

    args = parser.parse_args()

    with open(args.config, "rb") as f:
        config = tomllib.load(f)

    manager = SolarManager(
        api_key=config["account"]["api_key"],
        username=config["account"]["username"],
        password=config["account"]["password"],
        target_percent=config["charging"]["target_percent"],
        start_time=config["charging"]["start_time"],
        stop_time=config["charging"]["end_time"],
        update_frequency=config["timing"]["update_frequency"],
        max_delay_time=config["timing"]["max_delay_time"],
        api_delay_time=config["timing"]["api_delay_time"],
        enable_webhook=config["webhooks"]["enable"],
        webhook_url=config["webhooks"]["url"],
        verbose=config["other"]["verbose"],
    )

    manager.run_event_loop()


def debug() -> SolarManager:
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    manager = SolarManager(
        api_key=config["account"]["api_key"],
        username=config["account"]["username"],
        password=config["account"]["password"],
        target_percent=config["charging"]["target_percent"],
        start_time=config["charging"]["start_time"],
        stop_time=config["charging"]["end_time"],
        update_frequency=config["timing"]["update_frequency"],
        max_delay_time=config["timing"]["max_delay_time"],
        api_delay_time=config["timing"]["api_delay_time"],
        enable_webhook=config["webhooks"]["enable"],
        webhook_url=config["webhooks"]["url"],
        verbose=True,  # Always be verbose when using the debug creation method
    )

    return manager


if __name__ == "__main__":
    main()
