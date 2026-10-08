import pandas as pd, numpy as np, os, random
os.makedirs("data/raw", exist_ok=True)
np.random.seed(42)

rows=[]
for i in range(5000):
  age = np.random.normal(62, 15)
  age = max(18, min(90, int(age)))
  comorbidity = np.random.poisson(2)
  los = np.random.exponential(4) + 1 # length of stay
  prev_admissions = np.random.poisson(1)
  is_diabetic = random.random()<0.3
  is_hf = random.random()<0.25 # heart failure
  discharge_disposition = random.choice(["home","rehab","SNF"])
  lab_abnormal = random.random()<0.4

  # Readmission risk logic
  risk_score = 0
  risk_score += (age-50)*0.02
  risk_score += comorbidity*0.3
  risk_score += (los-3)*0.15
  risk_score += prev_admissions*0.5
  risk_score += 0.8 if is_hf else 0
  risk_score += 0.5 if is_diabetic else 0
  risk_score += 0.6 if lab_abnormal else 0
  risk_score += 0.4 if discharge_disposition=="SNF" else 0

  prob = 1/(1+np.exp(-risk_score+1.5)) # sigmoid
  readmitted = random.random() < prob

  cost = 8000 + los*1500 + comorbidity*2000 + (5000 if readmitted else 0) + np.random.normal(0,1000)

  rows.append({
    "patient_id": f"P_{i}",
    "age": age,
    "comorbidity_count": comorbidity,
    "length_of_stay": round(los,1),
    "prev_admissions": prev_admissions,
    "is_diabetic": is_diabetic,
    "is_heart_failure": is_hf,
    "discharge_disposition": discharge_disposition,
    "lab_abnormal": lab_abnormal,
    "readmitted_30d": readmitted,
    "cost_usd": int(max(1000,cost))
  })

pd.DataFrame(rows).to_csv("data/raw/patients.csv", index=False)
df = pd.DataFrame(rows)
print(f"Generated {len(df)} | Readmission rate: {df['readmitted_30d'].mean()*100:.1f}% | Avg cost: ${df['cost_usd'].mean():.0f}")
