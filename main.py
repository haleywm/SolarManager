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
    )

    args = parser.parse_args()

    with open(args.config, "rb") as f:
        config = tomllib.load(f)

    manager = SolarManager(
        config["account"]["api_key"],
        config["charging"]["target_percent"],
        config["charging"]["start_time"],
        config["charging"]["end_time"],
        config["timing"]["update_frequency"],
        config["timing"]["max_delay_time"],
    )

    manager.run_event_loop()


def debug() -> SolarManager:
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    manager = SolarManager(
        config["account"]["api_key"],
        config["charging"]["target_percent"],
        config["charging"]["start_time"],
        config["charging"]["end_time"],
        config["timing"]["update_frequency"],
        config["timing"]["max_delay_time"],
    )

    return manager


if __name__ == "__main__":
    main()
