# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import joblib
# import pandas as pd

# app = FastAPI()

# # Load model and scaler
# model = joblib.load('Loan_status_predictor_rf.pkl')
# scaler = joblib.load('vector.pkl')  # ✅ Corrected

# # List of numeric columns for scaling
# nums_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']

# # Define the request body schema
# class LoanApproval(BaseModel):
#     Gender: float
#     Married: float
#     Dependents: float
#     Education: float
#     Self_Employed: float
#     ApplicantIncome: float
#     CoapplicantIncome: float
#     LoanAmount: float
#     Loan_Amount_Term: float
#     Credit_History: float
#     Property_Area: float

# # Define the prediction endpoint
# @app.post("/predict")
# async def predict_loan_status(application: LoanApproval):
#     try:
#         # Convert input to DataFrame
#         input_data = pd.DataFrame([application.dict()])

#         # Scale numeric features
#         input_data[nums_cols] = scaler.transform(input_data[nums_cols])

#         # Predict using the model
#         result = model.predict(input_data)

#         # Return result
#         if result[0] == 1:
#             return {'Loan Status': "Approved"}
#         else:
#             return {'Loan Status': "Not Approved"}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load model and scaler
model = joblib.load('Loan_status_predictor_rf.pkl')
scaler = joblib.load('vector.pkl')  # ✅ Corrected

# List of numeric columns for scaling
nums_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']

# Define the request body schema
class LoanApproval(BaseModel):
    Gender: float
    Married: float
    Dependents: float
    Education: float
    Self_Employed: float
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: float

# Define the prediction endpoint
@app.post("/predict")
async def predict_loan_status(application: LoanApproval):
    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([application.dict()])

        # Scale numeric features
        input_data[nums_cols] = scaler.transform(input_data[nums_cols])

        # Predict using the model
        result = model.predict(input_data)

        # Return result
        if result[0] == 1:
            return {'Loan Status': "Approved"}
        else:
            return {'Loan Status': "Not Approved"}

    except Exception as e:
        raise HttpException(status_code=500, detail=f"Prediction error: {str(e)}")