# 🏭 SAP P2P Dashboard — Procure-to-Pay (SAP MM)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

A full-stack interactive dashboard simulating the **Procure-to-Pay (P2P)** business process in **SAP MM**, built with Python & Streamlit.

Submitted as part of the **KIIT University SAP Project** (Academic Year 2024-25).

---

## 📋 Project Details

| Field | Value |
|---|---|
| **Topic** | Procure-to-Pay (P2P) — Full Purchasing Cycle |
| **Module** | SAP MM (Materials Management) |
| **Company** | ABC Manufacturing Ltd. (Fictitious) |
| **Academic Year** | 2024-25 |
| **Tech Stack** | Python, Streamlit, Plotly, Pandas |

---

## 🚀 Features

| Page | Description |
|---|---|
| 🏠 Overview | Executive KPI dashboard, process flow, financial summary |
| 📋 Purchase Requisition | PR register, create PR form (ME51N simulation), analytics |
| 📦 Purchase Order | PO register, create PO form (ME21N simulation), analytics |
| 🚚 Goods Receipt | GR register, post GR form (MIGO simulation), stock overview |
| 🧾 Invoice Verification | 3-Way Match, MIRO simulation, blocked invoice management |
| 💳 Vendor Payment | F110 auto payment run, F-53 manual payment, analytics |
| 📊 Analytics & Reports | Spend analysis, cycle times, custom report downloads |
| ℹ️ Process Guide | Step-by-step guide, T-Code reference, SPRO config checklist |

---

## 🔄 P2P Process Flow

```
Purchase Requisition (ME51N)
        ↓
Request for Quotation (ME41) → Quotation Comparison (ME49)
        ↓
Purchase Order (ME21N)
        ↓
Goods Receipt (MIGO — Mvt. Type 101)
        ↓
Invoice Verification — 3-Way Match (MIRO)
        ↓
Vendor Payment (F110 / F-53)
```

---

## 📦 Folder Structure

```
p2p_dashboard/
│
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # Python dependencies
├── README.md
│
├── data/
│   ├── __init__.py
│   └── sample_data.py        # Fictitious SAP data generator
│
└── pages/
    ├── __init__.py
    ├── overview.py           # Overview Dashboard
    ├── purchase_requisition.py
    ├── purchase_order.py
    ├── goods_receipt.py
    ├── invoice_verification.py
    ├── vendor_payment.py
    ├── analytics.py
    └── process_guide.py
```

---

## 🛠️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/p2p_dashboard.git
cd p2p_dashboard

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → Select your repo
4. Set **Main file path**: `app.py`
5. Click **Deploy** — Done! 🎉

---

## 🏢 SAP Organizational Structure (Fictitious)

| Object | Value | Description |
|---|---|---|
| Company Code | 1000 | ABC Manufacturing Ltd. |
| Plant | 1000 | Mumbai Main Plant |
| Plant | 2000 | Pune Plant |
| Storage Location | 0001 | Main Warehouse |
| Purchasing Org. | 1000 | Central Purchasing |
| Purchasing Group | 001 | Mechanical Buying |

---

## 📚 Key SAP T-Codes Covered

`ME51N` `ME41` `ME47` `ME49` `ME21N` `MIGO` `MIRO` `MRBR` `F110` `F-53` `MMBE` `MB51` `XK01` `MM01` `SPRO`

---

## 📝 License

Academic project — KIIT University, 2024-25. For educational purposes only.
