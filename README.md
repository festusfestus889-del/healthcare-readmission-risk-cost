# Healthcare Readmission Risk & Cost Impact Analysis

**Problem:** 30% 30-day readmission → CMS penalties + extra cost

**Pipeline:**
1. Generated 5000 synthetic patients (age, LOS, comorbidities, heart failure, diabetes)
2. RandomForest predicts readmission risk (Accuracy 0.82)
3. Risk drivers: prev_admissions, heart failure, LOS, comorbidity count
4. What-if: Target top 20% high-risk with care management → prevent 40% readmissions → Net savings $420k per 5000 patients, ROI 8x

**Stack:** Python, Scikit-learn, Streamlit, Plotly, GitHub Actions (daily 9am)

**Run:** `streamlit run app.py`
