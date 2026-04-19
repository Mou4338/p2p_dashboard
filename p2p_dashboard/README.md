# SAP P2P Process Simulation

An interactive Streamlit application that simulates the complete **Procure-to-Pay (P2P)** purchasing cycle in SAP Materials Management (MM).

---

## Overview

This project demonstrates the end-to-end SAP P2P cycle for a fictitious company, **ZTECH Industries Pvt. Ltd.** (Company Code: ZT01, Plant: ZP01), covering all seven procurement process steps with realistic SAP transaction codes, document flows, and accounting entries.

**Submitted as part of:** SAP Certification Training — KIIT University, School of Computer Engineering, 2026.

---

## Process Steps Covered

| Step | Process | SAP T-Code |
|------|---------|------------|
| 1 | Purchase Requisition | ME51N |
| 2 | Request for Quotation | ME41 / ME47 |
| 3 | Vendor Evaluation | ME49 / ME61 |
| 4 | Purchase Order | ME21N |
| 5 | Goods Receipt | MIGO |
| 6 | Invoice Verification (LIV) | MIRO |
| 7 | Payment Processing | F110 / F-53 |

---

## Features

- Step-by-step navigation through the complete P2P cycle
- Vendor evaluation with composite scoring (price 40%, delivery 30%, quality 30%)
- Automated three-way matching simulation (PO + GR + Invoice)
- Real-time accounting document generation display
- SAP organizational structure sidebar reference
- Clean, formal UI with no external API dependencies

---

## Project Structure

```
sap_p2p_simulation/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules
```

---

## Setup and Run Locally

**Prerequisites:** Python 3.9 or higher

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/sap_p2p_simulation.git
cd sap_p2p_simulation

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select this repository.
4. Set **Main file path** to `app.py`.
5. Click **Deploy**.

---

## SAP Organizational Structure

| Object | Value |
|--------|-------|
| Company Code | ZT01 |
| Plant | ZP01 — Bhubaneswar |
| Storage Location | ZSL1 — Raw Material Store |
| Purchase Organization | ZPO1 |
| Purchase Group | ZPG |

---

## Tech Stack

- **Frontend / App Framework:** Streamlit
- **Data Processing:** Pandas
- **Visualization:** Plotly
- **Language:** Python 3.9+

---

## Academic Integrity

This project is an individual submission. All content, logic, and structure are original work developed for academic purposes under the KIIT SAP Training Program guidelines.
