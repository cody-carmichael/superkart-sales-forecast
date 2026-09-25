import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Name the Flask instance superkart_api; the Dockerfile's gunicorn command has to match this name
superkart_api = Flask("SuperKart Sales Predictor")

# Load the full pipeline once at startup (preprocessing + tuned model travel together)
model = joblib.load("superkart_model.joblib")


# Home route, handy for checking the API is alive
@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Forecasting API"


# Single prediction: one product-store combination sent as JSON
@superkart_api.post("/v1/predict")
def predict_sales():
    product_data = request.get_json()

    # Pull out exactly the 10 features the pipeline was trained on
    sample = {
        "Product_Weight": product_data["Product_Weight"],
        "Product_Sugar_Content": product_data["Product_Sugar_Content"],
        "Product_Allocated_Area": product_data["Product_Allocated_Area"],
        "Product_MRP": product_data["Product_MRP"],
        "Store_Size": product_data["Store_Size"],
        "Store_Location_City_Type": product_data["Store_Location_City_Type"],
        "Store_Type": product_data["Store_Type"],
        "Product_Id_char": product_data["Product_Id_char"],
        "Store_Age_Years": product_data["Store_Age_Years"],
        "Product_Type_Category": product_data["Product_Type_Category"],
    }

    input_data = pd.DataFrame([sample])

    # .tolist() turns the numpy value into a plain float so it can go back as JSON
    prediction = model.predict(input_data).tolist()[0]

    return jsonify({"Predicted Sales": round(prediction, 2)})


# Batch prediction: a whole CSV uploaded under the key "file"
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    file = request.files["file"]
    input_data = pd.read_csv(file)

    predictions = [round(x, 2) for x in model.predict(input_data).tolist()]

    # The batch file has no ID column, so we key each prediction by its row number
    output_dict = dict(zip(input_data.index.tolist(), predictions))

    return output_dict


if __name__ == "__main__":
    superkart_api.run(debug=True)
