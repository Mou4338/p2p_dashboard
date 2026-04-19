
# SAP Procure-to-Pay (P2P) Simulation Dashboard

## Project Overview

This project is an interactive simulation of the **SAP Procure-to-Pay (P2P) process** built using Python and Streamlit. It replicates the complete purchasing lifecycle followed in SAP Materials Management (MM), from Purchase Requisition to Vendor Payment, along with analytics and reporting.

The application provides a step-by-step walkthrough of the P2P cycle with real-time inputs, simulated data, and visual dashboards.

---

## Live Application

[https://p2pdashboardgit-sap-project.streamlit.app/](https://p2pdashboardgit-sap-project.streamlit.app/)

---

## Key Features

* Complete 8-step P2P process simulation
* Interactive UI with step-based navigation
* Real-time data entry and processing
* Vendor evaluation using composite scoring
* Automated GST calculation (18%)
* Three-way matching (PO, GR, Invoice)
* Financial postings simulation (FI integration)
* Analytics dashboard with charts and KPIs
* Exportable reports in CSV format
* Clean SAP-style user interface

---

## Process Flow Covered

1. Purchase Requisition (ME51N)
2. Request for Quotation (ME41 / ME47)
3. Vendor Evaluation (ME49 / ME61)
4. Purchase Order (ME21N)
5. Goods Receipt (MIGO)
6. Invoice Verification (MIRO)
7. Payment Processing (F110 / F-53)
8. Analytics and Reports

---

## Technology Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly

---

## SAP Concepts Simulated

* SAP MM (Procurement lifecycle)
* SAP FI (Accounting postings)
* Three-way matching (PO, GR, Invoice)
* Vendor evaluation and scoring
* GST tax calculation
* Document flow tracking

---

## Application Structure

The application is built as a single Streamlit app with sidebar-based navigation across all P2P steps.

Main components include:

* Sidebar navigation for process steps
* Dynamic forms for each transaction
* Real-time calculations and validations
* Data tables and visual dashboards
* Analytics module with KPIs and reports

---

## Financial Flow Logic

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

## Analytics and Reporting

The analytics module provides:

* Procurement cycle time trends
* Monthly spend analysis
* Vendor performance metrics
* P2P document funnel visualization
* Price variance analysis
* Custom report generation with CSV download

---

## How to Run Locally

```bash
git clone https://github.com/Mou4338/p2p_dashboard.git
cd p2p_dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## Use Case

This project is designed for:

* SAP MM learning and demonstration
* Academic projects and capstone submissions
* Understanding end-to-end procurement flow
* Showcasing SAP concepts in a working application

---

## Author

Moumita Das
CSE | SAP ABAP Developer
KIIT University

---

## Notes

* This is a simulation and does not connect to a real SAP system
* All data used is generated or sample-based
* Designed for educational and demonstration purposes

