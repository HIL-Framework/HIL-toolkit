import pytest
from unittest.mock import MagicMock, patch
from HIL.optimization.HIL import HIL

# @pytest.fixture
# def args():
#     return {
#         'Optimization': {
#             'n_parms': 1,
#             'range': [0, 100],
#             'model_save_path': 'test_path/',
#             'n_steps': 10,
#             'n_exploration': 5,
#             'n_start_points': 3,
#             'device': 'cpu',
#             'acquisition': 'qei',
#             'kernel_function': 'SE',
#             'GP': 'Regular',
#             'kernel_parms': {
#                 'n_parms': 1,
#                 'length_scale': [0.0, 1.0],
#                 'variance_constraints': [0.0, 1.0]
#             }
#         },
#         'Cost': {
#             'Name': 'Met_cost',
#             'n_samples': 5,
#             'time': 10,
#             'avg_time': 14,
#             'mean_time': 5
#         }
#     }

# @pytest.fixture
# def mock_resolve_streams(args):
#     with patch('pylsl.resolve_streams', autospec=True) as mock_resolve_streams:
#         dummy_stream = MagicMock()
#         dummy_stream.name.return_value = args['Cost']['Name']
#         mock_resolve_streams.return_value = [dummy_stream]
#         yield mock_resolve_streams

# @pytest.fixture
# def mock_stream_inlet(args):
#     with patch('pylsl.StreamInlet', autospec=True) as mock_stream_inlet:
#         mock_inlet = MagicMock()
#         mock_stream_inlet.return_value = mock_inlet
#         yield mock_inlet

# @pytest.fixture
# def mock_stream_outlet(args):
#     with patch('pylsl.StreamOutlet', autospec=True) as mock_stream_outlet:
#         mock_outlet = MagicMock()
#         mock_stream_outlet.return_value = mock_outlet
#         yield mock_outlet

def test_HIL_initialization(args):
    with pytest.raises(Exception) as e:
        hil = HIL(args)
    assert str(e.value) == "Cost function not found"

def test_HIL_stream_mocking(mock_stream_inlet, mock_resolve_streams, args):
    hil = HIL(args)
    assert hil.n == 0

def test_outlet_cost(mock_stream_inlet, mock_resolve_streams, mock_stream_outlet, args):
    hil = HIL(args)
    assert hasattr(hil, 'outlet')

def test_reset_data_collection(mock_stream_inlet, mock_resolve_streams, mock_stream_outlet, args):
    hil = HIL(args)
    assert hil.store_cost_data == []
    assert hil.cost_time == 0
    assert hil.start_time == 0

def test_start_optimization(mock_stream_inlet, mock_resolve_streams, mock_stream_outlet, args):
    hil = HIL(args)
    assert hil.BO.n_parms == args['Optimization']['n_parms']
    assert hil.BO.kernel.n_parms == args['Optimization']['n_parms']
    assert hasattr(hil.BO.kernel, 'covar_module')
    assert hasattr(hil.BO.kernel, 'length_scale_constraints')
    assert hasattr(hil.BO.kernel, 'output_constraints')
    assert hil.BO.kernel.kernel_name == args['Optimization']['kernel_function']

def test_change_kernel(mock_stream_inlet, mock_resolve_streams, mock_stream_outlet, args):
    args['Optimization']['kernel_function'] = 'Matern'
    hil = HIL(args)
    assert hil.BO.kernel.n_parms == args['Optimization']['n_parms']
    assert hasattr(hil.BO.kernel, 'covar_module')
    assert hasattr(hil.BO.kernel, 'length_scale_constraints')
    assert hil.BO.kernel.kernel_name == 'Matern'



def test_empty_kernel_parms(mock_stream_inlet, mock_resolve_streams, mock_stream_outlet, args):
    args['Optimization']['kernel_function'] = 'Matern'
    args['Optimization']['kernel_parms'] = {}
    hil = HIL(args)
    assert hil.BO.kernel.n_parms == args['Optimization']['n_parms']
    assert hasattr(hil.BO.kernel, 'covar_module')
    assert hasattr(hil.BO.kernel, 'length_scale_constraints')
    assert hil.BO.kernel.kernel_name == 'Matern'


    args['Optimization']['kernel_function'] = 'SE'
    args['Optimization']['kernel_parms'] = {}
    hil = HIL(args)
    assert hil.BO.kernel.n_parms == args['Optimization']['n_parms']
    assert hasattr(hil.BO.kernel, 'covar_module')
    assert hasattr(hil.BO.kernel, 'length_scale_constraints')
    assert hil.BO.kernel.kernel_name == 'SE'


def test_no_model_save_path(mock_stream_inlet, mock_resolve_streams, mock_stream_outlet, args):
    args['Optimization']['model_save_path'] = ""
    hil = HIL(args)
    assert hil.BO.model_save_path == "tmp_data/"

# def test_reset_data_collection(args):
#     hil = HIL(args)
#     hil.store_cost_data = [1, 2, 3]
#     hil.cost_time = 100
#     hil.start_time = 50

#     hil._reset_data_collection()

#     assert hil.store_cost_data == []
#     assert hil.cost_time == 0
#     assert hil.start_time == 0

# @patch('HIL.optimization.HIL.BayesianOptimization')
# def test_start_optimization(mock_BO, args):
#     hil = HIL(args)
#     mock_BO.return_value = MagicMock()
    
#     hil._start_optimization(args['Optimization'])
    
#     mock_BO.assert_called_once_with(
#         n_parms=3,
#         range=MagicMock(),
#         model_save_path='path/to/model'
#     )
#     assert hasattr(hil, 'BO')

# def test_generate_initial_parameters(args):
#     hil = HIL(args)
#     hil._generate_initial_parameters()
    
#     assert len(hil.x) == args['Optimization']['n_start_points']
#     assert hil.x[0] == 35.0
#     assert hil.x[1] == 75.0
#     assert hil.x[2] == 10.0