"""Find laboratory sensors with overdue calibration."""

import json
from pathlib import Path

import pandas as pd
import yaml


def main() -> None:
    """Read, join, filter and export sensor data."""
    script_folder = Path(__file__).resolve().parent

    config_path = script_folder / "config.yml"
    sensors_path = script_folder / "sensors.xlsx"
    calibrations_path = script_folder / "calibrations.csv"

    with config_path.open(
        mode="r",
        encoding="utf-8",
    ) as config_file:
        config = yaml.safe_load(config_file)

    max_days = int(config["max_days_since_calibration"])
    output_path = script_folder / config["output_file"]

    sensors = pd.read_excel(sensors_path)
    calibrations = pd.read_csv(calibrations_path)

    merged_data = pd.merge(
        sensors,
        calibrations,
        on="sensor_id",
    )

    overdue_sensors = []

    for _, row in merged_data.iterrows():
        days = int(row["days_since_calibration"])

        if days > max_days:
            sensor_item = {
                "sensor_id": str(row["sensor_id"]),
                "lab_room": str(row["lab_room"]),
                "owner": str(row["owner"]),
                "days_since_calibration": days,
            }
            overdue_sensors.append(sensor_item)

    with output_path.open(
        mode="w",
        encoding="utf-8",
    ) as json_file:
        json.dump(
            overdue_sensors,
            json_file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Found overdue sensors: {len(overdue_sensors)}")
    print(f"Output saved to: {output_path.name}")


if __name__ == "__main__":
    main()