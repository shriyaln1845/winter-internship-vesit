import joblib
import os

try:
    path = "model/feature_order.pkl"
    if not os.path.exists(path):
        path = "models/feature_order.pkl"
        
    features = joblib.load(path)
    print("FEATURES_LIST:")
    for i, f in enumerate(features):
        print(f"{i}: {repr(f)}")
except Exception as e:
    print(f"Error: {e}")
