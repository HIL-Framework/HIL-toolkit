import socket
import select
from typing import Any
import logging




# base UDP class which will send the data to matlab or any socket
class _UDP():
    def __init__(self, ip = 'localhost', port = '5005', receiving = False, receiving_ip = 30005, timeout = 0.1):
        """
        UDP communication class for general purpose usage.

        Args:
        ip (str, optional): IP address of the exoskeleton computer or port. Defaults to 'localhost'.
        port (int, optional): Port for sending the prediction data. Defaults to 50005.
        receiving (bool, optional): If True, the class will receive data. Defaults to False.
        receiving_ip (int, optional): Port for receiving the data. Defaults to 30005.
        timeout (float, optional): Timeout for receiving the data. Defaults to 0.1.
        """
        logging.warning(f'starting port at {ip}, port {port}')
        # setup the communication
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(0) #type: ignore
        self.port = port
        self.ip = ip
        self._logger = logging.Logger(__name__)
        if receiving:
            self.sock.bind((self.ip, receiving_ip))
            self.sock.settimeout(timeout)
            self.select = select.select([],[self.sock], [], timeout + 0.5)

    def send(self, i: Any) -> None:
        """
        Send the message by encode the string to bytes

        Args:
        i (str): Message to send
        """
        MESSAGE = str(i).encode('utf-8')
        self.sock.sendto(MESSAGE, (self.ip,self.port ))

    def close(self) -> None:
        """
        Close the socket
        """
        logging.warning('closing the socket')
        self.sock.close()
    
    def receive(self) -> Any:
        """
        Receive the latest message from the socket by clearing the buffer.

        Returns:
            str | None: The last received message or None if no data is received.
        """
        data = None
        try:
            if self.select[1]:
                data = self.sock.recv(1024) # buffer size is 1024 bytes
                while data != None:
                    data = self.sock.recv(1024) # buffer size is 1024 bytes
                    self._logger.info(f'{data.decode()} recieved in the loop')
                    # new_data = data
                # data = new_data #type: ignore
        except TimeoutError:
            self._logger.info('timeout, in receive so exiting')
        return data
