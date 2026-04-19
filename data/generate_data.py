import csv, random, datetime

random.seed(42)

PRODUCTS   = ['Laptop', 'Mobile', 'Tablet', 'Monitor', 'Printer']
REGIONS    = ['North', 'South', 'East', 'West']
CUSTOMERS  = ['Tata Corp', 'Reliance Ltd', 'Infosys', 'Wipro', 'HCL Tech',
               'HDFC Bank', 'ICICI Ltd', 'Mahindra Co', 'Bajaj Auto', 'Zenith Pvt']
STATUSES   = ['Delivered', 'Delivered', 'Delivered', 'Pending', 'Cancelled']
PAY_TERMS  = ['Net30', 'Net45', 'Net60', 'Immediate']
SAP_DOC    = ['5000001','5000002','5000003','5000004','5000005']

rows = []
start = datetime.date(2024, 1, 1)

for i in range(500):
    order_date = start + datetime.timedelta(days=random.randint(0, 364))
    delivery_days = random.randint(1, 20)
    delivery_date = order_date + datetime.timedelta(days=delivery_days)
    quantity = random.randint(1, 50)
    unit_price = random.choice([800, 1200, 1500, 2000, 2500, 3000, 5000, 8000, 12000, 18000])
    revenue = quantity * unit_price
    discount = round(random.uniform(0, 0.15), 2)
    net_revenue = round(revenue * (1 - discount))
    status = random.choice(STATUSES)
    rows.append({
        'Order_ID':        f'SO-{2400 + i:04d}',
        'SAP_Doc_No':      f'00{random.choice(SAP_DOC)}{i:03d}',
        'Customer':        random.choice(CUSTOMERS),
        'Product':         random.choice(PRODUCTS),
        'Region':          random.choice(REGIONS),
        'Quantity':        quantity,
        'Unit_Price':      unit_price,
        'Discount':        discount,
        'Revenue':         revenue,
        'Net_Revenue':     net_revenue,
        'Order_Date':      order_date.isoformat(),
        'Delivery_Date':   delivery_date.isoformat(),
        'Delivery_Days':   delivery_days,
        'Payment_Terms':   random.choice(PAY_TERMS),
        'Status':          status,
        'On_Time':         'Yes' if delivery_days <= 10 else 'No',
    })

fieldnames = list(rows[0].keys())
with open('sales_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("sales_data.csv generated with", len(rows), "records")
