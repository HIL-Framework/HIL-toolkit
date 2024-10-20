from typing import Dict, Tuple
from HIL.optimization.HIL.HIL import HIL_base, HIL_MODE
import logging
from HIL.optimization.BO import BayesianOptimization
import numpy as np
import uuid


class HIL_API(HIL_base):
    def __init__(self, args: dict) -> None:
        super().__init__(args)
        self.mode = HIL_MODE.API
        self.logger = logging.getLogger(__name__)


    def _init_opt(self):
        self.opt_framework = BayesianOptimization(n_parms=self.args['n_parms'], 
                range=np.array(list(self.args['range'])), 
                model_save_path=self.args['model_save_path'], 
                kernel=self.args['kernel_function'],
                kernel_parms=self.args['kernel_parms'],
                save = self.args['save']
                )

    def generate_session_id(self):
        return uuid.uuid4()

    def _fetch_data(self, session_id: str) -> Tuple[np.ndarray, np.ndarray]: #type: ignore
        pass # For now I will connect the a sqlite database later.

    def _store_data(self, session_id: str, parameter: np.ndarray, cost: float) -> None:
        pass

    def _send_data(self, session_id: str) -> Dict:
        return {}

    def optimize_session(self, session_id, current_parameter, cost, reload_hyper: bool = False) -> np.ndarray:
        parameters, costs = self._fetch_data(session_id)
        # TODO need to implement the a logic to hot reload the model here without reoptimizing the hyperparameters.
        new_parameter = self.optimize(parameters, cost, reload_hyper)
        self._store_data(session_id, new_parameter, cost)
        return new_parameter


    def optimize(self, parameters, costs, reload_hyper: bool = False) -> np.ndarray:
        self._init_opt()
        # Convert parameters and costs to float32
        parameters = np.array(parameters, dtype=np.float32)
        costs = np.array(costs, dtype=np.float32)
        new_parameter = self.opt_framework.run(x=parameters, y=costs, reload_hyper=reload_hyper)
        return new_parameter
        