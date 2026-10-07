import pandas as pd
import numpy as np
import json

# ---- Step 1: Load ----
df = pd.read_csv("online_retail.csv", encoding="latin1")
print("Raw rows:", len(df))

# ---- Step 2: Clean ----
df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]
df = df.drop_duplicates()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["CustomerID"] = df["CustomerID"].astype(int)
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

print("After cleaning:", len(df), "rows |", df["CustomerID"].nunique(), "unique customers")

# ---- Step 3: RFM metrics ----
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalPrice", "sum")
).reset_index()

# ---- Step 4: Scoring ----
rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1,2,3,4,5]).astype(int)
rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

# ---- Step 5: Segment ----
def segment(row):
    if row["RFM_Score"] >= 13:
        return "Champions"
    elif row["RFM_Score"] >= 10:
        return "Loyal Customers"
    elif row["R_Score"] >= 4 and row["F_Score"] <= 2:
        return "New Customers"
    elif row["R_Score"] <= 2 and row["RFM_Score"] >= 7:
        return "At Risk"
    elif row["R_Score"] <= 2:
        return "Lost Customers"
    else:
        return "Occasional"

rfm["Segment"] = rfm.apply(segment, axis=1)
rfm.to_csv("rfm_customer_segments.csv", index=False)

# ---- Step 6: Summary for dashboard ----
seg_summary = rfm.groupby("Segment").agg(
    Customers=("CustomerID","count"),
    AvgRecency=("Recency","mean"),
    AvgFrequency=("Frequency","mean"),
    AvgMonetary=("Monetary","mean")
).round(1)

summary = {
    "total_customers": int(rfm.shape[0]),
    "total_orders": int(df["InvoiceNo"].nunique()),
    "total_revenue": round(df["TotalPrice"].sum(),2),
    "avg_order_value": round(df["TotalPrice"].sum() / df["InvoiceNo"].nunique(), 2),
    "segment_counts": rfm["Segment"].value_counts().to_dict(),
    "segment_summary": {
        seg: {"customers": int(row["Customers"]), "avg_recency": row["AvgRecency"],
              "avg_frequency": row["AvgFrequency"], "avg_monetary": row["AvgMonetary"]}
        for seg, row in seg_summary.iterrows()
    },
    "scatter_points": [
        {"recency": int(r.Recency), "monetary": round(r.Monetary,2), "segment": r.Segment}
        for r in rfm.itertuples()
    ]
}

with open("summary.json","w") as f:
    json.dump(summary, f, indent=2)

print("Total Revenue:", summary["total_revenue"])
print("Total Customers:", summary["total_customers"])