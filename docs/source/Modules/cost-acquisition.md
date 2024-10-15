# Cost acquisition
This module is for cost acquisition from physiological sensors

## Polar (ECG)

The Polar sensor is used to acquire ECG (Electrocardiogram) data.

Cost acquisition is done using two steps:

1. Search for the Polar sensor using the `search_polar.py` script. This script will search for available Polar sensors in Bluetooth range and save the BLE information in the `config/polar.yml` file.

```yaml
address: E0:1B:3C:22:13:D8
name: Polar H10 7F302C25
``` 


2. Acquire the cost using the `collect_polar.py` script. This script will connect to the Polar sensor and start acquiring the cost.

This script will read the ECG stream using the BLE connection and publish to the `polar_ecg` topic. More information on the streaming can be found in the `cost_acquisition/polar/polar.py` file.