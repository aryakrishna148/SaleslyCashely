# SAC Connection Setup Guide

## Option A — Live Data Connection (S/4HANA HANA Views) ★ Recommended

1. Open SAC → Main Menu (hamburger) → **Connections** → **Add Connection**
2. Select: **SAP S/4HANA**
3. Fill in the details:
   - Connection Name: `O2C_S4H_LIVE`
   - Host: `your-s4hana-host.domain.com`
   - HTTPS Port: `443`
   - SAP Client: `100` (your client number)
   - Authentication: SSO (recommended) or Basic Auth
4. Click **OK** → **Test Connection** → should show green
5. In **Modeler**, create a new model → choose this connection
6. Select view `ZVO2CANALYTICS` (the SQL view name of the CDS view)

**Advantage:** Real-time data, no scheduling needed.


## Option B — Import Connection via CSV (BTP Pipeline)

1. Run the pipeline script to generate sample data:
   ```bash
   pip install pandas
   python scripts/btp_pipeline.py
   ```
   This creates:
   - `data/o2c_transactions.csv`
   - `data/o2c_rfm.csv`
   - `data/o2c_anomalies.csv`

2. In SAC → **Connections** → **Add Connection** → **File / Local**
3. Upload `data/o2c_transactions.csv`
4. Map columns as per `sac_model/model_config.json`
5. Schedule daily refresh via BTP Data Intelligence pipeline

**Advantage:** Works without direct HANA network access.


## Option C — SAP BW/BEx Connection

1. In SAC → Connections → Add Connection → **SAP BW**
2. Enter your BW system host, system number, client
3. Activate these ODP DataSources in transaction `LBWE`:
   - `2LIS_11_VAHDR` — Sales Order Header
   - `2LIS_12_VCITM` — Delivery Items
   - `2LIS_13_VDHDR` — Billing Header
4. Load to BW InfoCube `ZO2C_CUBE`
5. In SAC Modeler, select this InfoCube as the data source


## SAP Authorization Objects Required

Ensure your RFC/communication user has:

| Auth Object | Field       | Value             |
|-------------|-------------|-------------------|
| S_TABU_DIS  | ACTVT       | 03 (Display)      |
| S_TABU_DIS  | DICBERCLS   | SD, FI, MM tables |
| S_RS_COMP   | RSINFOAREA  | ZO2C (your area)  |
| S_CARRID    | (not needed for SD) |               |

Transaction `SU53` can show authorization failures for your RFC user.


## Roles and Data Access Control in SAC

Create roles in **SAC Admin → Roles**:

| Role Name     | Permissions                              |
|---------------|------------------------------------------|
| O2C_Viewer    | Read-only story access                   |
| O2C_Analyst   | Edit models and stories                  |
| O2C_Admin     | Full access including connections        |

Set up **Data Access Control** in the model to filter Region by user:
- In Modeler → your model → Data Access Control
- Map the `Region` dimension to a user attribute
- Assign users to regions so North users only see North data
