"""
data/sample_data.py
-------------------
Sample data module for the SAP P2P Simulation application.
Provides pre-built DataFrames and constants consumed by all pages.
"""

import pandas as pd
from datetime import date, timedelta
import random

# ── Seed for reproducibility ──────────────────────────────────────────────────
random.seed(42)

# ── Vendor master ─────────────────────────────────────────────────────────────
VENDORS = {
    "V-1001": {"name": "ABC Suppliers",    "price": 450, "delivery_days": 6,  "rating": 4.5},
    "V-1002": {"name": "XYZ Traders",      "price": 420, "delivery_days": 8,  "rating": 4.0},
    "V-1003": {"name": "FastSupply Co.",   "price": 480, "delivery_days": 4,  "rating": 4.8},
    "V-1004": {"name": "Global Parts Ltd.","price": 410, "delivery_days": 10, "rating": 3.9},
    "V-1005": {"name": "Prime Materials",  "price": 465, "delivery_days": 5,  "rating": 4.3},
}

# ── Helper ────────────────────────────────────────────────────────────────────
def _days_ago(n):
    return str(date.today() - timedelta(days=n))

def _days_later(n):
    return str(date.today() + timedelta(days=n))

# ── Purchase Requisition data ─────────────────────────────────────────────────
def get_pr_data() -> pd.DataFrame:
    records = [
        {
            "PR Number":      "PR-1000001",
            "Material":       "Raw Steel Sheets",
            "Quantity":       500,
            "UOM":            "KG",
            "Cost Center":    "CC-PROD-01",
            "Required Date":  _days_later(14),
            "Created On":     _days_ago(5),
            "Status":         "Approved",
            "Release Level":  "Dept. Manager",
            "Est. Value (INR)": 225000,
        },
        {
            "PR Number":      "PR-1000002",
            "Material":       "Industrial Bearings",
            "Quantity":       200,
            "UOM":            "PC",
            "Cost Center":    "CC-MAINT-02",
            "Required Date":  _days_later(10),
            "Created On":     _days_ago(3),
            "Status":         "Pending",
            "Release Level":  "Finance Head",
            "Est. Value (INR)": 680000,
        },
        {
            "PR Number":      "PR-1000003",
            "Material":       "Hydraulic Oil",
            "Quantity":       1000,
            "UOM":            "LTR",
            "Cost Center":    "CC-PROD-01",
            "Required Date":  _days_later(7),
            "Created On":     _days_ago(1),
            "Status":         "Open",
            "Release Level":  "Dept. Manager",
            "Est. Value (INR)": 95000,
        },
        {
            "PR Number":      "PR-1000004",
            "Material":       "Electronic Components",
            "Quantity":       300,
            "UOM":            "PC",
            "Cost Center":    "CC-ADMIN-03",
            "Required Date":  _days_later(20),
            "Created On":     _days_ago(7),
            "Status":         "Approved",
            "Release Level":  "Dept. Manager",
            "Est. Value (INR)": 142500,
        },
        {
            "PR Number":      "PR-1000005",
            "Material":       "Safety Equipment",
            "Quantity":       50,
            "UOM":            "BOX",
            "Cost Center":    "CC-MAINT-02",
            "Required Date":  _days_later(5),
            "Created On":     _days_ago(2),
            "Status":         "Approved",
            "Release Level":  "Dept. Manager",
            "Est. Value (INR)": 37500,
        },
    ]
    return pd.DataFrame(records)


