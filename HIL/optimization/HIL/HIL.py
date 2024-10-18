from enum import Enum
from abc import ABC, abstractmethod
import numpy as np


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
        # Optimization variables.
        self.n = int(0) # number of optimization
        self.x = np.array([]) # input parameter for the exoskeleton
        self.y = np.array([]) # cost function
        self.args = args
        self.start_time = 0
        self.WARM_UP = True
        self.x_opt = np.array([])
        self.y_opt = np.array([])
        # Setting the FLAGs and the state.
        self.OPTIMIZATION = False
        self.STATE = STATE.EXPLORATION
        self.TIME_BASED = args['time_based']

    @abstractmethod
    def _reset_data_collection(self) -> None:
        """Reset the data collection and restart the clocks
        """
        self.store_cost_data = []
        self.cost_time = 0
        self.start_time = 0

    @abstractmethod
    def _init_opt(self):
        raise NotImplementedError("This method must be implemented in the subclass")

