import streamlit as st
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.sample_data import get_invoice_data, VENDORS

def show():
    st.markdown('<div class="section-header">🧾 Invoice Verification (MIRO) — 3-Way Match</div>', unsafe_allow_html=True)

    inv = get_invoice_data()

    tab1, tab2, tab3 = st.tabs(["🧾 Invoice Register", "➕ Enter Invoice (MIRO)", "📊 Invoice Analytics"])

    # ── Tab 1 ─────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("#### Logistics Invoice Verification Register — MIR5")

        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect("Status", inv["Status"].unique(), default=list(inv["Status"].unique()))
        with col2:
            vendor_filter = st.multiselect("Vendor", inv["Vendor Name"].unique(), default=list(inv["Vendor Name"].unique()))
        with col3:
            search = st.text_input("🔍 Search Invoice No.")

        filtered = inv[inv["Status"].isin(status_filter) & inv["Vendor Name"].isin(vendor_filter)]
        if search:
            filtered = filtered[filtered["Invoice No"].str.contains(search, case=False)]

        def color_row(row):
            c = {
                "Blocked":         "background-color:#F8D7DA;color:#721C24",
                "Paid":            "background-color:#D4EDDA;color:#155724",
                "Posted":          "background-color:#CCE5FF;color:#004085",
                "In Verification": "background-color:#FFF3CD;color:#856404",
            }
            return [c.get(row["Status"], "")] * len(row)

        st.dataframe(filtered.style.apply(color_row, axis=1), use_container_width=True, height=400)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Invoices", len(filtered))
        m2.metric("Total Value", f"₹{filtered['Total Amt (₹)'].sum():,.0f}")
        m3.metric("🚫 Blocked", len(filtered[filtered.Status=="Blocked"]), delta_color="inverse")
        m4.metric("✅ Paid", len(filtered[filtered.Status=="Paid"]))

        # Blocked invoices breakdown
        blocked = filtered[filtered.Status=="Blocked"]
        if len(blocked):
            with st.expander("🚫 View Blocked Invoices (Require MRBR Release)", expanded=True):
                st.dataframe(blocked[["Invoice No","Vendor Name","Total Amt (₹)","Block Reason","Due Date"]],
                             use_container_width=True)
                st.warning(f"⚠️ {len(blocked)} invoice(s) are blocked. Use T-Code **MRBR** to review and release blocked invoices.")

    # ── Tab 2: Enter Invoice ──────────────────────────────────────────────────
    with tab2:
        st.markdown("#### Simulate: Enter Vendor Invoice (MIRO)")
        st.info("💡 MIRO performs 3-Way Match: PO ↔ Goods Receipt ↔ Vendor Invoice")

        # 3-Way match visual
        st.markdown("##### 🔄 3-Way Match Concept")
        c1, c2, c3, c4, c5 = st.columns([3,1,3,1,3])
        with c1:
            st.markdown("""
            <div style='background:#CCE5FF;border-radius:8px;padding:14px;text-align:center'>
                <b>📦 Purchase Order</b><br>
                <small>PO Qty × PO Price</small>
            </div>""", unsafe_allow_html=True)
        with c2: st.markdown("<div style='text-align:center;font-size:28px;padding-top:10px'>⇌</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div style='background:#D4EDDA;border-radius:8px;padding:14px;text-align:center'>
                <b>🚚 Goods Receipt</b><br>
                <small>Qty Received</small>
            </div>""", unsafe_allow_html=True)
        with c4: st.markdown("<div style='text-align:center;font-size:28px;padding-top:10px'>⇌</div>", unsafe_allow_html=True)
        with c5:
            st.markdown("""
            <div style='background:#FFF3CD;border-radius:8px;padding:14px;text-align:center'>
                <b>🧾 Vendor Invoice</b><br>
                <small>Invoice Qty × Invoice Price</small>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        with st.form("miro_form"):
            st.markdown("**Basic Data**")
            c1, c2, c3 = st.columns(3)
            with c1:
                inv_date  = st.date_input("Invoice Date")
                post_date = st.date_input("Posting Date")
                inv_ref   = st.text_input("Vendor Invoice Ref No.", placeholder="VND-INV-2025-001")
            with c2:
                amount    = st.number_input("Invoice Amount (₹)", min_value=0.0, value=50000.0, step=100.0)
                tax_code  = st.selectbox("Tax Code", ["V0 – No Tax","V1 – GST 5%","V2 – GST 12%","V3 – GST 18%"])
                currency  = st.selectbox("Currency", ["INR","USD","EUR"])
            with c3:
                po_ref    = st.text_input("PO Reference", value="4500010012")
                gr_ref    = st.text_input("GR Document Ref", value="5000010012")
                vendor    = st.selectbox("Vendor", [f"{k} – {v}" for k,v in VENDORS.items()])

            text = st.text_area("Invoice Text / Notes", placeholder="Payment against PO 4500010012 for Steel Rods")
            submitted = st.form_submit_button("📤 Post Invoice (MIRO)", use_container_width=True)

        if submitted:
            import random
            tax_val   = float(tax_code.split("GST ")[-1].replace("%","")) if "GST" in tax_code else 0
            tax_amt   = round(amount * tax_val / 100, 2)
            total_amt = amount + tax_amt
            inv_doc   = random.randint(5105500000, 5105599999)
            acc_doc   = random.randint(1900020000, 1900099999)
            st.success(f"✅ Invoice posted! Invoice Document: **{inv_doc}**")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                | Field | Value |
                |---|---|
                | Invoice Doc. | {inv_doc} |
                | Accounting Doc. | {acc_doc} |
                | Invoice Date | {inv_date} |
                | Posting Date | {post_date} |
                """)
            with c2:
                st.markdown(f"""
                | Field | Value |
                |---|---|
                | Base Amount | ₹{amount:,.2f} |
                | Tax ({tax_code}) | ₹{tax_amt:,.2f} |
                | **Total Payable** | **₹{total_amt:,.2f}** |
                | Next Step | F110 – Auto Payment Run |
                """)

    # ── Tab 3: Analytics ──────────────────────────────────────────────────────
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            inv_stat = inv.groupby("Status")["Total Amt (₹)"].sum().reset_index()
            fig = px.pie(inv_stat, names="Status", values="Total Amt (₹)", hole=0.4,
                         title="Invoice Value by Status",
                         color="Status",
                         color_discrete_map={"Posted":"#2E75B6","Blocked":"#DC3545",
                                             "Paid":"#28A745","In Verification":"#FFC107"})
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            vend_inv = inv.groupby("Vendor Name")["Total Amt (₹)"].sum().reset_index()
            fig2 = px.bar(vend_inv, x="Total Amt (₹)", y="Vendor Name", orientation='h',
                          title="Invoice Value by Vendor",
                          color="Total Amt (₹)", color_continuous_scale="Blues")
            fig2.update_layout(coloraxis_showscale=False,
                               yaxis=dict(categoryorder='total ascending'))
            st.plotly_chart(fig2, use_container_width=True)

        # Tax analysis
        st.markdown("#### 💰 Tax Code Breakdown")
        tax_grp = inv.groupby("Tax %").agg(
            Count=("Invoice No","count"),
            Tax_Amount=("Tax Amt (₹)","sum"),
            Base_Amount=("Base Amt (₹)","sum")
        ).reset_index()
        tax_grp.columns = ["Tax %","Count","Tax Collected (₹)","Base Amount (₹)"]
        st.dataframe(tax_grp, use_container_width=True)
