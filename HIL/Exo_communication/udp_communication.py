import logging
from HIL.Exo_communication.utils import _UDP

# object to create and initialize the hander class for sending

# TODO add the documentation for these class
class UDPSend(object):
    
    def __init__(self, target_ip: str = 'localhost', prediction_port: int = 50005,stopping_port:int = 50007) -> None:
        """
        UDP communication class to send the data to the exoskeleton

        Args:
        target_ip (str, optional): IP address of the exoskeleton computer or port. Defaults to 'localhost'.
        prediction_port (int, optional): Port for sending the prediction data. Defaults to 50005.
        stopping_port (int, optional): Port for sending the stopping data. Defaults to 50007.
        """
        self.target_ip = target_ip
        self.prediction_port = prediction_port
        self.stopping_port = stopping_port
        self._prediction = _UDP(self.target_ip, self.prediction_port) #type: ignore
        self._stoping  = _UDP(self.target_ip, self.stopping_port) #type: ignore
        self._logger = logging.Logger(__name__)
        self._logger.info(f'started comm port with ip {self.target_ip},\
                  prediction port {self.prediction_port}, stopping port \
                  {self.stopping_port}')

    def send_all(self, prediction : float, stopping: bool) -> None:
        """
        Send the prediction and stopping data to the exoskeleton

        Args:
        prediction (float): Prediction data
        stopping (float): Stopping data
        """

        # data validation 
        if not isinstance(prediction, float) or not isinstance(stopping, bool):
            self._logger.error(f'prediction is not a float or stopping is not a bool')
            raise ValueError('prediction is not a float or stopping is not a bool')

        self._logger.info(f'sending the data to {self.prediction_port}  stopping port: {self.stopping_port}')
        self._prediction.send(prediction)

        if stopping:
            self._stoping.send('STOP')

    def send_pred(self,prediction:float) -> None:
        """
        Send the prediction data to the exoskeleton

        Args:
        prediction (float): Prediction data
        """
        self._prediction.send(prediction)

    def send_stopping(self, stoping:bool) -> None:
        """
        Send the stopping data to the exoskeleton

        Args:
        stoping (float): Stopping data
        """
        self._stoping.send(stoping)

    def close(self) -> None:
        """
        Close the socket
        """
        self._prediction.close()
        self._stoping.close()


class UDPReceive(object):
    def __init__(self, target_ip = 'localhost', port = 30005) -> None:
        """
        UDP communication class to receive the data from the exoskeleton

        Args:
        target_ip (str, optional): IP address of the exoskeleton computer or port. Defaults to 'localhost'.
        port (int, optional): Port for receiving the data. Defaults to 30005.
        """
        self._receiving = _UDP(ip = target_ip, receiving= True, receiving_ip = port)
        self._logger = logging.Logger(__name__)


    def receive_stop(self) -> bool:
        """
        Receive the data from the exoskeleton and see if it is a stop signal then return True else False

        Returns:
        data (str): Stopping data
        """
        data = self._receiving.receive()
        if type(data) != type(None):
            self._logger.info(f'received data: {data}')
            return True
        else:
            self._logger.info(f'no data received')
            return False

    def receive_pred(self) -> float | None:
        """
        Receive the prediction data from the exoskeleton

        Returns:
        data (float): Prediction data
        """
        data = self._receiving.receive()
        if type(data) != type(None):
            self._logger.info(f'received data: {data}')
            return float(data) # convert bytes to float # type: ignore
        else:
            self._logger.info(f'no data received')
            return None

    def close(self) -> None:
        """
        Close the socket
        """
        self._receiving.close()








# # simple script to test the communication
# if __name__ == "__main__":
#     MESSAGE = b'test'
#     sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
#     sock.sendto(MESSAGE, ('localhost', 5005))
#     an = _UDP()
#     i = 1
#     communication = UDPSend()
#     while i < 10000:
#         i += 1
#         communication.send_pred(i)
#         time.sleep(1)
#         print(i)
#     an.close()

