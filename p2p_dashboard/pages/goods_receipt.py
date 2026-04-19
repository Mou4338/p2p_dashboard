import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.sample_data import get_gr_data, MATERIALS, PLANTS, VENDORS

def show():
    st.markdown('<div class="section-header">Goods Receipt — T-Code: MIGO</div>', unsafe_allow_html=True)

    gr = get_gr_data()

    tab1, tab2, tab3 = st.tabs(["GR Register", "Post Goods Receipt", "Stock Overview"])

    with tab1:
        st.markdown("#### Goods Receipt Document List — MB51 / MIGO Display")
        col1, col2 = st.columns(2)
        with col1:
            mvt_filter   = st.multiselect("Movement Type", gr["Mvt. Type"].unique(),
                                          default=list(gr["Mvt. Type"].unique()))
        with col2:
            plant_filter = st.multiselect("Plant", gr["Plant"].unique(),
                                          default=list(gr["Plant"].unique()))

        filtered = gr[gr["Mvt. Type"].isin(mvt_filter) & gr["Plant"].isin(plant_filter)]

        def highlight_shortfall(row):
            if row["Qty Received"] < row["Qty Ordered"]:
                return ["background-color:#FFF3CD"] * len(row)
            return [""] * len(row)

        st.dataframe(
            filtered.style.apply(highlight_shortfall, axis=1),
            use_container_width=True, height=400
        )
        st.caption("Rows highlighted in yellow indicate partial deliveries where received quantity is less than ordered quantity.")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total GR Documents",  len(filtered))
        m2.metric("Total Qty Received",  f"{filtered['Qty Received'].sum():,}")
        m3.metric("Total Value (Rs)",    f"Rs {filtered['Value (Rs)'].sum():,.0f}")
        shortfall = filtered[filtered["Qty Received"] < filtered["Qty Ordered"]]
        m4.metric("Partial Deliveries",  len(shortfall), delta_color="inverse",
                  delta=f"{len(shortfall)} pending")

    with tab2:
        st.markdown("#### Post Goods Receipt — MIGO (Simulation)")
        st.info("Simulates MIGO Transaction: A01 - Goods Receipt against Purchase Order")

        with st.form("gr_form"):
            st.markdown("**Reference Document**")
            c1, c2, c3 = st.columns(3)
            with c1:
                transaction  = st.selectbox("Transaction",      ["A01 - Goods Receipt", "A07 - Goods Issue", "A08 - Transfer Posting"])
                ref_doc      = st.selectbox("Reference Doc Type",["R01 - Purchase Order", "R02 - Order", "R10 - Delivery"])
                po_ref       = st.text_input("PO Number",        value="4500010012")
            with c2:
                post_date    = st.date_input("Posting Date")
                doc_date     = st.date_input("Document Date")
                plant        = st.selectbox("Plant",             PLANTS)
            with c3:
                storage_loc  = st.selectbox("Storage Location",  ["0001 - Main Store", "0002 - Production Store", "0003 - QC Store"])
                mvt_type     = st.selectbox("Movement Type",     ["101 - GR for PO", "103 - GR into QI Stock", "105 - QI to Unrestricted"])
                delivery_note= st.text_input("Delivery Note / Challan No.", placeholder="e.g. DN-12345")

            st.markdown("**Item Data**")
            c4, c5, c6 = st.columns(3)
            with c4:
                material     = st.selectbox("Material",          [f"{k} - {v[0]}" for k, v in MATERIALS.items()])
            with c5:
                qty_ordered  = st.number_input("Ordered Qty",    min_value=0, value=200)
                qty_received = st.number_input("Qty Received",   min_value=0, value=200)
            with c6:
                item_ok      = st.checkbox("Item OK", value=True)
                batch_no     = st.text_input("Batch No. (if applicable)", placeholder="BATCH-001")

            submitted = st.form_submit_button("Post Goods Receipt", use_container_width=True)

        if submitted:
            import random
            if qty_received <= qty_ordered:
                mat_doc = random.randint(5000020000, 5000099999)
                acc_doc = random.randint(4900020000, 4900099999)
                st.success(f"Goods Receipt posted successfully. Material Document: {mat_doc}")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                    | Field | Value |
                    |---|---|
                    | Material Document | {mat_doc} |
                    | Movement Type | {mvt_type} |
                    | PO Reference | {po_ref} |
                    | Posting Date | {post_date} |
                    """)
                with c2:
                    st.markdown(f"""
                    | Field | Value |
                    |---|---|
                    | Accounting Document | {acc_doc} |
                    | Qty Received | {qty_received} |
                    | Storage Location | {storage_loc} |
                    | Next Step | MIRO — Post Vendor Invoice |
                    """)
                if qty_received < qty_ordered:
                    st.warning(f"Partial delivery: {qty_ordered - qty_received} units still pending from vendor.")
            else:
                st.error("Received quantity cannot exceed ordered quantity. Please verify and re-enter.")

    with tab3:
        st.markdown("#### Stock Overview — MMBE (Simulated)")

        np.random.seed(10)
        stock_rows = []
        for mat_id, (name, uom, price) in MATERIALS.items():
            for plant in ["1000 - Mumbai", "2000 - Pune"]:
                unr  = np.random.randint(50, 400)
                qi   = np.random.randint(0, 50)
                blkd = np.random.randint(0, 20)
                stock_rows.append({
                    "Material":        mat_id,
                    "Description":     name,
                    "Plant":           plant,
                    "UOM":             uom,
                    "Unrestricted":    unr,
                    "QI Stock":        qi,
                    "Blocked":         blkd,
                    "Total Stock":     unr + qi + blkd,
                    "Stock Value (Rs)":round((unr + qi) * price, 2),
                })
        stock_df = pd.DataFrame(stock_rows)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Stock Value", f"Rs {stock_df['Stock Value (Rs)'].sum():,.0f}")
        c2.metric("Materials in Stock", len(stock_df["Material"].unique()))
        c3.metric("Plants",             len(stock_df["Plant"].unique()))

        fig = px.bar(
            stock_df, x="Description", y=["Unrestricted", "QI Stock", "Blocked"],
            barmode="stack", title="Stock by Material and Category",
            color_discrete_map={
                "Unrestricted": "#2E75B6",
                "QI Stock":     "#FFC107",
                "Blocked":      "#DC3545"
            }
        )
        fig.update_layout(xaxis_tickangle=-30, height=360)
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(stock_df, use_container_width=True, height=280)
