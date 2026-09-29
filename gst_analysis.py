import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "gst_invoice_data.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["Date"])

print("GST Invoice & Tax Analysis")
print("=" * 30)
print(f"Total invoices : {len(df)}")
print(f"Taxable value  : ₹{df['Taxable_Value'].sum():,.2f}")
print(f"Total GST      : ₹{df['GST_Amount'].sum():,.2f}")
print(f"Invoice total  : ₹{df['Invoice_Total'].sum():,.2f}")
print(f"CGST           : ₹{df['CGST'].sum():,.2f}")
print(f"SGST           : ₹{df['SGST'].sum():,.2f}")
print(f"IGST           : ₹{df['IGST'].sum():,.2f}")

# Monthly GST
monthly = df.groupby("Month", as_index=False)[["Taxable_Value","GST_Amount"]].sum()
ax = monthly.set_index("Month")[["Taxable_Value","GST_Amount"]].plot(kind="bar", figsize=(9,5))
ax.set_title("Monthly Taxable Value and GST")
ax.set_xlabel("Month")
ax.set_ylabel("Amount (₹)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUT/"monthly_gst_analysis.png", dpi=160)
plt.close()

# GST by product category
category = df.groupby("Category", as_index=False)["GST_Amount"].sum().sort_values("GST_Amount", ascending=False)
ax = category.plot(x="Category", y="GST_Amount", kind="bar", figsize=(8,5), legend=False)
ax.set_title("GST by Category")
ax.set_xlabel("Category")
ax.set_ylabel("GST (₹)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUT/"gst_by_category.png", dpi=160)
plt.close()

# Tax component
components = pd.Series({
    "CGST": df["CGST"].sum(),
    "SGST": df["SGST"].sum(),
    "IGST": df["IGST"].sum()
})
ax = components.plot(kind="bar", figsize=(7,5))
ax.set_title("GST Component Summary")
ax.set_xlabel("Tax Component")
ax.set_ylabel("Amount (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT/"gst_components.png", dpi=160)
plt.close()

# Intra vs inter-state
supply = df.groupby("Supply_Type", as_index=False)["GST_Amount"].sum()
ax = supply.plot(x="Supply_Type", y="GST_Amount", kind="bar", figsize=(7,5), legend=False)
ax.set_title("GST by Supply Type")
ax.set_xlabel("Supply Type")
ax.set_ylabel("GST (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT/"gst_by_supply_type.png", dpi=160)
plt.close()

summary = pd.DataFrame({
    "Metric": ["Number of Invoices","Taxable Value","Total GST","Invoice Total","CGST","SGST","IGST"],
    "Value": [
        len(df), round(df["Taxable_Value"].sum(),2), round(df["GST_Amount"].sum(),2),
        round(df["Invoice_Total"].sum(),2), round(df["CGST"].sum(),2),
        round(df["SGST"].sum(),2), round(df["IGST"].sum(),2)
    ]
})
summary.to_csv(OUT/"tax_summary.csv", index=False)
print("\nAnalysis complete. Check the outputs folder.")
