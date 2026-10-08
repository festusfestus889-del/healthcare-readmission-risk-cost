import pandas as pd

df = pd.read_csv("data/processed/patients_risk.csv")

# Cost analysis
avg_cost_readmitted = df[df.readmitted_30d==True]['cost_usd'].mean()
avg_cost_not = df[df.readmitted_30d==False]['cost_usd'].mean()
extra_cost_per_readmission = avg_cost_readmitted - avg_cost_not

print(f"Cost if readmitted: ${avg_cost_readmitted:.0f} vs ${avg_cost_not:.0f} = extra ${extra_cost_per_readmission:.0f}")

# What-if: Target top 20% high-risk with intervention (assume 40% reduction in readmission)
df_sorted = df.sort_values('risk_score', ascending=False)
top_20_pct = df_sorted.head(int(len(df)*0.2))
baseline_readmissions = top_20_pct['readmitted_30d'].sum()
prevented = int(baseline_readmissions * 0.4) # intervention works 40%
savings = prevented * extra_cost_per_readmission
intervention_cost = len(top_20_pct)*200 # $200 per patient program

result = pd.DataFrame([{
  'scenario': 'Target high-risk 20% with care management',
  'patients_targeted': len(top_20_pct),
  'baseline_readmissions_in_group': int(baseline_readmissions),
  'prevented_readmissions': prevented,
  'gross_savings': int(savings),
  'intervention_cost': int(intervention_cost),
  'net_savings': int(savings-intervention_cost),
  'roi': round((savings-intervention_cost)/intervention_cost,2)
}])

result.to_csv("data/processed/cost_impact.csv", index=False)
print(result.to_string(index=False))
print(f"\nNET SAVINGS: ${result['net_savings'].values[0]:,} per 5000 patients cohort")
