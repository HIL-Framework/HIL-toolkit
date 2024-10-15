## CLI mode for optimization

Here is an overview of the 4 components of the CLI operation.

![](images/components.png)

1. `Cost acquisition`: Start the polar sensor streaming using the following command 
 
Please be mindful the if you are using the polar sensor for the first time or if your bluetooth configuration is not working, please use the `search_polar.py` script to find your polar sensor address and update the `configs/polar.yml` file.

```python
python collect_polar.py --config configs/polar.yml
```

2. `Cost estimation`: Here you are starting the cost estimation to convert the raw ECG data into a cost value. Here I am using the RMSSD as the cost function.

```python
python send_rmssd.py --config configs/RMSSD.yml
```

3. `Optimization`: Run the ECG optimization:

```python
python ECG_optimization.py  --config configs/ECG_config.yml
```