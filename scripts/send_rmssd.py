from HIL.cost_processing.ECG.RMSSD import RMSSDFromStream
import yaml
import logging
import argparse


logging.basicConfig(level=logging.DEBUG)

logger_blocklist = [
    "fiona",
    "rasterio",
    "matplotlib",
    "PIL",
]

for module in logger_blocklist:
    logging.getLogger(module).setLevel(logging.WARNING)

def main():
    parser = argparse.ArgumentParser(description="Polar data collection script")
    parser.add_argument("--config", default="configs/RMSSD.yml", help="Path to the configuration file")
    args = parser.parse_args()
    with open(args.config, 'r') as config_file:
        rmssd_config = yaml.safe_load(config_file)
    rmssd = RMSSDFromStream(config=rmssd_config)
    rmssd.run()

if __name__ == "__main__":
    main()
