import joblib
import json

f = joblib.load('model/feature_order.pkl')
with open('features_full.json', 'w') as out:
    json.dump(f, out)
