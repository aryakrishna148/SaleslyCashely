"""
SAP BTP Data Pipeline
Replicates O2C data from S/4HANA to SAC Import Connection.
Run on SAP Data Intelligence / BTP Data Pipelines or locally.

Usage:
    pip install pandas
    python btp_pipeline.py
"""

import pandas as pd
import random
from datetime import datetime, timedelta


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — SAP HANA CONNECTION (replace stub in production)
# ─────────────────────────────────────────────────────────────────────────────

def pull_from_sap_hana(view_name: str) -> pd.DataFrame:
    """
    Pull data from SAP HANA CDS view.

    In production, replace this function body with:

        from hdbcli import dbapi
        conn = dbapi.connect(
            address  = 'your-hana-host.domain.com',
            port     = 443,
            user     = 'YOUR_RFC_USER',
            password = 'YOUR_PASSWORD',
            encrypt  = True,
            sslValidateCertificate = False
        )
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM "_SYS_BIC"."{view_name}"')
        cols = [d[0] for d in cursor.description]
        df   = pd.DataFrame(cursor.fetchall(), columns=cols)
        conn.close()
        return df

    For SAP ECC via RFC (PyRFC):

        import pyrfc
        conn = pyrfc.Connection(ashost='host', sysnr='00', client='100',
                                user='USER', passwd='PASS')
        result = conn.call('RFC_READ_TABLE', QUERY_TABLE='VBAK', ...)
        ...
    """
    print(f"[INFO] Simulating pull from view: {view_name} (replace with real HANA connection)")
    return _generate_o2c_sample(500)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — SAMPLE DATA GENERATOR (mirrors ZV_O2C_ANALYTICS columns)
# ─────────────────────────────────────────────────────────────────────────────

def _generate_o2c_sample(n: int = 500) -> pd.DataFrame:
    random.seed(42)
    customers  = ["TATA001","INFY002","WIPR003","MAHI004","HCL005",
                  "RELI006","BAJA007","HERO008","MARU009","ASIA010"]
    cust_names = ["Tata Motors","Infosys Ltd","Wipro Tech","Mahindra & Mahindra","HCL Systems",
                  "Reliance Ind","Bajaj Auto","Hero MotoCorp","Maruti Suzuki","Asian Paints"]
    materials  = ["MAT-LAPT","MAT-MOBL","MAT-TABL","MAT-MNTR","MAT-PRNT"]
    mat_desc   = ["Laptop","Mobile Phone","Tablet","Monitor","Printer"]
    regions    = ["North","South","East","West"]
    sales_orgs = ["1000","2000","3000","4000"]
    pay_map    = {"Z030":"Net30","Z045":"Net45","Z060":"Net60","SOFO":"Immediate"}
    statuses   = ["A","B","C"]          # A=Open, B=Delivered, C=Cancelled
    base       = datetime(2024, 1, 1)

    rows = []
    for i in range(1, n + 1):
        ci = random.randint(0, 9)
        mi = random.randint(0, 4)
        ri = random.randint(0, 3)
        pt = random.choice(list(pay_map.keys()))
        order_date    = base + timedelta(days=random.randint(0, 364))
        delivery_days = random.randint(1, 15)
        delivery_date = order_date + timedelta(days=delivery_days)
        billing_date  = delivery_date + timedelta(days=random.randint(1, 10))
        qty    = random.randint(1, 50)
        price  = random.randint(500, 80000)
        net    = round(qty * price * (1 - random.uniform(0, 0.15)))
        status = random.choices(statuses, weights=[10, 75, 15])[0]
        on_time = "Y" if (delivery_days <= 7 and status == "B") else (
                  "Y" if random.random() > 0.18 else "N")

        rows.append({
            "SalesOrder":           f"50{1000 + i:05d}",
            "SalesOrderItem":       "000010",
            "CustomerID":           customers[ci],
            "CustomerName":         cust_names[ci],
            "Region":               regions[ri],
            "Country":              "IN",
            "Material":             materials[mi],
            "MaterialDescription":  mat_desc[mi],
            "OrderQuantity":        qty,
            "UnitPrice":            price,
            "NetValue":             net,
            "Currency":             "INR",
            "SalesOrg":             sales_orgs[random.randint(0, 3)],
            "PaymentTerms":         pay_map[pt],
            "OrderDate":            order_date.strftime("%Y-%m-%d"),
            "ActualDeliveryDate":   delivery_date.strftime("%Y-%m-%d"),
            "BillingDate":          billing_date.strftime("%Y-%m-%d"),
            "DeliveryDays":         delivery_days,
            "OverallStatus":        status,
            "OnTimeDelivery":       on_time,
            "OrderToBillCycleDays": (billing_date - order_date).days,
        })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — RFM COMPUTATION
