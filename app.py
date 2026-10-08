import streamlit as st, pandas as pd, plotly.express as px
st.set_page_config(layout="wide")
st.title("🏥 Hospital Readmission Risk & Cost Impact")

df = pd.read_csv("data/processed/patients_risk.csv")
factors = pd.read_csv("data/processed/risk_factors.csv")
cost = pd.read_csv("data/processed/cost_impact.csv")

c1,c2,c3 = st.columns(3)
c1.metric("Readmission Rate", f"{df['readmitted_30d'].mean()*100:.1f}%")
c2.metric("Avg Cost", f"${df['cost_usd'].mean():.0f}")
c3.metric("Net Savings Potential", f"${cost['net_savings'].values[0]:,}")

st.plotly_chart(px.bar(factors.head(8), x='importance', y='factor', orientation='h', title="Top Readmission Risk Factors"), use_container_width=True)
st.plotly_chart(px.histogram(df, x='risk_score', color='readmitted_30d', title="Risk Score Distribution"), use_container_width=True)
st.plotly_chart(px.scatter(df, x='length_of_stay', y='comorbidity_count', color='risk_score', size='age', title="LOS vs Comorbidity (color=risk)"), use_container_width=True)
st.dataframe(cost)
st.success(f"Recommendation: {cost['scenario'].values[0]} → Saves ${cost['net_savings'].values[0]:,} with ROI {cost['roi'].values[0]}x")
