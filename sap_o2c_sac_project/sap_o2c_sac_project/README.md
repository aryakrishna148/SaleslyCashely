# SAP O2C Analytics — SAP Analytics Cloud Project

## Overview

Complete implementation kit for building an **Order-to-Cash (O2C) analytics dashboard**
in **SAP Analytics Cloud (SAC)**, connected to SAP S/4HANA or ECC via Live Data
Connection or BTP Import Pipeline.

O2C Flow:
  Inquiry (VA11) → Quotation (VA21) → Sales Order (VA01) → Delivery (VL01N) → Billing (VF01) → Payment (F-28)

---

## Folder Structure

```
sap_o2c_sac_project/
├── README.md
├── cds_views/
│   ├── ZV_O2C_ANALYTICS.abap      ← Main O2C CDS view (deploy in SAP ADT)
│   └── ZV_O2C_RFM.abap            ← RFM customer segmentation view
├── sac_model/
│   └── model_config.json          ← SAC model: dimensions, measures, formulas
├── sac_story/
│   └── story_layout.json          ← 5-page story and widget layout spec
├── scripts/
│   └── btp_pipeline.py            ← BTP pipeline + sample data generator
├── data/
│   ├── o2c_transactions.csv       ← 500 SAP-style O2C records
│   ├── o2c_rfm.csv                ← Customer RFM scores
│   └── o2c_anomalies.csv          ← Z-score flagged anomalous orders
└── docs/
    ├── SAC_Connection_Setup.md    ← Step-by-step connection guide
    └── Implementation_Checklist.md
```

---

## Quick Start

### Step 1 — Deploy CDS Views (Eclipse ADT)
Open Eclipse ADT, create a new Data Definition, paste `ZV_O2C_ANALYTICS.abap`, activate with Ctrl+F3. Repeat for `ZV_O2C_RFM.abap`.

### Step 2 — Connect SAC to S/4HANA
Follow `docs/SAC_Connection_Setup.md`. Three options: Live (real-time), CSV Import, or BW.

### Step 3 — Build SAC Model
Use `sac_model/model_config.json` as specification in SAC Modeler.

### Step 4 — Build SAC Story (5 pages)
Use `sac_story/story_layout.json` as blueprint in SAC Stories.

### Step 5 — Generate Sample CSV Data
```bash
pip install pandas
python scripts/btp_pipeline.py
```

---

## Analytics Modules

| Module               | SAC Feature                    | Story Page |
|----------------------|--------------------------------|------------|
| Descriptive KPIs     | Numeric Point, Line chart      | P01        |
| Delivery Analysis    | Waterfall, Scatter, Bar        | P02        |
| RFM Segmentation     | Bubble chart, Table            | P03        |
| Revenue Forecast     | Smart Predict - Time Series    | P04        |
| Anomaly Detection    | Smart Insights - Find Outliers | P05        |

---

## SAP T-Codes Referenced

| T-Code     | Description                       |
|------------|-----------------------------------|
| VA01/02/03 | Sales Order create/change/display |
| VL01N      | Create Outbound Delivery          |
| VF01       | Create Billing Document           |
| F-28       | Post Incoming Payment             |
| FBL5N      | Customer Line Item Display        |
| SE11 / ADT | CDS View Development              |
| LBWE       | ODP Extractor Activation (BW)     |

---

*SAP O2C Analytics | SAP Analytics Cloud | S4HANA SD | 2024*
