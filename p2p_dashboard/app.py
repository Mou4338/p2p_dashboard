import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta
import random
import numpy as np
import sys, os

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="SAP P2P Process Simulation",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    .header-band {
        background: linear-gradient(135deg, #1a3a5c 0%, #2e6dad 100%);
        padding: 1.4rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .header-band h1 {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .header-band p {
        color: #d6e8f7;
        font-size: 0.88rem;
        margin: 0.3rem 0 0 0;
    }

    .step-card {
        background: #ffffff;
        border-left: 4px solid #2e6dad;
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }
    .step-card.active { border-left-color: #e87722; background: #fff8f4; }
    .step-card.done   { border-left-color: #28a745; background: #f4fff7; }

    .step-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #6c757d;
    }
    .step-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1a3a5c;
        margin: 0.1rem 0;
    }
    .step-tcode {
        font-size: 0.8rem;
        color: #e87722;
        font-family: monospace;
        font-weight: 600;
    }

    .metric-box {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .metric-box .val {
        font-size: 1.7rem;
        font-weight: 800;
        color: #1a3a5c;
    }
    .metric-box .lbl {
        font-size: 0.78rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .section-divider {
        border: none;
        border-top: 2px solid #dee2e6;
        margin: 1.5rem 0 1rem 0;
    }
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1a3a5c;
        border-bottom: 2px solid #e87722;
        display: inline-block;
        padding-bottom: 3px;
        margin-bottom: 1rem;
    }

    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-open     { background: #e3f2fd; color: #1565c0; }
    .badge-approved { background: #e8f5e9; color: #2e7d32; }
    .badge-pending  { background: #fff3e0; color: #e65100; }

    div[data-testid="stSidebar"] { background: #1a3a5c; }
    div[data-testid="stSidebar"] * { color: #d6e8f7 !important; }
    div[data-testid="stSidebar"] .stSelectbox label,
    div[data-testid="stSidebar"] .stSlider label { color: #aac8e8 !important; }
    div[data-testid="stSidebar"] hr { border-color: #2e6dad; }

    .stButton > button {
        background: #1a3a5c;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.45rem 1.4rem;
        font-weight: 600;
        font-size: 0.9rem;
        width: 100%;
    }
    .stButton > button:hover { background: #2e6dad; }

    .vendor-highlight {
        background: linear-gradient(90deg, #1a3a5c, #2e6dad);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 7px;
        margin-top: 0.8rem;
    }
    .vendor-highlight .name { font-size: 1.3rem; font-weight: 800; }
    .vendor-highlight .sub  { font-size: 0.82rem; color: #d6e8f7; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### SAP P2P Simulation")
    st.markdown("**Module:** Materials Management (MM)")
    st.markdown("---")
    st.markdown("**Process Steps**")

    steps = [
        ("Step 1", "Purchase Requisition", "ME51N"),
        ("Step 2", "Request for Quotation", "ME41 / ME47"),
        ("Step 3", "Vendor Evaluation",     "ME49 / ME61"),
        ("Step 4", "Purchase Order",        "ME21N"),
        ("Step 5", "Goods Receipt",         "MIGO"),
        ("Step 6", "Invoice Verification",  "MIRO"),
        ("Step 7", "Payment Processing",    "F110"),
    ]

    active_step = st.radio(
        "Navigate to Step",
        [f"{s[0]}: {s[1]}" for s in steps],
        index=0,
        label_visibility="collapsed",
    )
    current_idx = [f"{s[0]}: {s[1]}" for s in steps].index(active_step)

    st.markdown("---")
    st.markdown("**Company:** ZTECH Industries Pvt. Ltd.")
    st.markdown("**Comp. Code:** ZT01")
    st.markdown("**Plant:** ZP01 — Bhubaneswar")
    st.markdown("**Pur. Org.:** ZPO1")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-band">
  <h1>SAP Procure-to-Pay (P2P) — Full Purchasing Cycle</h1>
  <p>ZTECH Industries Pvt. Ltd. &nbsp;|&nbsp; Company Code: ZT01 &nbsp;|&nbsp;
     Plant: ZP01 &nbsp;|&nbsp; Purchase Organization: ZPO1 &nbsp;|&nbsp; Module: SAP MM</p>
</div>
""", unsafe_allow_html=True)

# ─── Progress Bar ─────────────────────────────────────────────────────────────
progress_pct = int(((current_idx + 1) / len(steps)) * 100)
cols_prog = st.columns([6, 1])
with cols_prog[0]:
    st.progress(progress_pct / 100)
with cols_prog[1]:
    st.markdown(f"<small style='color:#6c757d'>Step {current_idx+1} of {len(steps)}</small>",
                unsafe_allow_html=True)

# ─── Step Cards (mini flow) ───────────────────────────────────────────────────
step_cols = st.columns(len(steps))
for i, (sno, sname, tcode) in enumerate(steps):
    state = "done" if i < current_idx else ("active" if i == current_idx else "")
    indicator = "&#10003;" if i < current_idx else (str(i + 1))
    with step_cols[i]:
        st.markdown(f"""
        <div class="step-card {state}" style="padding:0.5rem 0.6rem;min-height:72px">
          <div class="step-label">{indicator}</div>
          <div class="step-title" style="font-size:0.75rem">{sname}</div>
          <div class="step-tcode">{tcode}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# STEP CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

# ── STEP 1: Purchase Requisition ──────────────────────────────────────────────
if current_idx == 0:
    st.markdown("<div class='section-title'>Step 1 — Purchase Requisition (T-Code: ME51N)</div>",
                unsafe_allow_html=True)
    st.caption("An internal department raises a request for materials. The PR triggers the procurement workflow.")

    c1, c2, c3 = st.columns(3)
    with c1:
        material = st.selectbox("Material", ["Raw Steel Sheets", "Industrial Bearings",
                                              "Electronic Components", "Hydraulic Oil", "Safety Equipment"])
        plant    = st.selectbox("Plant", ["ZP01 — Bhubaneswar", "ZP02 — Chennai"])
    with c2:
        qty      = st.number_input("Quantity Required", min_value=1, max_value=10000, value=500)
        unit     = st.selectbox("Unit of Measure", ["KG", "PC", "LTR", "MT", "BOX"])
    with c3:
        req_date = st.date_input("Required Delivery Date", value=date.today() + timedelta(days=14))
        cost_ctr = st.selectbox("Cost Center", ["CC-PROD-01 (Production)", "CC-MAINT-02 (Maintenance)",
                                                  "CC-ADMIN-03 (Admin)"])

    st.markdown("**Approval Release Strategy**")
    a1, a2, a3 = st.columns(3)
    est_val = qty * random.randint(80, 150)
    with a1:
        st.metric("Estimated Value (INR)", f"{est_val:,}")
    with a2:
        release_lvl = "Finance Head" if est_val > 500000 else "Dept. Manager"
        st.metric("Release Level Required", release_lvl)
    with a3:
        st.metric("Approval SLA", "2 Business Days")

    if st.button("Create Purchase Requisition"):
        pr_no = f"PR-{random.randint(1000000, 9999999)}"
        st.success(f"Purchase Requisition {pr_no} created successfully. Status: Open — Pending Approval.")
        st.markdown(f"""
        | Field | Value |
        |---|---|
        | PR Number | {pr_no} |
        | Material | {material} |
        | Quantity | {qty} {unit} |
        | Required Date | {req_date} |
        | Cost Center | {cost_ctr} |
        | Release Status | Pending — {release_lvl} |
        """)

# ── STEP 2: Request for Quotation ─────────────────────────────────────────────
elif current_idx == 1:
    st.markdown("<div class='section-title'>Step 2 — Request for Quotation (T-Code: ME41 / ME47)</div>",
                unsafe_allow_html=True)
    st.caption("Purchasing team issues RFQs to registered vendors. Vendor responses are entered into SAP for comparison.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**RFQ Details**")
        rfq_material = st.selectbox("Material (from approved PR)", ["Raw Steel Sheets", "Industrial Bearings",
                                                                     "Electronic Components"])
        rfq_qty = st.number_input("RFQ Quantity", min_value=1, value=500)
        rfq_deadline = st.date_input("Quotation Submission Deadline", value=date.today() + timedelta(days=5))

    with c2:
        st.markdown("**Vendor Selection**")
        vendors_selected = st.multiselect(
            "Select Vendors to Invite",
            ["ABC Suppliers (V-1001)", "XYZ Traders (V-1002)", "FastSupply Co. (V-1003)",
             "Global Parts Ltd. (V-1004)", "Prime Materials (V-1005)"],
            default=["ABC Suppliers (V-1001)", "XYZ Traders (V-1002)", "FastSupply Co. (V-1003)"]
        )

    st.markdown("**Enter Vendor Quotations**")
    if vendors_selected:
        vq_data = {}
        vcols = st.columns(len(vendors_selected))
        for i, vendor in enumerate(vendors_selected):
            with vcols[i]:
                st.markdown(f"**{vendor.split('(')[0].strip()}**")
                price = st.number_input(f"Unit Price (INR)", key=f"price_{i}", value=450 + i*50, min_value=1)
                delivery = st.number_input(f"Delivery Days", key=f"del_{i}", value=5 + i*2, min_value=1)
                vq_data[vendor] = {"price": price, "delivery": delivery}

        if st.button("Save Quotations and Generate Comparison"):
            rfq_no = f"RFQ-{random.randint(6000000, 6999999)}"
            st.success(f"RFQ {rfq_no} issued to {len(vendors_selected)} vendors. Quotations recorded.")
            df = pd.DataFrame([
                {"Vendor": v.split("(")[0].strip(), "Unit Price (INR)": d["price"],
                 "Delivery (Days)": d["delivery"], "Total Value (INR)": d["price"] * rfq_qty}
                for v, d in vq_data.items()
            ])
            df = df.sort_values("Unit Price (INR)")
            df["Rank"] = range(1, len(df) + 1)
            st.dataframe(df, use_container_width=True, hide_index=True)

# ── STEP 3: Vendor Evaluation ─────────────────────────────────────────────────
elif current_idx == 2:
    st.markdown("<div class='section-title'>Step 3 — Vendor Evaluation and Selection (T-Code: ME49 / ME61)</div>",
                unsafe_allow_html=True)
    st.caption("SAP generates a price comparison list. The procurement team evaluates vendors on price, delivery, and quality rating.")

    st.markdown("**Configure Vendor Parameters**")
    vendors = ["ABC Suppliers", "XYZ Traders", "FastSupply Co."]

    v_data = {}
    for vendor in vendors:
        c1, c2, c3 = st.columns(3)
        with c1:
            price = st.number_input(f"{vendor} — Unit Price (INR)", key=f"ep_{vendor}", value=450 + vendors.index(vendor)*50)
        with c2:
            days = st.number_input(f"{vendor} — Delivery Days", key=f"ed_{vendor}", value=6 + vendors.index(vendor)*2, min_value=1)
        with c3:
            rating = st.slider(f"{vendor} — Quality Rating", 1.0, 5.0, value=4.5 - vendors.index(vendor)*0.25, step=0.05, key=f"er_{vendor}")
        v_data[vendor] = {"price": price, "delivery": days, "rating": rating}

    if st.button("Run Vendor Evaluation"):
        records = []
        for v, d in v_data.items():
            # Scoring: 40% price (inverted), 30% delivery (inverted), 30% rating
            max_price = max(x["price"] for x in v_data.values())
            max_days  = max(x["delivery"] for x in v_data.values())
            score = (
                0.40 * (1 - (d["price"] / max_price)) +
                0.30 * (1 - (d["delivery"] / max_days)) +
                0.30 * (d["rating"] / 5.0)
            )
            records.append({
                "Vendor": v, "Unit Price (INR)": d["price"],
                "Delivery (Days)": d["delivery"], "Quality Rating": d["rating"],
                "Composite Score": round(score, 4)
            })

        df = pd.DataFrame(records).sort_values("Composite Score", ascending=False).reset_index(drop=True)
        df["Rank"] = range(1, len(df) + 1)
        best = df.iloc[0]

        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"""
            <div class="vendor-highlight">
              <div class="sub">Recommended Vendor</div>
              <div class="name">{best['Vendor']}</div>
              <div class="sub">Price: INR {best['Unit Price (INR)']:,} &nbsp;|&nbsp;
                   Delivery: {best['Delivery (Days)']} days &nbsp;|&nbsp;
                   Rating: {best['Quality Rating']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            fig = px.bar(df, x="Vendor", y="Composite Score",
                         color="Composite Score", color_continuous_scale=["#d6e8f7", "#1a3a5c"],
                         title="Vendor Composite Score Comparison",
                         labels={"Composite Score": "Score (0–1)"})
            fig.update_layout(showlegend=False, height=250, margin=dict(t=40, b=20, l=0, r=0),
                              plot_bgcolor="#f8f9fa", paper_bgcolor="#f8f9fa")
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df, use_container_width=True, hide_index=True)

# ── STEP 4: Purchase Order ────────────────────────────────────────────────────
elif current_idx == 3:
    st.markdown("<div class='section-title'>Step 4 — Purchase Order Creation (T-Code: ME21N)</div>",
                unsafe_allow_html=True)
    st.caption("A formal Purchase Order is issued to the selected vendor. The PO is a legally binding procurement document.")

    c1, c2 = st.columns(2)
    with c1:
        po_vendor  = st.selectbox("Vendor (Awarded)", ["ABC Suppliers (V-1001)", "XYZ Traders (V-1002)",
                                                        "FastSupply Co. (V-1003)"])
        po_mat     = st.selectbox("Material", ["Raw Steel Sheets", "Industrial Bearings", "Electronic Components"])
        po_qty     = st.number_input("Quantity", min_value=1, value=500)
        po_price   = st.number_input("Agreed Unit Price (INR)", min_value=1, value=450)
    with c2:
        po_plant   = st.selectbox("Delivery Plant", ["ZP01 — Bhubaneswar", "ZP02 — Chennai"])
        po_sloc    = st.selectbox("Storage Location", ["ZSL1 — Raw Material Store", "ZSL2 — Finished Goods"])
        po_del     = st.date_input("Scheduled Delivery Date", value=date.today() + timedelta(days=10))
        po_pay     = st.selectbox("Payment Terms", ["NET30 — Net 30 Days", "NET45 — Net 45 Days",
                                                     "2/10NET30 — 2% Discount if paid in 10 days"])

    total_val = po_qty * po_price
    t1, t2, t3 = st.columns(3)
    t1.metric("Total PO Value (INR)", f"{total_val:,}")
    t2.metric("Tax (GST 18%)", f"{int(total_val * 0.18):,}")
    t3.metric("Grand Total (INR)", f"{int(total_val * 1.18):,}")

    if st.button("Create and Release Purchase Order"):
        po_no = f"PO-{random.randint(4500000000, 4599999999)}"
        st.success(f"Purchase Order {po_no} created and released. Sent to {po_vendor.split('(')[0].strip()}.")
        st.markdown(f"""
        | PO Field | Value |
        |---|---|
        | PO Number | {po_no} |
        | Vendor | {po_vendor} |
        | Material | {po_mat} |
        | Quantity / UOM | {po_qty} KG |
        | Unit Price | INR {po_price:,} |
        | Total Value (excl. tax) | INR {total_val:,} |
        | Delivery Date | {po_del} |
        | Payment Terms | {po_pay} |
        | Release Status | Released |
        """)

# ── STEP 5: Goods Receipt ─────────────────────────────────────────────────────
elif current_idx == 4:
    st.markdown("<div class='section-title'>Step 5 — Goods Receipt (T-Code: MIGO)</div>",
                unsafe_allow_html=True)
    st.caption("When materials arrive at the plant, the warehouse team records the Goods Receipt (GR) against the Purchase Order.")

    c1, c2 = st.columns(2)
    with c1:
        gr_po     = st.text_input("Reference PO Number", value="4500000123")
        gr_qty    = st.number_input("Quantity Received", min_value=1, value=500)
        gr_date   = st.date_input("Receipt Date", value=date.today())
    with c2:
        gr_sloc   = st.selectbox("Storage Location", ["ZSL1 — Raw Material Store", "ZSL2 — Finished Goods"])
        gr_batch  = st.text_input("Batch Number (optional)", value="BATCH-2026-04")
        gr_qc     = st.selectbox("Quality Check Status", ["Passed — Unrestricted Stock",
                                                           "In Inspection — Quality Stock",
                                                           "Failed — Blocked Stock"])

    st.markdown("**Document Flow After GR Posting**")
    flow_df = pd.DataFrame([
        {"Document Type": "Material Document", "Number": f"50{random.randint(10000000, 99999999)}", "Effect": "Stock updated (+500 KG unrestricted)"},
        {"Document Type": "Accounting Document", "Number": f"10{random.randint(10000000, 99999999)}", "Effect": "GR/IR Clearing Account credited; Stock Account debited"},
        {"Document Type": "PO History Update", "Number": gr_po, "Effect": "GR quantity linked to PO — 3-way match initiated"},
    ])
    st.dataframe(flow_df, use_container_width=True, hide_index=True)

    if st.button("Post Goods Receipt"):
        mat_doc = f"5000{random.randint(100000, 999999)}"
        st.success(f"Goods Receipt posted. Material Document {mat_doc} generated. Stock updated in ZSL1.")
        st.info("Three-way match status: PO (open) + GR (posted) + Invoice (pending). Invoice Verification can now proceed.")

# ── STEP 6: Invoice Verification ─────────────────────────────────────────────
elif current_idx == 5:
    st.markdown("<div class='section-title'>Step 6 — Logistics Invoice Verification (T-Code: MIRO)</div>",
                unsafe_allow_html=True)
    st.caption("Vendor invoice is entered in SAP and automatically matched against the PO and GR (3-way matching).")

    c1, c2 = st.columns(2)
    with c1:
        inv_no    = st.text_input("Vendor Invoice Number", value="INV-ABC-2026-0451")
        inv_date  = st.date_input("Invoice Date", value=date.today())
        inv_ref   = st.text_input("Reference PO Number", value="4500000123")
    with c2:
        inv_amt   = st.number_input("Invoice Amount (excl. tax, INR)", min_value=1, value=225000)
        inv_tax   = st.number_input("Tax Amount (INR)", min_value=0, value=40500)
        inv_total = inv_amt + inv_tax

    st.markdown("**Three-Way Match Verification**")
    po_val, gr_val = 225000, 225000
    match_data = pd.DataFrame([
        {"Document": "Purchase Order (PO)", "Quantity": "500 KG", "Value (INR)": f"{po_val:,}", "Status": "Matched"},
        {"Document": "Goods Receipt (GR)",  "Quantity": "500 KG", "Value (INR)": f"{gr_val:,}", "Status": "Matched"},
        {"Document": "Vendor Invoice",       "Quantity": "500 KG", "Value (INR)": f"{inv_amt:,}", "Status": "Matched" if inv_amt == po_val else "Variance Detected"},
    ])

    def highlight_status(row):
        if row["Status"] == "Matched":
            return ["background-color: #e8f5e9"] * len(row)
        return ["background-color: #fff3e0"] * len(row)

    st.dataframe(match_data.style.apply(highlight_status, axis=1), use_container_width=True, hide_index=True)

    if abs(inv_amt - po_val) > 0:
        st.warning(f"Variance detected: INR {abs(inv_amt - po_val):,}. Check tolerance limits in SAP (OMR6).")
    else:
        st.success("Three-way match successful. No variance detected. Invoice approved for payment.")

    if st.button("Post Invoice"):
        acc_doc = f"1900{random.randint(100000, 999999)}"
        st.success(f"Invoice posted. Accounting Document {acc_doc} created.")
        st.markdown(f"""
        | FI Posting | Account | Amount (INR) |
        |---|---|---|
        | Dr | GR/IR Clearing Account | {inv_amt:,} |
        | Dr | Input Tax Account (GST) | {inv_tax:,} |
        | Cr | Vendor Payable Account  | {inv_total:,} |
        """)

# ── STEP 7: Payment Processing ────────────────────────────────────────────────
elif current_idx == 6:
    st.markdown("<div class='section-title'>Step 7 — Payment Processing (T-Code: F110 / F-53)</div>",
                unsafe_allow_html=True)
    st.caption("Finance processes outgoing payment to the vendor. The vendor account is cleared and the P2P cycle is complete.")

    c1, c2 = st.columns(2)
    with c1:
        pay_vendor = st.selectbox("Vendor", ["ABC Suppliers (V-1001)", "XYZ Traders (V-1002)"])
        pay_method = st.selectbox("Payment Method", ["F110 — Automatic Payment Run",
                                                      "F-53 — Manual Outgoing Payment"])
        pay_bank   = st.selectbox("House Bank", ["HDFC Bank — ZB01", "SBI — ZB02", "ICICI — ZB03"])
    with c2:
        pay_date   = st.date_input("Payment Run Date", value=date.today())
        pay_due    = st.date_input("Due Date Filter (Pay invoices due by)", value=date.today() + timedelta(days=5))
        pay_amt    = st.number_input("Payment Amount (INR)", min_value=1, value=265500)

    st.markdown("**Open Items Selected for Payment**")
    items_df = pd.DataFrame([
        {"Invoice No.": "INV-ABC-2026-0451", "Invoice Date": str(date.today() - timedelta(days=3)),
         "Due Date": str(date.today() + timedelta(days=27)), "Amount (INR)": "2,65,500", "Status": "Selected"},
    ])
    st.dataframe(items_df, use_container_width=True, hide_index=True)

    if st.button("Execute Payment Run"):
        pay_doc = f"20{random.randint(10000000, 99999999)}"
        clr_doc = f"10{random.randint(10000000, 99999999)}"
        st.success(f"Payment of INR {pay_amt:,} processed via {pay_bank.split('—')[0].strip()}.")
        st.markdown(f"""
        | FI Posting | Account | Amount (INR) |
        |---|---|---|
        | Dr | Vendor Payable Account | {pay_amt:,} |
        | Cr | Bank Outgoing Account  | {pay_amt:,} |
        """)
        st.markdown(f"""
        | Field | Value |
        |---|---|
        | Payment Document | {pay_doc} |
        | Clearing Document | {clr_doc} |
        | Vendor Account | Cleared |
        | P2P Cycle Status | **Complete** |
        """)
        st.balloons()
    
# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#aaa;font-size:0.78rem'>"
    "SAP P2P Simulation — KIIT University, School of Computer Engineering | Academic Project, 2026"
    "</p>",
    unsafe_allow_html=True
)
