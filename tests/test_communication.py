import pytest
import time
from HIL.Exo_communication.udp_communication import UDPSend, UDPReceive

@pytest.fixture
def UDP_configs():
    return {
        'target_ip': 'localhost',
        'prediction_port': 50005,
        'stopping_port': 50007
    }

def test_initialization(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    assert udp_send._prediction.port == UDP_configs['prediction_port']
    assert udp_send._stoping.port == UDP_configs['stopping_port']
    assert udp_send.target_ip == UDP_configs['target_ip']
    udp_send.close()

def test_udp_send_all(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['prediction_port'])
    udp_send.send_all(2.0, True)
    received = udp_receive.receive_pred()
    print(received)
    assert received == 2.0
    udp_send.close()
    udp_receive.close()

def test_udp_stopping(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['stopping_port'])
    udp_send.send_stopping(True)
    received = udp_receive.receive_stop()
    print(received)
    assert received == True
    udp_send.close()
    udp_receive.close()


def test_udp_send_prediction(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['prediction_port'])
    udp_send.send_pred(1.0)
    received = udp_receive.receive_pred()
    print(received, 'second function')
    assert received == 1
    udp_send.close()
    udp_receive.close()

def test_udp_communication_timeout(UDP_configs):
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['prediction_port'])
    start_time = time.time()
    udp_receive.receive_pred()
    assert time.time() - start_time < 1
    udp_receive.close()


def test_udp_send_invalid_data(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    with pytest.raises(ValueError):
        udp_send.send_all('not a float', True) # type: ignore
    udp_send.close()


def test_UDP_receive_stop_false(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    udp_send.send_stopping(False)
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['stopping_port'])
    received = udp_receive.receive_stop()
    assert received == False
    udp_receive.close()
    udp_send.close()



def test_UDP_receive_pred_loop(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['prediction_port'])
    for i in range(10):
        udp_send.send_pred(i)
    
    received = udp_receive.receive_pred()
    print(received, 'received')
    assert received == 9
    udp_receive.close()
    udp_send.close()
