# Import necessary libraries
import numpy as np
import joblib   # For loading the serialized model
import pandas as pd   # For data manipulation
from flask import Flask, request, jsonify   # For creating the Flask API

# Initialize the Flask application
sales_forecast_api = Flask("SuperKart Sales Forecasting API")

# Load the trained SuperKart Sales Forecasting model pipeline
model = joblib.load("deployment_files/superkart_sales_forecast_model_v1_0.joblib")

# Define a route for the home page (GET request)
@sales_forecast_api.get('/')
def home():
    """
    Handles GET requests to the root URL ('/').
    Returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Forecasting API!"

# Define an endpoint for single prediction (POST request)
@sales_forecast_api.post('/v1/sales')
def predict_sales():
    """
    Handles POST requests to '/v1/sales'.
    Expects a JSON payload containing product/store details
    and returns the predicted sales value.
    """
    # Get the JSON data from the request body
    sales_data = request.get_json()

    # Convert JSON into DataFrame (keys must match training features)
    input_data = pd.DataFrame([sales_data])

    # Make prediction
    predicted_sales = model.predict(input_data)[0]

    # Convert to Python float and round
    predicted_sales = round(float(predicted_sales), 2)

    # Return prediction
    return jsonify({'Predicted Sales': predicted_sales})

# Define an endpoint for batch prediction (POST request)
@sales_forecast_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    Handles POST requests to '/v1/salesbatch'.
    Expects a CSV file with product/store details for multiple rows
    and returns predicted sales values as a dictionary.
    """
    # Get uploaded CSV file
    file = request.files['file']

    # Read CSV into DataFrame
    input_data = pd.read_csv(file)

    # Make predictions
    predicted_sales = model.predict(input_data).tolist()

    # Round predictions
    predicted_sales = [round(float(val), 2) for val in predicted_sales]

    # Use an identifier column if available (e.g., 'Product_ID')
    if 'Product_ID' in input_data.columns:
        ids = input_data['Product_ID'].tolist()
        output_dict = dict(zip(ids, predicted_sales))
    else:
        # If no ID column, just return list
        output_dict = {'Predicted Sales': predicted_sales}

    return jsonify(output_dict)

# Run the Flask application
if __name__ == '__main__':
    sales_forecast_api.run(debug=True)