# ── Purchase Order data ───────────────────────────────────────────────────────
def get_po_data() -> pd.DataFrame:
    records = [
        {
            "PO Number":        "4500000001",
            "Vendor ID":        "V-1001",
            "Vendor Name":      "ABC Suppliers",
            "Material":         "Raw Steel Sheets",
            "Quantity":         500,
            "Unit Price (INR)": 450,
            "Total Value (INR)":225000,
            "Plant":            "ZP01",
            "Storage Loc.":     "ZSL1",
            "Delivery Date":    _days_later(6),
            "Payment Terms":    "NET30",
            "Status":           "Released",
            "PR Reference":     "PR-1000001",
        },
        {
            "PO Number":        "4500000002",
            "Vendor ID":        "V-1003",
            "Vendor Name":      "FastSupply Co.",
            "Material":         "Safety Equipment",
            "Quantity":         50,
            "Unit Price (INR)": 750,
            "Total Value (INR)":37500,
            "Plant":            "ZP01",
            "Storage Loc.":     "ZSL1",
            "Delivery Date":    _days_later(4),
            "Payment Terms":    "NET45",
            "Status":           "Released",
            "PR Reference":     "PR-1000005",
        },
        {
            "PO Number":        "4500000003",
            "Vendor ID":        "V-1005",
            "Vendor Name":      "Prime Materials",
            "Material":         "Electronic Components",
            "Quantity":         300,
            "Unit Price (INR)": 475,
            "Total Value (INR)":142500,
            "Plant":            "ZP01",
            "Storage Loc.":     "ZSL2",
            "Delivery Date":    _days_later(5),
            "Payment Terms":    "2/10NET30",
            "Status":           "Open",
            "PR Reference":     "PR-1000004",
        },
    ]
    return pd.DataFrame(records)


# ── Goods Receipt data ────────────────────────────────────────────────────────
def get_gr_data() -> pd.DataFrame:
    records = [
        {
            "Material Document": "5000000101",
            "PO Reference":      "4500000001",
            "Material":          "Raw Steel Sheets",
            "Quantity Received": 500,
            "UOM":               "KG",
            "Storage Location":  "ZSL1",
            "Receipt Date":      _days_ago(2),
            "Batch":             "BATCH-2026-04A",
            "QC Status":         "Passed — Unrestricted Stock",
            "Posted By":         "WAREHOUSE_USER",
        },
        {
            "Material Document": "5000000102",
            "PO Reference":      "4500000002",
            "Material":          "Safety Equipment",
            "Quantity Received": 50,
            "UOM":               "BOX",
            "Storage Location":  "ZSL1",
            "Receipt Date":      _days_ago(1),
            "Batch":             "BATCH-2026-04B",
            "QC Status":         "Passed — Unrestricted Stock",
            "Posted By":         "WAREHOUSE_USER",
        },
    ]
    return pd.DataFrame(records)


# ── Invoice data ──────────────────────────────────────────────────────────────
def get_invoice_data() -> pd.DataFrame:
    records = [
        {
            "Invoice No.":       "INV-ABC-2026-0451",
            "Vendor":            "ABC Suppliers",
            "PO Reference":      "4500000001",
            "GR Reference":      "5000000101",
            "Invoice Date":      _days_ago(1),
            "Base Amount (INR)": 225000,
            "Tax (GST 18%)":     40500,
            "Total (INR)":       265500,
            "3-Way Match":       "Matched",
            "Status":            "Posted",
            "Accounting Doc":    "1900000201",
        },
        {
            "Invoice No.":       "INV-FSC-2026-0112",
            "Vendor":            "FastSupply Co.",
            "PO Reference":      "4500000002",
            "GR Reference":      "5000000102",
            "Invoice Date":      str(date.today()),
            "Base Amount (INR)": 37500,
            "Tax (GST 18%)":     6750,
            "Total (INR)":       44250,
            "3-Way Match":       "Matched",
            "Status":            "Pending Payment",
            "Accounting Doc":    "1900000202",
        },
    ]
    return pd.DataFrame(records)


# ── Payment data ──────────────────────────────────────────────────────────────
def get_payment_data() -> pd.DataFrame:
    records = [
        {
            "Payment Doc":       "2000000301",
            "Clearing Doc":      "1000000401",
            "Vendor":            "ABC Suppliers",
            "Invoice Ref":       "INV-ABC-2026-0451",
            "Payment Date":      str(date.today()),
            "Amount (INR)":      265500,
            "Bank Account":      "HDFC Bank — ZB01",
            "Payment Method":    "F110 — Automatic Run",
            "Status":            "Cleared",
        },
    ]
    return pd.DataFrame(records)
