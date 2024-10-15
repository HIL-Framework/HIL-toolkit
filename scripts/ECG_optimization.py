import yaml
import argparse
from HIL.optimization.HIL import HIL

def run():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="ECG Optimization Script")
    parser.add_argument('--config', type=str, default='configs/ECG_config.yml',
                        help='Path to the configuration file (default: configs/ECG_config.yml)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Initialize HIL with loaded configuration
    hil = HIL(config)
    hil.start_cli()

if __name__ == "__main__":
    run()
