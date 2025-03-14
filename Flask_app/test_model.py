import pickle

# Function to load a model from a pickle file
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    print(f"Model loaded successfully from {model_path}")
    return model

if __name__ == '__main__':
    # Define paths to your models (update these as needed)
    salary_model_path = 'Models\\svr_model.pkl'
    stability_model_path = 'Models\\xgb_model (1).pkl'

    # Load models
    salary_model = load_model(salary_model_path)
    stability_model = load_model(stability_model_path)
import pandas as pd

# --- Predefined columns (from training data) ---

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
    # Initialize a dictionary with all columns set to 0
    input_dict = {col: 0 for col in STABILITY_COLUMNS}
    
    # Set salary
    input_dict['Salary_USD'] = salary_usd

    # Set correct Job Title (if exists in columns)
    job_col = f"Job_Title_{job_title}"
    if job_col in input_dict:
        input_dict[job_col] = 1

    # Set correct Location (if exists in columns)
    loc_col = f"Location_{location}"
    if loc_col in input_dict:
        input_dict[loc_col] = 1

    # Convert to DataFrame
    return pd.DataFrame([input_dict])

# --- Transform function for Salary Model ---
def transform_input_for_salary(company_size_str, job_title, location):
    # Map company size from string to number
    company_size_map = {'Small': 1, 'Medium': 2, 'Large': 3}
    company_size = company_size_map.get(company_size_str, 1)  # Default to 1 if not found

    # Initialize a dictionary with all columns set to False
    input_dict = {col: False for col in SALARY_COLUMNS}

    # Set mapped company size
    input_dict['Company_Size'] = company_size

    # Set correct Job Title (if exists in columns)
    job_col = f"Job_Title_{job_title}"
    if job_col in input_dict:
        input_dict[job_col] = True

    # Set correct Location (if exists in columns)
    loc_col = f"Location_{location}"
    if loc_col in input_dict:
        input_dict[loc_col] = True

    # Convert to DataFrame
    return pd.DataFrame([input_dict])


# Example user input
salary = 90000
job_title = "Data Scientist"
location = "London"

# Transform input
stability_input = transform_input_for_stability(salary, job_title, location)
print(stability_input)

# Predict Stability
stability_result = stability_model.predict(stability_input)
print("Stability Prediction:", stability_result[0])

# Example user input from UI form
company_size_input = "Medium"
job_title_input = "Data Scientist"
location_input = "London"

# Transform input
salary_input = transform_input_for_salary(company_size_input, job_title_input, location_input)
print(salary_input)

# Predict Salary
salary_prediction = salary_model.predict(salary_input)
print("Predicted Salary (USD):", salary_prediction[0])