# ─────────────────────────────────────────────────────────────────────────────

def compute_rfm(df: pd.DataFrame, reference_date: str = "2025-01-01") -> pd.DataFrame:
    ref = pd.to_datetime(reference_date)
    delivered = df[df["OverallStatus"] == "B"].copy()
    delivered["OrderDate"] = pd.to_datetime(delivered["OrderDate"])

    rfm = delivered.groupby(["CustomerID", "CustomerName", "Region"]).agg(
        RecencyDays    = ("OrderDate",   lambda x: (ref - x.max()).days),
        OrderFrequency = ("SalesOrder",  "nunique"),
        TotalRevenue   = ("NetValue",    "sum"),
        AvgOrderValue  = ("NetValue",    "mean"),
    ).reset_index()

    rfm["R_Score"] = pd.qcut(rfm["RecencyDays"],
                              q=3, labels=[3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["OrderFrequency"].rank(method="first"),
                              q=3, labels=[1, 2, 3]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["TotalRevenue"].rank(method="first"),
                              q=3, labels=[1, 2, 3]).astype(int)
    rfm["RFM_Total"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

    def segment(row):
        t = row["RFM_Total"]
        if t >= 8: return "Champion"
        if t >= 6: return "Loyal Customer"
        if t >= 5: return "Potential Loyalist"
        return "At Risk"

    rfm["CustomerSegment"] = rfm.apply(segment, axis=1)
    rfm["AvgOrderValue"]   = rfm["AvgOrderValue"].round(2)
    rfm["TotalRevenue"]    = rfm["TotalRevenue"].round(2)
    return rfm


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — ANOMALY DETECTION (Z-Score)
# ─────────────────────────────────────────────────────────────────────────────

def detect_anomalies(df: pd.DataFrame, z_threshold: float = 2.5) -> pd.DataFrame:
    mean = df["NetValue"].mean()
    std  = df["NetValue"].std()
    tmp  = df.copy()
    tmp["ZScore"]    = ((tmp["NetValue"] - mean) / std).abs().round(3)
    tmp["IsAnomaly"] = tmp["ZScore"] > z_threshold
    anomalies = tmp[tmp["IsAnomaly"]][
        ["SalesOrder", "CustomerName", "MaterialDescription",
         "Region", "NetValue", "ZScore", "OverallStatus", "OrderDate"]
    ].sort_values("ZScore", ascending=False)
    return anomalies


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — EXPORT FOR SAC IMPORT CONNECTION
# ─────────────────────────────────────────────────────────────────────────────

def export_for_sac(df: pd.DataFrame, rfm: pd.DataFrame, anomalies: pd.DataFrame, out_dir: str = "data"):
    df.to_csv(f"{out_dir}/o2c_transactions.csv",  index=False)
    rfm.to_csv(f"{out_dir}/o2c_rfm.csv",          index=False)
    anomalies.to_csv(f"{out_dir}/o2c_anomalies.csv", index=False)
    print(f"[OK] o2c_transactions.csv  — {len(df)} rows")
    print(f"[OK] o2c_rfm.csv           — {len(rfm)} customers")
    print(f"[OK] o2c_anomalies.csv     — {len(anomalies)} flagged orders")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  SAP O2C BTP Data Pipeline")
    print("=" * 50)

    df        = pull_from_sap_hana("ZV_O2C_ANALYTICS")
    rfm       = compute_rfm(df)
    anomalies = detect_anomalies(df)
    export_for_sac(df, rfm, anomalies)

    print("\nUpload the CSV files from the data/ folder to SAC via:")
    print("  SAC > Connections > Add Connection > File / Local")
    print("  Then create your model from the uploaded dataset.")
