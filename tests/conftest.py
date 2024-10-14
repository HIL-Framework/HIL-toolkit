import pytest
from unittest.mock import MagicMock, patch
from HIL.optimization.HIL import HIL

@pytest.fixture
def args():
    return {
        'Optimization': {
            'n_parms': 1,
            'range': [0, 100],
            'model_save_path': 'test_path/',
            'n_steps': 7,
            'n_exploration': 5,
            'n_start_points': 3,
            'device': 'cpu',
            'acquisition': 'qei',
            'kernel_function': 'SE',
            'GP': 'Regular',
            'kernel_parms': {
                'n_parms': 1,
                'length_scale': [0.0, 1.0],
                'variance_constraints': [0.0, 1.0]
            }
        },
        'Cost': {
            'Name': 'Met_cost',
            'n_samples': 5,
            'max_samples_per_cost': 5,
            'time': 10,
            'avg_time': 14,
            'mean_time': 5,
            'time_step': 0.1
        },
        'time_based': False
    }

@pytest.fixture
def mock_resolve_streams(args):
    with patch('pylsl.resolve_streams', autospec=True) as mock_resolve_streams:
        dummy_stream = MagicMock()
        dummy_stream.name.return_value = args['Cost']['Name']
        mock_resolve_streams.return_value = [dummy_stream]
        yield mock_resolve_streams

@pytest.fixture
def mock_stream_inlet(args):
    with patch('pylsl.StreamInlet', autospec=True) as mock_stream_inlet:
        mock_inlet = MagicMock()
        mock_stream_inlet.return_value = mock_inlet
        yield mock_inlet

@pytest.fixture
def mock_stream_outlet(args):
    with patch('pylsl.StreamOutlet', autospec=True) as mock_stream_outlet:
        mock_outlet = MagicMock()
        mock_stream_outlet.return_value = mock_outlet
        yield mock_outlet

@pytest.fixture
def hil_instance(args, mock_resolve_streams, mock_stream_inlet, mock_stream_outlet):
    return HIL(args)