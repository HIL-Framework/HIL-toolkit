import os
import asyncio
import yaml
import argparse

from HIL.cost_acquisition.polar.polar import Polar



def start_polar(address):
    """
    Start the Polar data collection.
    """
    polar_inst=Polar(address)
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(polar_inst.main())


def run():
    """
    Run the Polar data collection with the given configuration.
    """
    parser = argparse.ArgumentParser(description="Polar data collection script")
    parser.add_argument("--config", default="configs/polar.yml", help="Path to the configuration file")
    parser.add_argument("--address", help="Polar device address (overrides config file)")
    args = parser.parse_args()
    with open(args.config, 'r') as file:
        polar_information = yaml.safe_load(file)
    
    device_address = args.address or polar_information['address']
    start_polar(device_address)


if __name__ == "__main__":
    run()
