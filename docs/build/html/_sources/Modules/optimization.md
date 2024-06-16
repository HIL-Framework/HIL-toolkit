# Optimization

## Overview

Overview of the optimization is here

![](../images/bo.png)


## Config
The config of the optimization is defined in the yaml file, example as follows.
```yaml
Cost:
  Name: "Met_cost" # name of the cost function stream
  time: 90 # time of the cost function stream.
  avg_time: 14 # average time of the cost function stream.
  mean_time: 5 # mean time of the cost function.

Optimization:
  n_parms: 1 # number of parametes
  n_steps: 15 # number of steps
  n_exploration: 3 # number of exploration steps
  range: [0, 85] # range of the parameters
  model_save_path: "models/"
  device: "cuda" # device to use
  n_start_points: 3 # number of start points
  acquisition: 'ei' # other options are qei, pi, ucb
  kernel_function: 'se' # other options se, linear, fixed noise
  GP: 'Regaular' # other options, fixed noise GP.
```

## Function information
```{eval-rst}
.. automodule:: HIL.optimization.BO
   :members:
   :undoc-members:
   :show-inheritance:
```