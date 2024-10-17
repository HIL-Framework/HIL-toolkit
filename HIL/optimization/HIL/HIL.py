from enum import Enum
from abc import ABC, abstractmethod


class STATE(Enum):
    EXPLORATION = 1
    OPTIMIZATION = 2
    DONE = 3

class HIL_MODE(Enum):
    """
    CLI: Command line interface, used in the terminal and local machine. The CLI model will use the pylsl for the communication between the modules.
    API: Application programming interface, used for communicating between different modules and languages, this is done using fastapi.
    """
    CLI = 1
    API = 2


class HIL_base(ABC):
    """
    This is the base class for the HIL.
    """
    def __init__(self, args: dict) -> None:
        self.args = args


    @abstractmethod
    def _reset_data_collection(self):
        raise NotImplementedError("This method must be implemented in the subclass")

    @abstractmethod
    def _outlet_cost(self):
        raise NotImplementedError("This method must be implemented in the subclass")
    

    @abstractmethod
    def _start_optimization(self):
        raise NotImplementedError("This method must be implemented in the subclass")


    @abstractmethod
    def start(self):
        raise NotImplementedError("This method must be implemented in the subclass")


