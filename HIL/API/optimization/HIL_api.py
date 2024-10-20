import fastapi
import yaml
from HIL.optimization.HIL.HIL_API import HIL_API
from .pydantic_models import OptimizeSessionInput, OptimizeInput



def get_app(config_path: str):
    app = fastapi.FastAPI(debug=True, title="HIL API", description="API for HIL optimization")
    args = yaml.load(open(config_path, "r"), Loader=yaml.FullLoader)
    hil_api = HIL_API(args['Optimization'])
    return app, hil_api


@app.get("/generate_session_id")
def generate_session_id():
    return {"session_id": hil_api.generate_session_id()}

@app.post("/optimize_session")
def optimize_session(input_data: OptimizeSessionInput):
    return {"new_parameter": hil_api.optimize_session(input_data.session_id, input_data.current_parameter, input_data.cost)}

@app.post("/optimize")
def optimize(input_data: OptimizeInput):
    return {"optimization_parameters": hil_api.optimize(input_data.parameters, input_data.costs)}