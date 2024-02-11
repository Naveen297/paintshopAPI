from flask import Flask, request, jsonify
from flask_cors import CORS
import httpx
from pydantic import BaseModel, ValidationError

# Define your Pydantic models for data validation
class DataModel(BaseModel):
    date_range: str

class TaskModel(BaseModel):
    task: str
    data: DataModel

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/forecast/', methods=['POST'])
def receive_data():
    # Validate request data using Pydantic
    try:
        task_data = TaskModel(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    # Prepare data for the POST request
    json_data = task_data.dict()
    url = "https://wasim.lightinfosys.com/analytics/forecast/"
    timeout = 300.0  # Setting timeout

    # Make synchronous HTTP call using httpx
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=json_data)
            response_data = response.json()

            if 'data' in response_data and isinstance(response_data['data'], dict):
                return jsonify(response_data)
            else:
                return jsonify(response_data)
    except httpx.ReadTimeout:
        return jsonify({"detail": "Timeout occurred while forwarding data"}), 504

if __name__ == '__main__':
    app.run(debug=True)

# from fastapi import FastAPI, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field
# import httpx

# class DataModel(BaseModel):
#     date_range: str = Field(..., example="2023-01-01 2023-01-08")

# class TaskModel(BaseModel):
#     task: str = Field(..., example="dashboard")
#     data: DataModel

# app = FastAPI()

# # Add CORSMiddleware to the application instance
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# @app.post("/forecast/")
# async def receive_data(task_data: TaskModel):
#     url = "https://wasim.lightinfosys.com/analytics/forecast/"
#     json_data = task_data.dict()
    
#     timeout = httpx.Timeout(300.0, connect=300.0, read=300.0, write=300.0)

#     async with httpx.AsyncClient(timeout=timeout) as client:
#         try:
#             response = await client.post(url, json=json_data)
#             response_data = response.json()

#             if 'data' in response_data and isinstance(response_data['data'], dict):
#                 return response_data
#             else:
#                 return response_data
#         except httpx.ReadTimeout:
#             raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Timeout occurred while forwarding data")
