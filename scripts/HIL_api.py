import uvicorn
from HIL.API.optimization.HIL_api import HILApp


if __name__ == "__main__":
    app = HILApp("configs/api-optimization-config.yml")
    uvicorn.run(app.app, host="0.0.0.0", port=8000)
