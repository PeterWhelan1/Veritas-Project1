import pandas as pd
import plotly.express as px
from pathlib import Path

CSV_FILE = Path("submissions.csv")

if not CSV_FILE.exists():
    raise SystemExit("❌ Couldn't find submissions.csv — export your Formspree data first.")

df = pd.read_csv(CSV_FILE)

# Ensure correct columns
cols = ['present_a','present_b','present_c','future_a','future_b','future_c']
for col in cols:
    if col not in df.columns:
        raise SystemExit(f"Missing column: {col}")
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=cols)

# Normalise (handle rounding errors)
for prefix in ['present','future']:
    s = df[f'{prefix}_a'] + df[f'{prefix}_b'] + df[f'{prefix}_c']
    s = s.replace(0, 1)
    for c in ['a','b','c']:
        df[f'{prefix}_{c}'] = df[f'{prefix}_{c}'] / s

# Plot Present
fig1 = px.scatter_ternary(
    df, a='present_a', b='present_b', c='present_c',
    title='Veritas AI — Present (2025) Values'
)
fig1.update_traces(marker=dict(size=6, opacity=0.8))
fig1.write_html('present_aggregate.html', include_plotlyjs='cdn')

# Plot Future
fig2 = px.scatter_ternary(
    df, a='future_a', b='future_b', c='future_c',
    title='Veritas AI — Future (2075) Values'
)
fig2.update_traces(marker=dict(size=6, opacity=0.8))
fig2.write_html('future_aggregate.html', include_plotlyjs='cdn')

# Save dataset for report appendix
df.to_excel('veritas_values_dataset.xlsx', index=False)
print("✅ Created: present_aggregate.html, future_aggregate.html, veritas_values_dataset.xlsx")
