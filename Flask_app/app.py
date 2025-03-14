from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import logging

app = Flask(__name__)

# --- Load Pre-trained Models ---
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    print(f"Model loaded successfully from {model_path}")
    return model

# Paths to models
salary_model_path = 'Models/svr_model.pkl'
stability_model_path = 'Models/xgb_model (1).pkl'

# Load models
salary_model = load_model(salary_model_path)
stability_model = load_model(stability_model_path)

# --- Predefined columns (as per training) ---
STABILITY_COLUMNS = [
    'Salary_USD', 'Job_Title_AI Researcher', 'Job_Title_Cybersecurity Analyst',
    'Job_Title_Data Scientist', 'Job_Title_HR Manager', 'Job_Title_Marketing Specialist',
    'Job_Title_Operations Manager', 'Job_Title_Product Manager', 'Job_Title_Sales Manager',
    'Job_Title_Software Engineer', 'Job_Title_UX Designer', 'Location_Berlin', 'Location_Dubai',
    'Location_London', 'Location_New York', 'Location_Paris', 'Location_San Francisco',
    'Location_Singapore', 'Location_Sydney', 'Location_Tokyo', 'Location_Toronto'
]

SALARY_COLUMNS = [
    'Company_Size', 'Location_Dubai', 'Location_London', 'Location_New York', 'Location_Paris',
    'Location_San Francisco', 'Location_Singapore', 'Location_Sydney', 'Location_Tokyo',
    'Location_Toronto', 'Job_Title_Cybersecurity Analyst', 'Job_Title_Data Scientist',
    'Job_Title_HR Manager', 'Job_Title_Marketing Specialist', 'Job_Title_Operations Manager',
    'Job_Title_Product Manager', 'Job_Title_Sales Manager', 'Job_Title_Software Engineer',
    'Job_Title_UX Designer'
]

# --- Transform function for Stability Model ---
def transform_input_for_stability(salary_usd, job_title, location):
    input_dict = {col: 0 for col in STABILITY_COLUMNS}
    input_dict['Salary_USD'] = salary_usd
    job_col = f"Job_Title_{job_title}"
    loc_col = f"Location_{location}"
    if job_col in input_dict:
        input_dict[job_col] = 1
    if loc_col in input_dict:
        input_dict[loc_col] = 1
    return pd.DataFrame([input_dict])

# --- Transform function for Salary Model ---
def transform_input_for_salary(company_size_str, job_title, location):
    company_size_map = {'Small': 1, 'Medium': 2, 'Large': 3}
    company_size = company_size_map.get(company_size_str, 1)
    input_dict = {col: False for col in SALARY_COLUMNS}
    input_dict['Company_Size'] = company_size
    job_col = f"Job_Title_{job_title}"
    loc_col = f"Location_{location}"
    if job_col in input_dict:
        input_dict[job_col] = True
    if loc_col in input_dict:
        input_dict[loc_col] = True
    return pd.DataFrame([input_dict])

# --- Flask Routes ---

@app.route('/')
def home():
    return render_template('template.html')

# Handle Salary Prediction form
@app.route('/predict_salary', methods=['POST'])
def predict_salary():
    job_title_salary = request.form.get('job_title_salary')
    company_size = request.form.get('company_size')
    location_salary = request.form.get('location_salary')

    print(f"Job Title for Salary: {job_title_salary}")
    print(f"Company Size: {company_size}")
    print(f"Location: {location_salary}")

    # Transform and predict
    salary_input = transform_input_for_salary(company_size, job_title_salary, location_salary)
    salary_prediction = salary_model.predict(salary_input)[0]
    salary_prediction = round(salary_prediction, 2)

    return render_template('template.html', salary_prediction=f"${salary_prediction:,} USD")

# Handle Job Stability Prediction form
STABILITY_LABEL_MAP = {0: 'Decline', 1: 'Growth', 2: 'Stable'}

# Handle Job Stability Prediction form
@app.route('/predict_stability', methods=['POST'])
def predict_stability():
    job_title_stability = request.form.get('job_title_stability')
    location_stability = request.form.get('location_stability')
    salary_usd = request.form.get('salary_usd')

    print(f"Job Title for Stability: {job_title_stability}")
    print(f"Location: {location_stability}")
    print(f"Salary (USD): {salary_usd}")

    # Transform and predict
    try:
        salary_usd_value = float(salary_usd)
    except ValueError:
        return render_template('template.html', stability_prediction="Invalid salary input. Please enter a valid number.")

    stability_input = transform_input_for_stability(salary_usd_value, job_title_stability, location_stability)
    stability_prediction = stability_model.predict(stability_input)[0]

    # Map numeric prediction to label
    stability_result = STABILITY_LABEL_MAP.get(stability_prediction, "Unknown")

    return render_template('template.html', stability_prediction=f"Predicted Job Growth: {stability_result}")

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
