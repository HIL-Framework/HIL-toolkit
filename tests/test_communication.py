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



def test_udp_send_all(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['prediction_port'])
    udp_send.send_all(1.0, True)
    assert udp_receive.receive() == 1
    udp_send.close()
    udp_receive.close()

def test_udp_stopping(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['stopping_port'])
    udp_send.send_stopping(True)
    assert udp_receive.receive() == 1
    udp_send.close()
    udp_receive.close()


def test_udp_send_prediction(UDP_configs):
    udp_send = UDPSend(UDP_configs['target_ip'], UDP_configs['prediction_port'], UDP_configs['stopping_port'])
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['prediction_port'])
    udp_send.send_pred(1)
    assert udp_receive.receive() == 1
    udp_send.close()
    udp_receive.close()

def test_udp_communication_timeout(UDP_configs):
    udp_receive = UDPReceive(UDP_configs['target_ip'], UDP_configs['prediction_port'])
    start_time = time.time()
    udp_receive.receive()
    assert time.time() - start_time < 1
    udp_receive.close()


