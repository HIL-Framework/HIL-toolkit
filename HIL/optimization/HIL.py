import numpy as np
import time 
import pylsl
from enum import Enum
import logging

from HIL.optimization.BO import BayesianOptimization
from HIL.optimization.extract_cost import ExtractCost


class STATE(Enum):
    EXPLORATION = 1
    OPTIMIZATION = 2
    DONE = 3


class HIL:
    """ Main HIL optimization
        This program will extract cost from the pylsl stream.
        Run the optimization.
        Check if the optimization is done.
    """
    def __init__(self, args: dict) -> None:
        """ cost_name: name of the cost function.
        """
        self.n = int(0) # number of optimization
        self.x = np.array([]) # input parameter for the exoskeleton
        self.y = np.array([]) # cost function
        self.args = args

        # start the
        self.start_time = 0 

        self._outlet_cost()

        self._reset_data_collection()


        # start optimization
        self._start_optimization(self.args['Optimization'])

        # start cost function
        self._start_cost(self.args['Cost'])

        # self.warm_up
        self.warm_up = True

        # start optimization
        self.OPTIMIZATION = False

        # The ones which are done. 
        self.x_opt = np.array([])
        self.y_opt = np.array([])

        # state
        self.STATE = STATE.EXPLORATION

        # Consider time 
        self.TIME_BASED = args['time_based']

        self.logger = logging.getLogger(__name__)
    
    def _outlet_cost(self) -> None:
        """Create an outlet function to send when the optimization has changed
        """
        info = pylsl.StreamInfo(name="Change_parm", type="Marker", channel_count=2, source_id='12345')
        self.outlet = pylsl.StreamOutlet(info)

    def _reset_data_collection(self)  -> None:
        """Reset data collection and restart the clocks
        """
        self.store_cost_data = []
        self.cost_time = 0
        self.start_time = 0

    def _start_optimization(self, args: dict) -> None:
        """O Start the optimization function, this will start the BO module

        Args:
            args (dict): Optimization args
        """
        # print(args['range'][0], args['range'][1])
        # print(np.array(list(args['range'])))
        # print(args['kernel_parms'])
        self.BO = BayesianOptimization(n_parms=args['n_parms'], 
                range=np.array(list(args['range'])), 
                model_save_path=args['model_save_path'], 
                kernel=args['kernel_function'],
                kernel_parms=args['kernel_parms'])

    def _start_cost(self, args: dict) -> None:
        """Start the cost extraction module

        Args:
            args (dict): Cost args
        """
        self.cost_time = 0
        self.cost = ExtractCost(cost_name=args['Name'], number_samples=args['n_samples'])

    @property
    def _check_time_based(self):
        if (not self.TIME_BASED) or (self.TIME_BASED and (self.cost_time - self.start_time) > self.args['Cost']['time']):
            return True
        else:
            return False
    
    @property
    def _check_cost_based(self):
        if len(self.store_cost_data) > self.args['Cost']['max_samples_per_cost']:
            return True
        else:
            return False


    def _optimize_and_push(self):
        new_parameter = self.BO.run(self.x_opt.reshape(self.n, -1), self.y_opt.reshape(self.n, -1))
        self.logger.info(f"Next parameter is {new_parameter}")
        self.x = np.concatenate((self.x, new_parameter.reshape(1,)), axis = 0)
        self.outlet.push_sample([self.x_opt[-1],self.y_opt[-1]])

    def start_cli(self):
        if self.n == 0:
            print(f'############################################################')
            print(f'############## Starting the optimization ###################')
            print(f'############## Using cost function {self.cost.cost_name} ###')
            print(f'############################################################')
            self._generate_initial_parameters()
            self.outlet.push_sample([0,0])
        # start the optimization loop.
        while self.n < self.args['Optimization']['n_steps']:


            # Still in exploration
            if self.n < self.args['Optimization']['n_exploration'] and self.STATE == STATE.EXPLORATION:
                print(f"{self.n=}, {self.x=} iteration")
                self.logger.info(f"In the exploration step {self.n}, parameter {self.x[self.n]}, len_cost {len(self.store_cost_data)}")
                
                if self.n == 0 and self.warm_up:
                    input(f"Please give 2 min of warmup and hit any key to continue \n")
                    self.warm_up = False
                self._get_cost()
                if self._check_time_based and self._check_cost_based:
                    print(f" cost is {np.nanmean(self.store_cost_data[-self.args['Cost']['n_samples']:])}")
                    out = input("Press Y to record the data: N to remove it:")
                    if out == 'N':
                        self._reset_data_collection()
                        self.logger.info("Recollecting data")
                        print("#" * 25)
                        print("# Recollecting data #".center(25))
                        print("#" * 25)
                    else:
                        self.x_opt = np.append(self.x_opt, self.x[self.n]) if len(self.x_opt) > 0 else np.array([self.x[0]])

                        mean_cost = np.nanmean(self.store_cost_data[-self.args['Cost']['n_samples']:])
                        
                        self.y_opt = np.append(self.y_opt, mean_cost) if len(self.y_opt) > 0 else np.array([mean_cost])

                        self.logger.info(f"recording cost function {self.y_opt[-1]}, for the parameter {self.x_opt[-1]}")
                        self.outlet.push_sample([self.x_opt[-1],self.y_opt[-1]])
                        self._reset_data_collection()
                        self.n += 1
                        if self.n == self.args['Optimization']['n_start_points'] :
                            self.logger.info(f"Starting the optimization")
                            self.STATE = STATE.OPTIMIZATION 
                            # start the optimization
                            self._optimize_and_push()



            if self.STATE == STATE.OPTIMIZATION:
                print(f"In the optimization loop {self.n}, parameter {self.x[self.n]}")
                self._get_cost()
                if self._check_time_based and self._check_cost_based:
                    out = input("Press Y to record the data: N to remove it:")
                    if out == 'N':
                        self._reset_data_collection()
                        print("################################")
                        print("########### recollecting #######")
                        print("################################")
                    else:
                        self.x_opt = np.concatenate((self.x_opt, np.array([self.x[self.n]])))
                        mean_cost = np.nanmean(self.store_cost_data[-5:])
                        self.y_opt = np.concatenate((self.y_opt, np.array([mean_cost])))
                        self.n += 1

                        self._optimize_and_push()
                        self._reset_data_collection()
            
            if self.n == self.args['Optimization']['n_steps']:
                self.STATE = STATE.DONE
                print(f"Optimization is done")
                break
                    

            time.sleep(self.args['Cost']['time_step'])

    def _generate_initial_parameters(self) -> None:
        opt_args = self.args['Optimization']
        self.x = np.random.random(opt_args['n_start_points'])*(opt_args['range'][1] - opt_args['range'][0]) + opt_args['range'][0]
        print(f'###### start functions are {self.x} ######') 
        
        
    def _get_cost(self) -> None:
        """This function extracts cost from pylsl, need to be called all the time."""
        data,time_stamp = self.cost.extract_data()
        if time_stamp is not None:
            # changing maximization to minimization.
            data = data[-1] * -1
            self.cost_time = time_stamp
            self.store_cost_data.append(data)
            if len(self.store_cost_data) == 1:
                self.start_time = time_stamp
            # print(f"got cost {self.store_cost_data[-1]}, parameter {self.x[self.n]}, time: {self.cost_time - self.start_time}")
            



                
                    
