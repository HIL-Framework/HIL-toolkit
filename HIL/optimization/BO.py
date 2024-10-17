import math
import os
import torch
from torch.optim import Adam # type: ignore
from botorch.models import SingleTaskGP
# from botorch.fit import fit_gpytorch_model
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.acquisition import ExpectedImprovement, qExpectedImprovement, qNoisyExpectedImprovement
from botorch.acquisition.analytic import ProbabilityOfImprovement
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.constraints import GreaterThan, Interval
from botorch.sampling import IIDNormalSampler
from botorch.optim import optimize_acqf

# local imports
from HIL.optimization.kernel import SE, Matern 

import numpy as np
import matplotlib.pyplot as plt

# utils
import logging
from typing import Any, Optional, Tuple, Dict

    

import warnings
warnings.filterwarnings("ignore")


class BayesianOptimization(object):
    """
    Bayesian Optimization class for HIL
    """
    def __init__(self, n_parms:int = 1, range: np.ndarray = np.array([0,1]), noise_range :np.ndarray = np.array([0.005, 10]), acq: str = "ei",
        kernel: str = "SE", model_save_path : str = "", device : str = "cpu" , plot: bool = False, kernel_parms: Dict = {}) -> None:
        """Bayesian optimization for HIL

        Args:
            n_parms (int, optional): Number of optimization parameters ( exoskeleton parameters). Defaults to 1.
            range (np.ndarray, optional): Range of the optimization parameters. Defaults to np.array([0,1]).
            noise_range (np.ndarray, optional): Range of noise contraints for optimization. Defaults to np.array([0.005, 10]).
            acq (str, optional): Selecting acquisition function, options are 'ei', 'pi'. Defaults to "ei".
            kernel (str, optional): Selecting kernel for the GP, options are "SE", "Matern". Defaults to "SE".
            model_save_path (str, optional): Path the new optimization saving directory. Defaults to "".
            device (str, optional): which device to perform optimization, "gpu", "cuda" or "cpu". Defaults to "cpu".
            plot (bool, optional): options to plot the gp and acquisition points. Defaults to False.
            kernel_parms (Dict, optional): Dictionary of kernel parameters. Defaults to {}.
        """
        if kernel == "SE":
            if kernel_parms == {}:
                self.kernel = SE(n_parms=n_parms)
            else:
                self.kernel = SE(**kernel_parms)
            self.covar_module = self.kernel.get_covr_module()

        else:
            if kernel_parms == {}:
                self.kernel = Matern(n_parms=n_parms)
            else:
                self.kernel = Matern(**kernel_parms)
            self.covar_module = self.kernel.get_covr_module()
        
        self.n_parms = n_parms
        self.range = range.reshape(2,self.n_parms).astype(float)
        
        if len(model_save_path):
            self.model_save_path = model_save_path
        else:
            # this is temp
            self.model_save_path = "tmp_data/"

        

        # place holder for model
        self.model = None

        # place to store the parameters
        self.x = torch.tensor([])
        self.y = torch.tensor([])

        # device 
        self.device = device

        # plotting
        self.PLOT = plot

        # logging
        self.logger = logging.getLogger()

        # Noise constraints
        self._noise_constraints = noise_range 
        self.likelihood = GaussianLikelihood() #noise_constraint=Interval(self._noise_constraints[0], self._noise_constraints[1]))

        # number of sampling in the acquisition points
        self.N_POINTS = 200

        # acquisition function type
        self.acq_type = acq

    def _step(self) -> np.ndarray:
        """ Fit the model and identify the next parameter, also plots the model if plot is true

        Returns:
            np.ndarray: Next parameter to sampled
        """

        parameter, value = self._fit()
        new_parameter = parameter.detach().cpu().numpy()

        self.logger.info(f"Next parameter is {new_parameter}")

        self._save_model()


        return new_parameter

    def _get_data_best(self) -> float:
        """Get the best value predicted by the model

        Returns:
            float: best value
        """
        
        range = np.arange(self.range[0,:], self.range[1,:], self.N_POINTS)
        range = torch.tensor(range)
        self.model.eval() #type: ignore
        output = self.model(range)     #type: ignore
        return torch.max(output).detach().numpy() #type: ignore

    def _training(self, model, likelihood,train_x,train_y):

        """
        Train the model using Adam Optimizer and gradient descent
        Log Marginal Likelihood is used as the cost function
        """
           
        parameter = list(model.parameters()) + list(likelihood.parameters())
        optimizer = Adam(parameter, lr=0.01) 
        mll= ExactMarginalLogLikelihood(likelihood, model).to(train_x)
         

        train_y=train_y.squeeze(-1)
        loss = -mll(model(train_x), train_y) #type: ignore
        self.logger.info("before training Loss: ", loss.item())
        for i in range(500):
            
            optimizer.zero_grad()
            output = model(train_x)
            loss = -mll(output, train_y) #type: ignore
            
            loss.backward()
            optimizer.step()
        self.logger.info("after training Loss: ", loss.item()) 

    def _fit(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Using the model and likelihood select the next data point to get next data points and acq value at that point

        Returns:
            Tuple[torch.tensor, torch.tensor]: next parmaeter, value at the point
        """
        self._training(self.model, self.likelihood, self.x, self.y)

        if self.acq_type == "ei":
            acq = qNoisyExpectedImprovement(self.model, self.x, sampler=IIDNormalSampler(torch.Size([self.N_POINTS]), seed=1234)) #type: ignore
        else:
            # TODO add other acquisition functions
            best_f = self._get_data_best()
            acq = ProbabilityOfImprovement(self.model, best_f, sampler=IIDNormalSampler(torch.Size([self.N_POINTS]), seed=1234)) #type: ignore

        new_point, value  = optimize_acqf(
            acq_function = acq,
            bounds=torch.tensor(self.range).to(self.device),
            q = 1,
            num_restarts=1000,
            raw_samples=2000,
            options={},
        )
        return new_point, value

    def _save_model(self) -> None:
        """Save the model and data in the given path
        """
        save_iter_path = self.model_save_path + f'iter_{len(self.x)}'
        os.makedirs(save_iter_path, exist_ok=True)
        model_path = save_iter_path +'/model.pth'
        torch.save(self.model.state_dict(), model_path) #type: ignore
        data_save = save_iter_path + '/data.csv'
        x = self.x.detach().cpu().numpy()
        y = self.y.detach().cpu().numpy()
        full_data = np.hstack((x,y))
        np.savetxt(data_save, full_data)
        self.logger.info(f"model saved successfully at {save_iter_path}")

    def run(self, x: np.ndarray, y: np.ndarray, reload_hyper: bool  = False ) -> np.ndarray:
        """Run the optimization with input data points

        Args:
            x (NxM np.ndarray): Input parameters N -> n_parms, M -> iter
            y (Mx1): Cost function array
            reload_hyper (bool, optional): Reload the hyper parameter trained in the previous iter. Defaults to True.

        Returns:
            np.ndarray: parameter to sample next
        """

        
        assert len(x) == len(y), "Length should be equal."

        self.x = torch.tensor(x).to(self.device)
        self.y = torch.tensor(y).to(self.device)

        if not reload_hyper:
            self.kernel.reset()
            self.likelihood = GaussianLikelihood(noise_constraint = Interval(self._noise_constraints[0], self._noise_constraints[1]))
            self.model = SingleTaskGP(self.x, self.y, likelihood = self.likelihood, covar_module = self.kernel.get_covr_module()) 
            # TODO check if this ok for multi dimension models
            self.model.to(self.device)

        else:
            # keeping the likehood save and kernel parameters so no need to reset those
            self.model = SingleTaskGP(self.x, self.y, likelihood = self.likelihood, covar_module = self.kernel.get_covr_module())
            self.model.to(self.device)

        # fi the model and get the next parameter.
        new_parameter = self._step()
        
        return new_parameter
        

