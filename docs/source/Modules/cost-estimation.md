# Cost Estimation

This module is for estimating cost functions for the Hardware-in-the-Loop (HIL) optimization.

There are currently two cost functions:

## ECG

ECG estimation is implemented using the `RMSSDFromStream` class. Which uses the Config file `configs/RMSSD.yml` to get the information about the stream. 

Here is an example of the Config file with explanations for each value:

```yaml
RMSSD_config:
  Stream_name: "polar ECG"  # Name of the input ECG data stream
  Skip_threshold: 40  # Upper threshold for RMSSD; values above this are not sent (usually set to standing threshold)
  Data_buffer_length: 1000  # Number of data points to process for RMSSD calculation (~9s at 133 Hz sampling rate)
  Sampling_rate: 133  # Sampling rate of the ECG signal in Hz
  Pubrate: 1  # Publication rate for RMSSD values (in seconds)
  Output_stream_name: 'RMSSD'  # Name of the output stream for processed RMSSD data
```

Explanations:
- `Stream_name`: Specifies the name of the input ECG data stream to be processed.
- `Skip_threshold`: Sets an upper limit for RMSSD values. If the calculated RMSSD exceeds this threshold, it is not sent. This is typically set to a standing threshold to filter out potentially erroneous or extreme values.
- `Data_buffer_length`: Determines the number of data points used to calculate RMSSD. With a sampling rate of 133 Hz, 1000 points represent approximately 9 seconds of data.
- `Sampling_rate`: Defines the number of ECG samples collected per second (in Hz).
- `Pubrate`: Specifies how often (in seconds) the RMSSD values are published or updated.
- `Output_stream_name`: Names the output stream that will contain the processed RMSSD data.

These configuration parameters allow for flexible adjustment of the RMSSD calculation process to suit different ECG data sources and processing requirements.
