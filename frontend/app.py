import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Forecasting")

# Section for single prediction
st.subheader("Single Prediction")

# Collect user input for product/store features
product_id = st.text_input("Product ID")
store_id = st.text_input("Store ID")
price = st.number_input("Price", min_value=0.0, value=100.0)
category = st.text_input("Category")

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_ID': product_id,
    'Store_ID': store_id,
    'Price': price,
    'Category': category
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales']
        st.success(f"Predicted Sales: {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
