import uvicorn
from HIL.API.optimization.HIL_api import HILAPIWrapper


if __name__ == "__main__":
    wrapper = HILAPIWrapper("configs/api-optimization-config.yml")
    uvicorn.run(wrapper.app, host="0.0.0.0", port=8000)
