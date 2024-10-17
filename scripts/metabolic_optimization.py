"""This code script is for optimization of the metabolic cost estimation and optimization using the HIL toolbox.
"""

import yaml 

# HIL toolbox import

from HIL.optimization.HIL.HIL_CLI import HIL_CLI


def run():
    
        args = yaml.safe_load(open('configs/Met_config.yml','r'))
        hil = HIL_CLI(args)
        hil.start()


if __name__ == "__main__":
    run()