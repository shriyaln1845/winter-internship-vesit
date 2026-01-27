import requests
import json
import time

def test_prediction():
    url = "http://127.0.0.1:8000/predict"
    
    # Needs to match Pydantic model
    payload = {
        "age": 45,
        "gender": "Male",
        "height": 175,
        "weight": 80,
        "physical_activity_level": "Moderate",
        "daily_steps": 6000,
        "diet_quality": "Moderate",
        "sleep_duration": 7.5,
        "stress_level": "Low",
        "family_history": "Yes",
        "polyuria": "No",
        "polydipsia": "No",
        "sudden_weight_loss": "No",
        "polyphagia": "No",
        "visual_blurring": "No"
    }

    try:
        response = requests.post(url, data=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            print("TEST PASSED")
        else:
            print("TEST FAILED")
    except Exception as e:
        print(f"TEST FAILED: {e}")

if __name__ == "__main__":
    # Wait for server to start
    time.sleep(3)
    test_prediction()
