# Welcome to the HIL toolbox.

![](images/Toolkit_overview.png)


The main purspose of this is have a all in one toolkit for exoskeleton personalization.

---



Toolkit has following functionalities ( more added over time)
1. Data acquisition functions
2. Cost processing for the following cost functions
    - RMSSD ( ECG based cost function )
    - Metabolic cost
3. Modular Bayesian optimization to minimize or maximize the cost function
4. Exoskeleton communication using UDP

To setup the module please follow the [Install/setup](Setup.md)

## Overview

The toolkit is designed to be a modular infrastructure for the human in the loop optimization of exoskeletons. 

There are two methods of operation:

1. **CLI / Running in the terminal**: 
   Here you will be required to run multiple scripts in the terminal simultaneously to start the data acquisition, cost estimation, and optimization. (require python and pip installed)
   This is done using the `python` command line interface. More information and ECG examples can be found [here](CLI.md). Here you will be required to enter commands such as 'enter' or 'Y' or 'N' when prompted. So Please be mindful of the prompts.

2. **API / DOCKER**: TODO. 
   Here you will be required to start the docker container and send the data to the docker container using an API. ( Any programming language can be used to send the data to the docker container )
   This is an API mode where the data will be streamed into the optimization pipeline hosted in a docker container, the data will be sent using the `FastAPI` framework and the input/output will be `json` with `pydantic` verififcation.