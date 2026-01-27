import joblib
import os

try:
    path = "models/feature_order.pkl"
    if not os.path.exists(path):
        path = "model/feature_order.pkl"
        
    features = joblib.load(path)
    print("FEATURES_LIST:")
    for f in features:
        print(f)
except Exception as e:
    print(f"Error: {e}")
