# SAP O2C SAC Implementation Checklist

## Phase 1 — SAP Backend (SAP GUI / Eclipse ADT)
- [ ] Open Eclipse ADT and connect to your S/4HANA system
- [ ] Create CDS view `ZV_O2C_ANALYTICS` (paste from cds_views/ZV_O2C_ANALYTICS.abap)
- [ ] Create CDS view `ZV_O2C_RFM` (paste from cds_views/ZV_O2C_RFM.abap)
- [ ] Activate both CDS views (Ctrl+F3 in ADT)
- [ ] Test views in SE16N: enter view name `ZVO2CANALYTICS`, press F8
- [ ] Grant RFC user access: SU01 → assign role with S_TABU_DIS on SD tables

## Phase 2 — SAP Analytics Cloud Connection
- [ ] Log into your SAC tenant
- [ ] Main Menu → Connections → Add Connection → SAP S/4HANA (or BW / File)
- [ ] Enter host, port, client, credentials
- [ ] Test connection successfully
- [ ] Note the connection name for use in Modeler

## Phase 3 — SAC Data Model
- [ ] Modeler → New Model → New Model from Data Source
- [ ] Select your connection and view `ZVO2CANALYTICS`
- [ ] Add all dimensions from model_config.json
- [ ] Add measures: NetValue, OrderQuantity, DeliveryDays, OrderToBillCycleDays
- [ ] Add calculated measure: OnTimeDeliveryRate
- [ ] Add calculated measure: CancellationRate
- [ ] Add calculated measure: RevenuePerOrder
- [ ] Add calculated dimension: RFM_Segment
- [ ] Add calculated dimension: DeliveryBucket
- [ ] Set date hierarchy on OrderDate: Year > Quarter > Month > Day
- [ ] Save and publish model

## Phase 4 — SAC Story (Dashboard)
- [ ] Stories → New Story → Responsive Page
- [ ] Page 1 (O2C Overview):
  - [ ] 4 Numeric Point KPI tiles (Revenue, On-Time %, Delivery Days, Cancellation Rate)
  - [ ] Line chart: Monthly Revenue Trend
  - [ ] Bar chart: Revenue by Region
  - [ ] Donut chart: Order Status Split
- [ ] Page 2 (Delivery Analytics):
  - [ ] Bar chart: Orders by Delivery Speed (DeliveryBucket)
  - [ ] Scatter chart: Delivery Days vs Revenue
  - [ ] Waterfall: On-Time % by Region
- [ ] Page 3 (Customer Segmentation):
  - [ ] Create second model from ZV_O2C_RFM
  - [ ] Bubble/Scatter: X=RecencyDays, Y=OrderFrequency, Size=TotalRevenue, Color=RFM_Segment
  - [ ] Table: Customer RFM scores
- [ ] Page 4 (Predictive Forecast):
  - [ ] Predictive Scenarios → New → Time Series Forecast
  - [ ] Set target=NetValue, time=OrderDate, horizon=6 months
  - [ ] Add forecast line chart to story with confidence band
- [ ] Page 5 (Anomaly Detection):
  - [ ] Add Revenue scatter chart
  - [ ] Right-click → Smart Insights → Find Outliers on NetValue
  - [ ] Add table of flagged orders

## Phase 5 — Filters and Global Controls
- [ ] Add Input Control: Date Range (OrderDate)
- [ ] Add Input Control: Multi-Select Region
- [ ] Add Input Control: Multi-Select Product/Material
- [ ] Add Input Control: Multi-Select Order Status
- [ ] Link all charts to global filters

## Phase 6 — Deploy and Share
- [ ] Apply Morning Horizon (or corporate) theme
- [ ] Share story → assign O2C_Viewer role
- [ ] Set data refresh schedule (if Import connection)
- [ ] Test on SAC mobile app
- [ ] Export to PDF/PowerPoint for offline reporting

## SAP T-Codes Reference
| T-Code       | Purpose                                |
|--------------|----------------------------------------|
| SE11 / ADT   | Create and activate CDS views          |
| VA01/02/03   | Sales order create/change/display      |
| VL01N/VL02N  | Delivery create/change                 |
| VF01/02/03   | Billing create/change/display          |
| F-28         | Post incoming payment                  |
| FBL5N        | Customer line item display             |
| LBWE         | Activate ODP extractors for BW         |
| SU01         | User maintenance (RFC user setup)      |
| SU53         | Authorization failure check            |
| SE16N        | Table/view data browser                |
