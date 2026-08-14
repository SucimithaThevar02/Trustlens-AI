import joblib

model = joblib.load("model/scam_model.pkl")

print(model.classes_)