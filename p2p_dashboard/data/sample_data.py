"""
data/sample_data.py
Generates realistic fictitious P2P data for ABC Manufacturing Ltd.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ── Constants ────────────────────────────────────────────────────────────────
VENDORS = {
    "V-001": "Tata Steel Components",
    "V-002": "Mahindra Auto Parts",
    "V-003": "Bosch India Ltd.",
    "V-004": "Minda Industries",
    "V-005": "Sundaram Fasteners",
}

MATERIALS = {
    "RAW-001": ("Steel Rod 10mm",         "KG",   45.00),
    "RAW-002": ("Aluminium Sheet 2mm",    "KG",   180.00),
    "RAW-003": ("Engine Bolts M8",        "PC",   12.50),
    "RAW-004": ("Rubber Gasket Set",      "SET",  340.00),
    "RAW-005": ("Copper Wire 1.5mm",      "MTR",  95.00),
    "RAW-006": ("Paint – Industrial Blue","LTR",  220.00),
    "RAW-007": ("Bearings 6205",          "PC",   185.00),
    "RAW-008": ("Filter Element",         "PC",   450.00),
}

PLANTS       = ["1000 – Mumbai", "2000 – Pune", "3000 – Chennai"]
PURCH_GROUPS = ["001 – Mechanical", "002 – Electrical", "003 – General"]
TODAY        = datetime.today()

def rdate(days_ago_max=120, days_ago_min=0):
    d = random.randint(days_ago_min, days_ago_max)
    return TODAY - timedelta(days=d)

def fmt(dt): return dt.strftime("%d-%b-%Y")

# ── Purchase Requisitions ────────────────────────────────────────────────────
def get_pr_data():
    rows = []
    statuses = ["Open", "Approved", "Converted to PO", "Rejected"]
    weights   = [0.20, 0.15, 0.55, 0.10]
    for i in range(1, 31):
        mat_id = random.choice(list(MATERIALS))
        mat_name, uom, price = MATERIALS[mat_id]
        qty    = random.randint(50, 500)
        status = random.choices(statuses, weights)[0]
        cr_dt  = rdate(90)
        rows.append({
            "PR Number":    f"10000{10000+i}",
            "Material":     mat_id,
            "Description":  mat_name,
            "Quantity":     qty,
            "UOM":          uom,
            "Est. Value (₹)": round(qty * price, 2),
            "Plant":        random.choice(PLANTS),
            "Purch. Group": random.choice(PURCH_GROUPS),
            "Created On":   fmt(cr_dt),
            "Req. Delivery":fmt(cr_dt + timedelta(days=random.randint(15,45))),
            "Status":       status,
            "Raised By":    random.choice(["Ravi Kumar","Priya S.","Amit Joshi","Neha T.","Suresh M."]),
        })
    return pd.DataFrame(rows)

# ── Purchase Orders ─────────────────────────────────────────────────────────
def get_po_data():
    rows = []
    statuses = ["Open", "Partially Delivered", "Fully Delivered", "Closed"]
    weights   = [0.20, 0.25, 0.40, 0.15]
    for i in range(1, 26):
        vend_id  = random.choice(list(VENDORS))
        mat_id   = random.choice(list(MATERIALS))
        mat_name, uom, price = MATERIALS[mat_id]
        qty       = random.randint(100, 800)
        net_price = round(price * random.uniform(0.9, 1.1), 2)
        status    = random.choices(statuses, weights)[0]
        po_dt     = rdate(80)
        rows.append({
            "PO Number":    f"45000{10000+i}",
            "Vendor ID":    vend_id,
            "Vendor Name":  VENDORS[vend_id],
            "Material":     mat_id,
            "Description":  mat_name,
            "Quantity":     qty,
            "UOM":          uom,
            "Net Price (₹)":net_price,
            "PO Value (₹)": round(qty * net_price, 2),
            "PO Date":      fmt(po_dt),
            "Delivery Date":fmt(po_dt + timedelta(days=random.randint(14,30))),
            "Plant":        random.choice(PLANTS),
            "Status":       status,
            "PR Reference": f"10000{10010+i}",
        })
    return pd.DataFrame(rows)

# ── Goods Receipts ───────────────────────────────────────────────────────────
def get_gr_data():
    rows = []
    mvt_types = ["101 – GR for PO", "103 – GR into QI", "105 – Release from QI"]
    for i in range(1, 21):
        mat_id   = random.choice(list(MATERIALS))
        mat_name, uom, price = MATERIALS[mat_id]
        qty_ord   = random.randint(100, 500)
        qty_recv  = random.randint(int(qty_ord*0.7), qty_ord)
        gr_dt     = rdate(60)
        rows.append({
            "GR Doc. No":   f"50000{10000+i}",
            "PO Reference": f"45000{10010+i}",
            "Material":     mat_id,
            "Description":  mat_name,
            "Mvt. Type":    random.choice(mvt_types),
            "Qty Ordered":  qty_ord,
            "Qty Received": qty_recv,
            "UOM":          uom,
            "Value (₹)":    round(qty_recv * price, 2),
            "Storage Loc.": random.choice(["0001","0002","0003"]),
            "Plant":        random.choice(PLANTS),
            "Posting Date": fmt(gr_dt),
            "Delivery Note":f"DN-{random.randint(10000,99999)}",
            "Vendor":       random.choice(list(VENDORS.values())),
        })
    return pd.DataFrame(rows)

# ── Invoices ─────────────────────────────────────────────────────────────────
def get_invoice_data():
    rows = []
    statuses = ["Posted", "Blocked", "Paid", "In Verification"]
    weights   = [0.35, 0.20, 0.35, 0.10]
    block_reasons = ["Price variance > tolerance","Qty mismatch","Missing GR","Duplicate Invoice",""]
    for i in range(1, 21):
        vend_id   = random.choice(list(VENDORS))
        base_amt  = random.randint(10000, 250000)
        tax_pct   = random.choice([0, 5, 12, 18])
        tax_amt   = round(base_amt * tax_pct / 100, 2)
        status    = random.choices(statuses, weights)[0]
        inv_dt    = rdate(50)
        block_r   = random.choice(block_reasons) if status == "Blocked" else ""
        rows.append({
            "Invoice No":   f"51055{10000+i}",
            "PO Reference": f"45000{10010+i}",
            "Vendor ID":    vend_id,
            "Vendor Name":  VENDORS[vend_id],
            "Invoice Date": fmt(inv_dt),
            "Posting Date": fmt(inv_dt + timedelta(days=random.randint(1,5))),
            "Base Amt (₹)": base_amt,
            "Tax %":        tax_pct,
            "Tax Amt (₹)":  tax_amt,
            "Total Amt (₹)":round(base_amt + tax_amt, 2),
            "Status":       status,
            "Block Reason": block_r,
            "Due Date":     fmt(inv_dt + timedelta(days=30)),
        })
    return pd.DataFrame(rows)

# ── Payments ──────────────────────────────────────────────────────────────────
def get_payment_data():
    rows = []
    methods  = ["Bank Transfer (NEFT)", "Cheque", "RTGS", "Online Banking"]
    statuses = ["Cleared", "Pending", "Overdue"]
    weights  = [0.55, 0.30, 0.15]
    for i in range(1, 18):
        vend_id  = random.choice(list(VENDORS))
        amount   = random.randint(15000, 300000)
        status   = random.choices(statuses, weights)[0]
        pay_dt   = rdate(45)
        rows.append({
            "Payment Doc":  f"20000{10000+i}",
            "Invoice Ref":  f"51055{10010+i}",
            "Vendor ID":    vend_id,
            "Vendor Name":  VENDORS[vend_id],
            "Amount (₹)":   amount,
            "Currency":     "INR",
            "Payment Date": fmt(pay_dt),
            "Due Date":     fmt(pay_dt - timedelta(days=random.randint(-5,10))),
            "Method":       random.choice(methods),
            "Bank Ref":     f"TXN{random.randint(100000000,999999999)}",
            "Status":       status,
            "Cleared By":   random.choice(["F110 – Auto Pay","F-53 – Manual"]),
        })
    return pd.DataFrame(rows)
