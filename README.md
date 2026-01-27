# Diabetes Risk AI

An AI-powered web application that predicts the risk of diabetes based on lifestyle and health data. Built with FastAPI and Machine Learning.

## Features
- **Instant Risk Assessment**: Get a probability score based on 15+ health factors.
- **Interactive UI**: Clean, modern interface using TailwindCSS.
- **Visual Dashboard**: See your health metrics and actionable advice.
- **Privacy First**: Data is processed locally in the session.

## Setup & Installation

1. **Clone the repository** (if not already present).
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   uvicorn app:app --reload
   ```
   Or double-click `run_app.bat` on Windows.

## Tech Stack
- **Backend**: Python (FastAPI, Scikit-Learn, Pandas)
- **Frontend**: HTML5, Jinja2 Templates, TailwindCSS, Chart.js
- **Model**: Trained Random Forest/Gradient Boosting Classifier (saved in `model/`)

## Disclaimer
This tool is for educational and informational purposes only and does not constitute medical advice.
