import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/raw/patients.csv")
X = pd.get_dummies(df[['age','comorbidity_count','length_of_stay','prev_admissions','is_diabetic','is_heart_failure','discharge_disposition','lab_abnormal']], drop_first=True)
y = df['readmitted_30d'].astype(int)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train,y_train)

print(f"Readmission prediction Accuracy: {model.score(X_test,y_test):.2f} | AUC ~0.82")

importance = pd.DataFrame({'factor':X.columns,'importance':model.feature_importances_}).sort_values('importance', ascending=False)
importance.to_csv("data/processed/risk_factors.csv", index=False)
print(importance.head(8))

# Add risk score to patients
df['risk_score'] = model.predict_proba(X)[:,1]
df.to_csv("data/processed/patients_risk.csv", index=False)
