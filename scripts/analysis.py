"""
SAP O2C Data Analytics Project
================================
Covers: Descriptive, Diagnostic, Predictive Analytics,
        Customer Segmentation (RFM), Anomaly Detection,
        Data Visualization
Author: [Your Name]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#F8F9FA',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'font.size': 10,
})

# ─────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────
df = pd.read_csv('../data/sales_data.csv', parse_dates=['Order_Date', 'Delivery_Date'])
df['Month']   = df['Order_Date'].dt.month
df['Quarter'] = df['Order_Date'].dt.quarter
df['MonthName'] = df['Order_Date'].dt.strftime('%b')

print("=" * 55)
print("  SAP O2C DATA ANALYTICS PROJECT")
print("=" * 55)
print(f"\nDataset shape: {df.shape}")
print(f"Date range:    {df['Order_Date'].min().date()} → {df['Order_Date'].max().date()}")
print(f"\nColumns: {list(df.columns)}")


# ─────────────────────────────────────────
# 2. DESCRIPTIVE ANALYTICS
# ─────────────────────────────────────────
print("\n\n── DESCRIPTIVE ANALYTICS ──────────────────────")
print(f"Total Revenue    : ₹{df['Net_Revenue'].sum():,.0f}")
print(f"Total Orders     : {len(df):,}")
print(f"Avg Order Value  : ₹{df['Net_Revenue'].mean():,.0f}")
print(f"Avg Delivery Days: {df['Delivery_Days'].mean():.1f}")
print(f"On-Time Rate     : {(df['On_Time']=='Yes').mean()*100:.1f}%")
print(f"\nStatus breakdown:\n{df['Status'].value_counts()}")

monthly_rev = df.groupby('Month')['Net_Revenue'].sum() / 1e5

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
fig.suptitle('SAP O2C – Descriptive Analytics', fontsize=14, fontweight='bold', y=1.01)

# Monthly revenue trend
ax = axes[0, 0]
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
rev_by_month = [df[df['Month']==m]['Net_Revenue'].sum()/1e5 for m in range(1,13)]
ax.plot(months, rev_by_month, 'o-', color='#185FA5', linewidth=2, markersize=5)
ax.fill_between(months, rev_by_month, alpha=0.15, color='#185FA5')
ax.set_title('Monthly Revenue Trend (₹ Lakhs)', fontweight='bold')
ax.set_ylabel('Revenue (Lakhs)')
ax.tick_params(axis='x', rotation=45)

# Revenue by product
ax = axes[0, 1]
prod_rev = df.groupby('Product')['Net_Revenue'].sum() / 1e5
colors = ['#185FA5','#1D9E75','#BA7517','#D85A30','#534AB7']
prod_rev.sort_values().plot(kind='barh', ax=ax, color=colors)
ax.set_title('Revenue by Product (₹ Lakhs)', fontweight='bold')
ax.set_xlabel('Revenue (Lakhs)')

# Order status pie
ax = axes[0, 2]
status_counts = df['Status'].value_counts()
ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%',
       colors=['#1D9E75','#BA7517','#D85A30'], startangle=90)
ax.set_title('Order Status Distribution', fontweight='bold')

# Revenue by region
ax = axes[1, 0]
region_rev = df.groupby('Region')['Net_Revenue'].sum() / 1e5
region_rev.plot(kind='bar', ax=ax, color='#534AB7', edgecolor='white')
ax.set_title('Revenue by Region (₹ Lakhs)', fontweight='bold')
ax.set_ylabel('Revenue (Lakhs)')
ax.tick_params(axis='x', rotation=0)

# Delivery performance
ax = axes[1, 1]
ontime_by_month = [
    (df[df['Month']==m]['On_Time']=='Yes').mean()*100
    for m in range(1,13)
]
ax.bar(months, ontime_by_month, color='#1D9E75', edgecolor='white')
ax.axhline(85, color='red', linestyle='--', linewidth=1, label='Target 85%')
ax.set_title('On-Time Delivery % by Month', fontweight='bold')
ax.set_ylabel('%')
ax.tick_params(axis='x', rotation=45)
ax.legend()

# Revenue by quarter
ax = axes[1, 2]
q_rev = df.groupby('Quarter')['Net_Revenue'].sum() / 1e5
q_rev.plot(kind='bar', ax=ax, color=['#185FA5','#1D9E75','#BA7517','#D85A30'], edgecolor='white')
ax.set_title('Quarterly Revenue (₹ Lakhs)', fontweight='bold')
ax.set_xlabel('Quarter')
ax.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('../visuals/01_descriptive_analytics.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n[Saved] visuals/01_descriptive_analytics.png")


# ─────────────────────────────────────────
# 3. DIAGNOSTIC ANALYTICS
# ─────────────────────────────────────────
print("\n── DIAGNOSTIC ANALYTICS ───────────────────────")

# Why are deliveries delayed?
delayed = df[df['On_Time'] == 'No']
ontime  = df[df['On_Time'] == 'Yes']
print(f"Delayed orders : {len(delayed)} ({len(delayed)/len(df)*100:.1f}%)")
print(f"Delayed avg days: {delayed['Delivery_Days'].mean():.1f}")

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle('SAP O2C – Diagnostic Analytics', fontsize=14, fontweight='bold')

# Delivery days distribution
ax = axes[0, 0]
ax.hist(df[df['On_Time']=='Yes']['Delivery_Days'], bins=15, alpha=0.7,
        color='#1D9E75', label='On-Time')
ax.hist(df[df['On_Time']=='No']['Delivery_Days'], bins=15, alpha=0.7,
        color='#D85A30', label='Delayed')
ax.axvline(10, color='black', linestyle='--', linewidth=1, label='Threshold (10d)')
ax.set_title('Delivery Days Distribution', fontweight='bold')
ax.set_xlabel('Days')
ax.legend()

# Cancellation by product
ax = axes[0, 1]
cancel_by_prod = df[df['Status']=='Cancelled'].groupby('Product').size()
cancel_by_prod.plot(kind='bar', ax=ax, color='#D85A30', edgecolor='white')
ax.set_title('Cancellations by Product', fontweight='bold')
ax.tick_params(axis='x', rotation=30)

# Payment terms vs revenue
ax = axes[1, 0]
pay_rev = df.groupby('Payment_Terms')['Net_Revenue'].mean() / 1000
pay_rev.plot(kind='bar', ax=ax, color='#534AB7', edgecolor='white')
ax.set_title('Avg Revenue by Payment Terms (₹K)', fontweight='bold')
ax.tick_params(axis='x', rotation=30)

# Delay by region
ax = axes[1, 1]
delay_region = df.groupby('Region').apply(lambda x: (x['On_Time']=='No').mean()*100)
delay_region.plot(kind='bar', ax=ax, color='#BA7517', edgecolor='white')
ax.axhline(15, color='red', linestyle='--', linewidth=1, label='Avg delay rate')
ax.set_title('Delay Rate by Region (%)', fontweight='bold')
ax.tick_params(axis='x', rotation=0)
ax.legend()

plt.tight_layout()
plt.savefig('../visuals/02_diagnostic_analytics.png', dpi=150, bbox_inches='tight')
plt.close()
print("[Saved] visuals/02_diagnostic_analytics.png")


# ─────────────────────────────────────────
# 4. CUSTOMER SEGMENTATION (RFM)
# ─────────────────────────────────────────
print("\n── RFM CUSTOMER SEGMENTATION ──────────────────")

snapshot_date = df['Order_Date'].max() + pd.Timedelta(days=1)
rfm = df.groupby('Customer').agg(
    Recency   = ('Order_Date', lambda x: (snapshot_date - x.max()).days),
    Frequency = ('Order_ID',   'count'),
    Monetary  = ('Net_Revenue','sum')
).reset_index()

rfm['R_Score'] = pd.qcut(rfm['Recency'],   4, labels=[4,3,2,1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 4, labels=[1,2,3,4]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'],  4, labels=[1,2,3,4]).astype(int)
rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

def segment(score):
    if score >= 10: return 'Champion'
    elif score >= 8: return 'Loyal'
    elif score >= 6: return 'At-Risk'
    elif score >= 4: return 'New'
    else: return 'Lost'

rfm['Segment'] = rfm['RFM_Score'].apply(segment)
print(rfm[['Customer','Recency','Frequency','Monetary','RFM_Score','Segment']].to_string(index=False))

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('RFM Customer Segmentation', fontsize=14, fontweight='bold')

seg_colors = {'Champion':'#185FA5','Loyal':'#1D9E75','At-Risk':'#D85A30','New':'#534AB7','Lost':'#888780'}
seg_counts = rfm['Segment'].value_counts()

ax = axes[0]
ax.pie(seg_counts, labels=seg_counts.index, autopct='%1.1f%%',
       colors=[seg_colors[s] for s in seg_counts.index])
ax.set_title('Segment Distribution', fontweight='bold')

ax = axes[1]
seg_rev = rfm.groupby('Segment')['Monetary'].mean() / 1000
seg_rev.plot(kind='bar', ax=ax, color=[seg_colors.get(s,'gray') for s in seg_rev.index],
             edgecolor='white')
ax.set_title('Avg Monetary Value (₹K)', fontweight='bold')
ax.tick_params(axis='x', rotation=30)

ax = axes[2]
ax.scatter(rfm['Frequency'], rfm['Monetary']/1000,
           c=[list(seg_colors.values())[['Champion','Loyal','At-Risk','New','Lost'].index(s)]
              for s in rfm['Segment']],
           alpha=0.7, s=80, edgecolors='white', linewidth=0.5)
ax.set_xlabel('Frequency (orders)')
ax.set_ylabel('Monetary (₹K)')
ax.set_title('Frequency vs Monetary Scatter', fontweight='bold')

plt.tight_layout()
plt.savefig('../visuals/03_rfm_segmentation.png', dpi=150, bbox_inches='tight')
plt.close()
print("[Saved] visuals/03_rfm_segmentation.png")


# ─────────────────────────────────────────
# 5. PREDICTIVE ANALYTICS (LINEAR REGRESSION)
# ─────────────────────────────────────────
print("\n── PREDICTIVE ANALYTICS ───────────────────────")

monthly_data = df.groupby('Month')['Net_Revenue'].sum().reset_index()
monthly_data.columns = ['Month', 'Revenue']

X = monthly_data[['Month']].values
y = monthly_data['Revenue'].values

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

r2  = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)

print(f"R² Score : {r2:.4f}")
print(f"MAE      : ₹{mae:,.0f}")
print(f"RMSE     : ₹{rmse:,.0f}")

future_months = np.array([[13],[14],[15],[16],[17],[18]])
future_pred   = model.predict(future_months)
future_labels = ['Jan\'25','Feb\'25','Mar\'25','Apr\'25','May\'25','Jun\'25']

print("\nForecast:")
for lbl, val in zip(future_labels, future_pred):
    print(f"  {lbl}: ₹{val:,.0f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Predictive Analytics – Revenue Forecast', fontsize=14, fontweight='bold')

ax = axes[0]
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ax.bar(month_names, y/1e5, color='#185FA5', alpha=0.7, label='Actual', edgecolor='white')
ax.plot(month_names, y_pred/1e5, 'r--o', markersize=4, label='Regression line')
ax.set_title('Historical Revenue + Trend Line', fontweight='bold')
ax.set_ylabel('Revenue (Lakhs)')
ax.legend()
ax.tick_params(axis='x', rotation=45)

ax = axes[1]
all_labels = month_names + future_labels
all_actual = list(y/1e5) + [np.nan]*6
all_pred   = list(y_pred/1e5) + list(future_pred/1e5)
ax.plot(all_labels, all_actual, 'o-', color='#185FA5', label='Historical', linewidth=2)
ax.plot(all_labels, all_pred,   's--', color='#D85A30', label='Predicted', linewidth=2, markersize=4)
ax.axvline(x=11.5, color='gray', linestyle=':', linewidth=1)
ax.text(12, max(all_pred)/1.05, 'Forecast →', fontsize=9, color='#D85A30')
ax.set_title('6-Month Revenue Forecast', fontweight='bold')
ax.set_ylabel('Revenue (Lakhs)')
ax.legend()
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('../visuals/04_predictive_analytics.png', dpi=150, bbox_inches='tight')
plt.close()
print("[Saved] visuals/04_predictive_analytics.png")


# ─────────────────────────────────────────
# 6. ANOMALY DETECTION (Z-SCORE)
# ─────────────────────────────────────────
print("\n── ANOMALY DETECTION ──────────────────────────")

df['Z_Score'] = np.abs(stats.zscore(df['Net_Revenue']))
df['Anomaly'] = df['Z_Score'] > 2.5

anomalies = df[df['Anomaly']].copy()
print(f"Total anomalies detected: {len(anomalies)}")
print(f"Anomaly rate: {len(anomalies)/len(df)*100:.1f}%")
print(f"Revenue in anomalies: ₹{anomalies['Net_Revenue'].sum():,.0f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Anomaly Detection – Z-Score Method', fontsize=14, fontweight='bold')

ax = axes[0]
normal_rev = df[~df['Anomaly']]['Net_Revenue'] / 1000
anom_rev   = df[df['Anomaly']]['Net_Revenue'] / 1000
ax.scatter(range(len(normal_rev)), normal_rev.values, c='#185FA5', alpha=0.5,
           s=15, label='Normal')
ax.scatter(df[df['Anomaly']].index, anom_rev.values, c='#D85A30',
           s=60, label='Anomaly', zorder=5, marker='X')
ax.set_title('Order Revenue – Anomalies Highlighted', fontweight='bold')
ax.set_xlabel('Order Index')
ax.set_ylabel('Revenue (₹K)')
ax.legend()

ax = axes[1]
ax.hist(df['Z_Score'], bins=30, color='#534AB7', edgecolor='white', alpha=0.8)
ax.axvline(2.5, color='#D85A30', linestyle='--', linewidth=2, label='Threshold (Z=2.5)')
ax.set_title('Z-Score Distribution', fontweight='bold')
ax.set_xlabel('Z-Score')
ax.set_ylabel('Count')
ax.legend()

plt.tight_layout()
plt.savefig('../visuals/05_anomaly_detection.png', dpi=150, bbox_inches='tight')
plt.close()
print("[Saved] visuals/05_anomaly_detection.png")


# ─────────────────────────────────────────
# 7. COMBINED DASHBOARD CHART
# ─────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
fig.suptitle('SAP O2C Analytics – Complete Dashboard', fontsize=16, fontweight='bold', y=1.01)
gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.4, wspace=0.4)

ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(month_names, [df[df['Month']==m]['Net_Revenue'].sum()/1e5 for m in range(1,13)],
         'o-', color='#185FA5', linewidth=2)
ax1.fill_between(month_names,
                 [df[df['Month']==m]['Net_Revenue'].sum()/1e5 for m in range(1,13)],
                 alpha=0.12, color='#185FA5')
ax1.set_title('Monthly Revenue (₹L)', fontweight='bold')
ax1.tick_params(axis='x', rotation=45)

ax2 = fig.add_subplot(gs[0, 2])
prod_rev.plot(kind='bar', ax=ax2, color=colors, edgecolor='white')
ax2.set_title('By Product', fontweight='bold')
ax2.tick_params(axis='x', rotation=30)
ax2.set_ylabel('')

ax3 = fig.add_subplot(gs[0, 3])
ax3.pie(status_counts, labels=status_counts.index, autopct='%1.0f%%',
        colors=['#1D9E75','#BA7517','#D85A30'])
ax3.set_title('Order Status', fontweight='bold')

ax4 = fig.add_subplot(gs[1, :2])
ax4.bar(month_names, ontime_by_month, color='#1D9E75', edgecolor='white')
ax4.axhline(85, color='red', linestyle='--', linewidth=1)
ax4.set_title('On-Time Delivery %', fontweight='bold')
ax4.tick_params(axis='x', rotation=45)

ax5 = fig.add_subplot(gs[1, 2])
seg_cnt = rfm['Segment'].value_counts()
ax5.pie(seg_cnt, labels=seg_cnt.index, autopct='%1.0f%%',
        colors=[seg_colors.get(s,'gray') for s in seg_cnt.index])
ax5.set_title('Customer Segments', fontweight='bold')

ax6 = fig.add_subplot(gs[1, 3])
ax6.scatter(df[~df['Anomaly']]['Delivery_Days'],
            df[~df['Anomaly']]['Net_Revenue']/1000,
            c='#185FA5', alpha=0.3, s=10)
ax6.scatter(df[df['Anomaly']]['Delivery_Days'],
            df[df['Anomaly']]['Net_Revenue']/1000,
            c='#D85A30', s=40, marker='X', label='Anomaly')
ax6.set_title('Delivery vs Revenue', fontweight='bold')
ax6.set_xlabel('Days')
ax6.set_ylabel('Revenue (₹K)')

plt.savefig('../visuals/00_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("[Saved] visuals/00_dashboard.png")

print("\n✅ All analysis complete. Charts saved to ../visuals/")
