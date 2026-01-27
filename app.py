from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd
import uvicorn
import os
from datetime import datetime

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Load Model and Features
MODEL_PATH = "model/diabetes_model.pkl"
FEATURE_PATH = "model/feature_order.pkl"

try:
    model = joblib.load(MODEL_PATH)
    feature_order = joblib.load(FEATURE_PATH)
    print("Model and features loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load model/features. {e}")
    model = None
    feature_order = []

def map_categorical(value, mapping):
    return mapping.get(value, 0)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "current_year": datetime.now().year
    })

@app.get("/risk-test", response_class=HTMLResponse)
async def read_risk_test(request: Request):
    return templates.TemplateResponse("risk_test.html", {
        "request": request,
        "current_year": datetime.now().year
    })

@app.post("/predict", response_class=HTMLResponse)
async def predict_risk(
    request: Request,
    age: int = Form(...),
    gender: str = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    physical_activity_level: str = Form(...),
    daily_steps: int = Form(5000),
    diet_quality: str = Form(...),
    sleep_duration: float = Form(...),
    stress_level: str = Form(...),
    family_history: str = Form(...),
    polyuria: str = Form(...),
    polydipsia: str = Form(...),
    sudden_weight_loss: str = Form(...),
    polyphagia: str = Form(...),
    visual_blurring: str = Form(...)
):
    # Calculate BMI
    height_m = height / 100.0
    bmi = weight / (height_m * height_m)

    # Encode inputs
    binary_map = {"No": 0, "no": 0, "Yes": 1, "yes": 1}
    gender_map = {"Female": 0, "Male": 1}
    level_map = {"Low": 1, "Moderate": 2, "High": 3}

    input_dict = {
        "age": age,
        "gender": map_categorical(gender, gender_map),
        "bmi": bmi,
        "polyuria": map_categorical(polyuria, binary_map),
        "polydipsia": map_categorical(polydipsia, binary_map),
        "sudden_weight_loss": map_categorical(sudden_weight_loss, binary_map),
        "polyphagia": map_categorical(polyphagia, binary_map),
        "visual_blurring": map_categorical(visual_blurring, binary_map),
        "physical_activity_level": map_categorical(physical_activity_level, level_map),
        "daily_steps": daily_steps,
        "sleep_duration": sleep_duration,
        "stress_level": map_categorical(stress_level, level_map),
        "diet_quality": map_categorical(diet_quality, level_map),
        "family_history_binary": map_categorical(family_history, binary_map),
    }

    # Predict
    risk_score = 0
    risk_level = "Unknown"
    
    if model:
        try:
            df = pd.DataFrame([input_dict])
            # Ensure proper column order
            df = df[feature_order]
            prob = model.predict_proba(df)[0][1] * 100
            risk_score = round(prob, 2)
            
            if prob < 30:
                risk_level = "Low"
            elif prob < 60:
                risk_level = "Moderate"
            else:
                risk_level = "High"
        except Exception as e:
            print(f"Prediction Error: {e}")
            risk_level = "Error"

    # Create readable labels for dashboard
    display_info = {
        "Age": age,
        "Gender": gender,
        "BMI": round(bmi, 1),
        "Activity": physical_activity_level,
        "Steps": daily_steps,
        "Diet": diet_quality,
        "Sleep": f"{sleep_duration}h",
        "Stress": stress_level,
        "Family History": family_history
    }

    # Context for Dashboard
    context = {
        "request": request,
        "current_year": datetime.now().year,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "inputs": input_dict,
        "display_info": display_info,
        "raw_bmi": round(bmi, 1)
    }

    return templates.TemplateResponse("dashboard.html", context)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
