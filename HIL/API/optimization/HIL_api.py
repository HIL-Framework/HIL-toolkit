import fastapi
import yaml
from HIL.optimization.HIL.HIL_API import HIL_API
from .pydantic_models import OptimizeSessionInput, OptimizeInput
import numpy as np

class HILApp:
    def __init__(self, config_path: str):
        self.app = fastapi.FastAPI(
            debug=True,
            title="HIL API",
            description="API for HIL optimization"
        )
        self.hil_api = self.initialize_hil_api(config_path)
        self.setup_routes()
    
    def initialize_hil_api(self, config_path: str) -> HIL_API:
        with open(config_path, "r") as file:
            args = yaml.load(file, Loader=yaml.FullLoader)
        return HIL_API(args['Optimization'])
    
    def setup_routes(self):
        self.app.get("/generate_session_id")(self.generate_session_id)
        self.app.post("/optimize_session")(self.optimize_session)
        self.app.post("/optimize")(self.optimize)
    
    def generate_session_id(self):
        return {"session_id": self.hil_api.generate_session_id()}
    
    def optimize_session(self, input_data: OptimizeSessionInput):
        new_param = self.hil_api.optimize_session(
            input_data.session_id,
            input_data.current_parameter,
            input_data.cost
        )
        return {"new_parameter": new_param}
    
    def optimize(self, input_data: OptimizeInput):
        optimization_params = self.hil_api.optimize(
            input_data.parameters,
            input_data.costs
        )
        print(f"optimization_params: {optimization_params}")
        print(f"type of optimization_params: {type(optimization_params)}")
        return {"optimization_parameters": optimization_params.tolist()[0]}

def get_app(config_path: str):
    hil_app = HILApp(config_path)
    return hil_app.app, hil_app.hil_api
