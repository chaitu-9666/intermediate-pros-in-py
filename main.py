import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Your personal data. Used by Nutritionix to calculate calories.
GENDER = "male"
WEIGHT_KG = 84
HEIGHT_CM = 180
AGE = 32

load_dotenv("env_for_pycharm.env")
# Nutritionix APP ID and API Key. Actual values are stored as environment variables.
APP_ID = os.getenv("ENV_NIX_APP_ID")
API_KEY = os.getenv("ENV_NIX_API_KEY")

# Sheety Project API. Check your Google sheet name and Sheety endpoint
GOOGLE_SHEET_NAME = "workout"
SHEETY_ENDPOINT = os.getenv("ENV_SHEETY_ENDPOINT")

# Nutritionix exercise API endpoint
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

# Ask for input from the user
exercise_text = input("Tell me which exercises you did: ")

# Nutritionix API Call
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Make the request to the Nutritionix API
response = requests.post(exercise_endpoint, json=parameters, headers=headers)

# Check if the request was successful
if response.status_code != 200:
    print(f"Error with Nutritionix API call: {response.text}")
    exit()

result = response.json()
print(f"Nutritionix API call result: \n {result} \n")

# Get the current date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Sheety API Call & Authentication
for exercise in result["exercises"]:
    sheet_inputs = {
        GOOGLE_SHEET_NAME: {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Sheety Authentication with Basic Auth
    sheet_response = requests.post(
        SHEETY_ENDPOINT,
        json=sheet_inputs,
        auth=(
            os.getenv("ENV_SHEETY_USERNAME"),
            os.getenv("ENV_SHEETY_PASSWORD"),
        )
    )

    # Check if the request to Sheety was successful
    if sheet_response.status_code == 200:
        print(f"Exercise added to sheet: {exercise['name'].title()}")
    else:
        print(f"Error adding to Sheety: {sheet_response.text}")

