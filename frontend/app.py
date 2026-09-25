import streamlit as st
import pandas as pd
import requests

# Inside the Docker network the backend container is reachable by its name
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Forecasting App")
st.write("Enter the product and store details below to forecast the total sales for that product in that store.")

# Product details (defaults match the sample payload in the inference section)
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area (share of display area)", min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
Product_MRP = st.number_input("Product MRP (max retail price)", min_value=0.0, value=117.08)
Product_Id_char = st.selectbox("Product ID Prefix (FD = food, DR = drinks, NC = non-consumable)", ["FD", "DR", "NC"])
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"], index=1)

# Store details
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"], index=1)
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"], index=1)
Store_Type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"], index=2)
Store_Age_Years = st.number_input("Store Age (years)", min_value=0, value=16)

# Keys must match the feature names the backend expects
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category,
}

# Single prediction
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Forecasted sales for this product in this store: ${result['Predicted Sales']:,.2f}")
    else:
        st.error("Unable to connect to the prediction API.")

# Batch prediction
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict for Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})

        if response.status_code == 200:
            results = response.json()
            st.success("Predictions completed successfully!")

            # One row per uploaded record, with the forecast next to its row number
            results_df = pd.DataFrame(list(results.items()), columns=["Row", "Predicted Sales"])
            st.dataframe(results_df, use_container_width=True)
        else:
            st.error("Unable to connect to the prediction API.")
