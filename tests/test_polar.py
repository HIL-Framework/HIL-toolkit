import pytest
from unittest.mock import Mock, patch, AsyncMock
from HIL.cost_acquisition.polar.polar import Polar
import asyncio

@pytest.fixture
def polar():
    return Polar()

def test_polar_initialization(polar):
    assert polar.ADDRESS == "E1:26:4D:8F:18:3B"
    assert polar.ECG_FLAG == True
    assert polar.ACC_FLAG == True
    assert polar.PUBLISH_DASHBOARD == True

@pytest.mark.parametrize("address,ecg,acc", [
    ("00:11:22:33:44:55", False, True),
    ("AA:BB:CC:DD:EE:FF", True, False),
])
def test_polar_custom_initialization(address, ecg, acc):
    polar = Polar(address=address, ECG=ecg, ACC=acc)
    assert polar.ADDRESS == address
    assert polar.ECG_FLAG == ecg
    assert polar.ACC_FLAG == acc

def test_setup(polar):
    polar._setup()
    assert polar.MODEL_NBR_UUID == "00002a24-0000-1000-8000-00805f9b34fb"
    assert "ECG" in polar.WRITE_DATA
    assert "ACC" in polar.WRITE_DATA
    assert polar.SAMPLING_FREQ["ECG"] == 130
    assert polar.SAMPLING_FREQ["ACC"] == 200

@pytest.mark.asyncio
@patch('HIL.cost_acquisition.polar.polar.BleakClient')
async def test_main(mock_bleak_client, polar):
    # Create a mock client
    mock_client = AsyncMock()
    mock_client.is_connected.return_value = True
    mock_client.read_gatt_char.return_value = b'Test'
    mock_client.write_gatt_char = AsyncMock()
    mock_client.start_notify = AsyncMock()

    # Make BleakClient return our mock client when used as a context manager
    mock_bleak_client.return_value.__aenter__.return_value = mock_client

    # Create a task for the main method
    main_task = asyncio.create_task(polar.main())
    
    # Allow the main method to run for a short time
    await asyncio.sleep(0.1)
    
    # Cancel the main task
    main_task.cancel()
    
    try:
        await main_task
    except asyncio.CancelledError:
        pass

    # Assert that BleakClient was called (i.e., instantiated)
    assert mock_bleak_client.called
    # Assert that the context manager was entered
    assert mock_bleak_client.return_value.__aenter__.called
    # Assert that methods on the client were called
    assert mock_client.is_connected.called
    assert mock_client.read_gatt_char.called
    assert mock_client.write_gatt_char.called
    assert mock_client.start_notify.called



@pytest.mark.parametrize("client_exists", [True, False])
@patch('HIL.cost_acquisition.polar.polar.sys.exit')
def test_interrupt_handler(mock_exit, client_exists, polar):
    # Mock the logger to prevent actual logging during the test
    polar.logger = Mock()

    if client_exists:
        polar.client = Mock()
    else:
        polar.client = None

    # Call the interrupt handler
    polar._interrupt_handler(None, None)

    if client_exists:
        polar.client.disconnect.assert_called_once() #type: ignore
    else:
        assert not hasattr(polar.client, 'disconnect')

    mock_exit.assert_called_once()

    # Assert that the correct log message was produced
    if client_exists:
        polar.logger.info.assert_called_with('found ble client stopping')
    else:
        polar.logger.info.assert_called_with('no ble client found closing the device')

@patch('HIL.cost_acquisition.polar.polar.convert_to_unsigned_long')
@patch('HIL.cost_acquisition.polar.polar.convert_array_to_signed_int')
@patch('HIL.cost_acquisition.polar.polar.ECG_stream')
def test_send_data_ecg(mock_convert_signed, mock_convert_unsigned, mock_ecg_stream, polar):
    mock_convert_unsigned.return_value = 1000
    mock_convert_signed.return_value = 100
    
    ecg_data = bytearray([0x00] + [0]*9 + [1,2,3])
    polar._send_data(None, ecg_data)
    
    assert len(polar.ECG_data['ecg']) > 0
    assert len(polar.ECG_data['time']) > 0

@patch('HIL.cost_acquisition.polar.polar.convert_to_unsigned_long')
@patch('HIL.cost_acquisition.polar.polar.convert_array_to_signed_int')
def test_send_data_acc(mock_convert_signed, mock_convert_unsigned, polar):
    mock_convert_unsigned.return_value = 1000
    mock_convert_signed.return_value = 100
    
    acc_data = bytearray([0x02] + [0]*9 + [1,2,3])
    polar._send_data(None, acc_data)

    print(polar.ACC_data['acc'])
    assert len(polar.ACC_data['acc']) > 0
    assert len(polar.ACC_data['time']) > 0
