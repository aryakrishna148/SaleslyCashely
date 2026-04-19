# 📊 SAP O2C Data Analytics Project

> **Order-to-Cash (O2C) Process Analytics** — A complete data analytics project built on SAP SD (Sales & Distribution) data covering all major analytics disciplines.

---

## 📌 Overview

This project analyzes the **Order-to-Cash (O2C)** business process using SAP SD concepts and data analytics techniques. It covers the entire O2C cycle from customer inquiry to payment collection, applying real-world analytics methods to derive business insights.

## 🔄 O2C Process Flow

```
Inquiry (VA11) → Quotation (VA21) → Sales Order (VA01) → Delivery (VL01N) → Billing (VF01) → Payment (F-28)
```

## 🎯 Objectives

- Simulate the O2C business process using SAP SD transaction data
- Apply all major data analytics techniques on real business data
- Generate actionable business insights for decision-making
- Build an interactive analytics dashboard (web app)

## 📚 Analytics Topics Covered

| Topic | Techniques Used |
|---|---|
| **Descriptive Analytics** | KPIs, revenue trends, monthly/quarterly analysis, delivery rates |
| **Diagnostic Analytics** | Root cause analysis, delay patterns, cancellation trends |
| **Predictive Analytics** | Linear Regression forecast, model evaluation (R², MAE, RMSE) |
| **Customer Segmentation** | RFM Analysis (Recency, Frequency, Monetary) |
| **Anomaly Detection** | Z-Score method, outlier identification |
| **Data Visualization** | Line, bar, pie, scatter, histogram charts |

## 🛠 Tools & Technologies

- **Python** — Pandas, NumPy, Matplotlib, Scikit-learn, SciPy
- **Streamlit** — Interactive web dashboard
- **Jupyter Notebook** — Step-by-step analysis
- **SAP SD** — Order-to-Cash process (conceptual + T-codes)

## 🗂 Project Structure

```
O2C-Data-Analytics/
├── app.py                  ← Streamlit web dashboard
├── README.md
├── requirements.txt
├── data/
│   ├── sales_data.csv      ← 500-record SAP O2C dataset
│   └── generate_data.py    ← Dataset generator script
├── notebooks/
│   └── analysis.ipynb      ← Full Jupyter analysis notebook
├── scripts/
│   └── analysis.py         ← Python analysis script (all topics)
├── visuals/
│   ├── 00_dashboard.png
│   ├── 01_descriptive_analytics.png
│   ├── 02_diagnostic_analytics.png
│   ├── 03_rfm_segmentation.png
│   ├── 04_predictive_analytics.png
│   └── 05_anomaly_detection.png
└── report/
    └── (add your final PDF report here)
```

## 📊 Dataset

The dataset (`data/sales_data.csv`) contains **500 SAP-style sales transaction records** with:

| Column | Description |
|---|---|
| Order_ID | Unique sales order number (SO-XXXX) |
| SAP_Doc_No | SAP document number |
| Customer | Customer name |
| Product | Product category |
| Region | Sales region (North/South/East/West) |
| Quantity | Units ordered |
| Unit_Price | Price per unit |
| Revenue / Net_Revenue | Gross and net revenue (after discount) |
| Order_Date / Delivery_Date | Dates |
| Delivery_Days | Days taken for delivery |
| Payment_Terms | Net30 / Net45 / Net60 / Immediate |
| Status | Delivered / Pending / Cancelled |
| On_Time | Yes / No |

## 📈 Key Results

- **Total Revenue**: ₹1.8 Cr across 500 orders
- **On-Time Delivery Rate**: ~82% (target: 85%)
- **Top Product**: Laptop (highest revenue share)
- **Revenue Forecast**: +15% growth predicted for H1 2025 (R² = 0.91)
- **Anomalies Detected**: 2.9% of orders flagged via Z-score
- **Champion Customers**: Identified top-tier customers via RFM scoring

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate dataset (if needed)
```bash
cd data
python generate_data.py
```

### 3. Run analysis script
```bash
cd scripts
python analysis.py
```

### 4. Open Jupyter notebook
```bash
jupyter notebook notebooks/analysis.ipynb
```

### 5. Launch web dashboard
```bash
streamlit run app.py
```

## 📋 SAP SD Transaction Codes Reference

| T-Code | Description |
|---|---|
| VA11 | Create Inquiry |
| VA21 | Create Quotation |
| VA01 / VA02 / VA03 | Create / Change / Display Sales Order |
| VL01N / VL02N | Create / Change Outbound Delivery |
| VF01 / VF02 / VF03 | Create / Change / Display Billing Document |
| F-28 | Post Incoming Payment |
| FBL5N | Customer Line Item Display |
| MB51 | Material Document List |

## 📌 Conclusion

Data analytics applied to the SAP O2C process helps organizations:
- Identify revenue trends and forecast future performance
- Detect and resolve delivery bottlenecks
- Segment customers for targeted strategies
- Flag anomalous transactions before they become issues

---

*Project submitted as part of [Your Course Name] | [Your College Name] | [Year]*
