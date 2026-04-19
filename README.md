

# SAP Procure-to-Pay (P2P) Dashboard — Full Purchasing Cycle

## Project Overview

This project demonstrates the complete **Procure-to-Pay (P2P) cycle** in SAP Materials Management (MM) using an interactive simulation dashboard built with Python and Streamlit.

It covers the end-to-end procurement process from **Purchase Requisition to Vendor Payment**, including real-time analytics and reporting.

The project is designed as a capstone implementation for SAP MM, integrating business process understanding with a working application.

---

## Live Application

[https://p2pdashboardgit-sap-project.streamlit.app/](https://p2pdashboardgit-sap-project.streamlit.app/)

---

## GitHub Repository

[https://github.com/Mou4338/p2p_dashboard.git](https://github.com/Mou4338/p2p_dashboard.git)

---

## Company Scenario

ZTECH Industries Pvt. Ltd. (fictitious)

* Company Code: ZT01
* Plant: ZP01 (Bhubaneswar)
* Purchase Organization: ZPO1
* Industry: Manufacturing
* Currency: INR

The system simulates procurement of raw materials (e.g., steel sheets) with complete SAP document flow and accounting impact.

---

## Procure-to-Pay (P2P) Process Flow

1. Purchase Requisition (ME51N)
2. Request for Quotation (ME41 / ME47)
3. Vendor Evaluation (ME49 / ME61)
4. Purchase Order (ME21N)
5. Goods Receipt (MIGO)
6. Invoice Verification (MIRO)
7. Payment Processing (F110)

The Purchase Order acts as the central document linking all stages.

---

## Key Features

* Complete 7-step P2P simulation
* Interactive dashboard built with Streamlit
* Vendor evaluation using composite scoring model
* Real-time data visualization using Plotly
* GST (18%) tax calculation integrated
* Three-way matching (PO, GR, Invoice)
* Automated financial flow representation
* Exportable reports (CSV)
* Clean UI structured like SAP process flow

---

## Technology Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly

SAP Concepts Covered:

* SAP MM (Procurement lifecycle)
* SAP FI (Accounting integration)
* SAP SD (Master data alignment)
* SAP ABAP (Custom logic simulation)

---

## System Architecture

* Frontend: Streamlit UI
* Backend: Python-based simulation logic
* Data Layer: Sample datasets simulating SAP tables
* Visualization: Plotly charts and dashboards

---

## Financial Flow (Accounting Logic)

Goods Receipt (MIGO)

* Debit: Stock Account
* Credit: GR-IR Clearing

Invoice Verification (MIRO)

* Debit: GR-IR Clearing
* Debit: Input Tax (GST)
* Credit: Vendor Payable

Payment Processing (F110)

* Debit: Vendor Payable
* Credit: Bank

---

## Business Value

* Eliminates manual procurement tracking
* Ensures real-time stock and financial updates
* Prevents duplicate payments through three-way match
* Improves vendor selection with data-driven scoring
* Maintains audit-ready document flow

---

## Folder Structure

```
p2p_dashboard/
│
├── app.py
├── pages/
│   ├── overview.py
│   ├── purchase_requisition.py
│   ├── purchase_order.py
│   ├── goods_receipt.py
│   ├── invoice_verification.py
│   ├── vendor_payment.py
│   └── process_guide.py
│
├── data/
│   └── sample_data.py
│
└── requirements.txt
```

---

## How to Run Locally

```bash
git clone https://github.com/Mou4338/p2p_dashboard.git
cd p2p_dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## Unique Highlights

* Full SAP P2P cycle mapped into a working application
* Real-time integration logic between procurement and finance
* GST-compliant pricing simulation
* Vendor performance analytics
* Interactive academic + industry-ready project

---

## Future Enhancements

* SAP PP (Production Planning) integration
* SAP HR payroll cost linkage
* Advanced analytics using SAP Analytics Cloud (SAC)
* Real database integration instead of sample data

---

## Author

Moumita Das
CSE | SAP ABAP Developer
KIIT University

---

## References

* SAP Help Portal
* SAP Community Network
* KIIT University SAP Project Documentation
* Purchasing and Supply Chain Management — Van Weele


