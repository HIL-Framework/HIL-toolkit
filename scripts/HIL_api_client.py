import requests
from typing import Optional 


def query_api(url: str, data: dict, request_type: str = "get") -> Optional[dict]:
    if request_type == "get":
        response = requests.get(url, params=data)
    elif request_type == "post":
        response = requests.post(url, json=data)
    else:
        raise ValueError(f"Invalid request type: {request_type}")
    
    return response.json()


def generate_session_id(url: str = "http://localhost:8000/generate_session_id") -> str:
    response = query_api(url, {}, "post")
    if response is None:
        raise ValueError("Failed to generate session id")
    return response["session_id"]


def optimize() -> Optional[dict]:
    parameters = [[50.0], [30.0], [10.0], [80.0]]
    costs = [[1.0], [2.0], [3.0], [4.0]]
    request = {
        "parameters": parameters,
        "costs": costs
    }
    return query_api("http://localhost:8000/optimize", request, "post")


if __name__ == "__main__":
    print(optimize())

